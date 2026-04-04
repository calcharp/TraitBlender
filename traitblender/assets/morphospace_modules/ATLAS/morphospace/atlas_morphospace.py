"""
ATLAS DATABASE-style deformation: dense markup targets from SSM PCs + Local RBF (Gaussian KNN)
matching agporto/ATLAS DATABASE.py (default method).

Template mesh is loaded with Blender's PLY importer (wm.ply_import).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import bpy
import numpy as np
from mathutils import Vector
from mathutils.kdtree import KDTree

from .atlas_morphospace_sample import AtlasMorphospaceSample


def _norm_cs(cs: str) -> str:
    s = str(cs).upper()
    if "LPS" in s or s == "0":
        return "LPS"
    if "RAS" in s or s == "1":
        return "RAS"
    return "RAS"


def _read_fcsv_points(path: Path) -> tuple[np.ndarray, str]:
    cs = "RAS"
    pts: list[tuple[float, float, float]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            if "CoordinateSystem" in line:
                cs = _norm_cs(line.split("=", 1)[-1])
            continue
        parts = line.strip().split(",")
        if len(parts) >= 4:
            try:
                pts.append((float(parts[1]), float(parts[2]), float(parts[3])))
            except ValueError:
                continue
    return np.asarray(pts, dtype=np.float64), cs


def _markups_points_ras(path: Path) -> np.ndarray:
    if path.suffix.lower() == ".fcsv":
        pts, cs = _read_fcsv_points(path)
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
        m = (data.get("markups") or [{}])[0]
        cs = _norm_cs(m.get("coordinateSystem", "RAS"))
        cps = m.get("controlPoints") or []
        pts = np.asarray([cp["position"] for cp in cps], dtype=np.float64)
    if cs == "LPS":
        a = pts.copy()
        a[:, :2] *= -1.0
        return a
    return pts


def _resolve_db_paths(db_root: Path) -> tuple[Path, Path, Path]:
    manifest_path = db_root / "manifest.json"
    if manifest_path.is_file():
        man = json.loads(manifest_path.read_text(encoding="utf-8"))
        files = man.get("files") or {}
        model = db_root / files.get("model", "")
        dense = db_root / files.get("dense", "")
        ssm = db_root / files.get("ssm", "ssm_model.npz")
        if model.is_file() and dense.is_file() and ssm.is_file():
            return model, dense, ssm
    files = sorted(db_root.iterdir())
    models = [f for f in files if f.suffix.lower() in (".ply", ".vtk", ".vtp", ".stl")]
    npzs = [f for f in files if f.suffix.lower() == ".npz"]
    markups = [f for f in files if f.suffix.lower() in (".json", ".fcsv")]
    if not models or not npzs or not markups:
        raise FileNotFoundError(
            f"Incomplete ATLAS database folder (need model, markups, npz): {db_root}"
        )
    ssm = db_root / "ssm_model.npz" if (db_root / "ssm_model.npz").is_file() else npzs[0]
    dense_hint = [f for f in markups if "dense" in f.name.lower() or "corr" in f.name.lower()]
    lm = dense_hint[0] if dense_hint else markups[0]
    return models[0], lm, ssm


def _import_ply_geometry(filepath: str) -> tuple[np.ndarray, list[tuple[int, ...]]]:
    """Import PLY via Blender; return vertex positions and polygon vertex index tuples."""
    path = bpy.path.abspath(filepath)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"PLY not found: {path}")

    bpy.ops.object.select_all(action="DESELECT")
    before = {o.name for o in bpy.data.objects}

    import_ok = False
    try:
        bpy.ops.wm.ply_import(filepath=path)
        import_ok = True
    except Exception:
        pass
    if not import_ok:
        try:
            if hasattr(bpy.ops, "import_mesh") and hasattr(bpy.ops.import_mesh, "ply"):
                bpy.ops.import_mesh.ply(filepath=path)
                import_ok = True
        except Exception:
            pass
    if not import_ok:
        raise RuntimeError(
            "ATLAS: PLY import failed. Ensure Blender can import PLY (e.g. wm.ply_import)."
        )

    new_objs = [bpy.data.objects[n] for n in bpy.data.objects.keys() if n not in before]
    obj = None
    for o in new_objs:
        if o.type == "MESH":
            obj = o
            break
    if obj is None:
        obj = bpy.context.view_layer.objects.active
    if obj is None or obj.type != "MESH":
        raise RuntimeError("PLY import did not produce a mesh object")

    mesh = obj.data
    verts = np.empty((len(mesh.vertices), 3), dtype=np.float64)
    for i, v in enumerate(mesh.vertices):
        verts[i, 0] = v.co.x
        verts[i, 1] = v.co.y
        verts[i, 2] = v.co.z
    faces = [tuple(p.vertices) for p in mesh.polygons]

    mesh_name = mesh.name
    bpy.data.objects.remove(obj, do_unlink=True)
    orphan = bpy.data.meshes.get(mesh_name)
    if orphan is not None and orphan.users == 0:
        bpy.data.meshes.remove(orphan, do_unlink=True)

    return verts, faces


def _precompute_local_rbf(
    template_vertices: np.ndarray, landmark_ras: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """DATABASE Local RBF: k=min(32,nL), h=75th percentile of k-th neighbor distance."""
    v = np.asarray(template_vertices, dtype=np.float64, copy=False)
    lm = np.asarray(landmark_ras, dtype=np.float64, copy=False)
    n_l = int(lm.shape[0])
    k = int(min(32, n_l))
    kd = KDTree(n_l)
    for i in range(n_l):
        kd.insert(Vector(lm[i]), i)
    kd.balance()

    n_v = int(v.shape[0])
    idx = np.zeros((n_v, k), dtype=np.int64)
    dist = np.zeros((n_v, k), dtype=np.float64)
    for i in range(n_v):
        found = kd.find_n(v[i], k)
        for j, item in enumerate(found):
            _co, ix, d = item
            idx[i, j] = int(ix)
            dist[i, j] = float(d)

    h = float(np.percentile(dist[:, -1], 75)) + 1e-9
    w = np.exp(-(dist * dist) / (h * h))
    w /= w.sum(axis=1, keepdims=True)
    return idx, w


def _apply_local_rbf(
    v0: np.ndarray,
    original_lm: np.ndarray,
    target_lm: np.ndarray,
    indices: np.ndarray,
    weights: np.ndarray,
) -> np.ndarray:
    delta_lm = np.asarray(target_lm, dtype=np.float64) - np.asarray(
        original_lm, dtype=np.float64
    )
    neighbor_deltas = delta_lm[indices]
    disp = np.sum(neighbor_deltas * weights[..., np.newaxis], axis=1)
    return np.asarray(v0, dtype=np.float64) + disp


def generate_atlas_sample(
    name: str, hyperparameters: dict | None, pc_values: list[float]
) -> AtlasMorphospaceSample:
    hp = dict(hyperparameters or {})
    db_raw = (hp.get("database_path") or "").strip()
    if not db_raw:
        raise ValueError(
            "ATLAS morphospace: set hyperparameter 'database_path' to your DATABASE folder "
            "(manifest + template_model + dense_correspondences + ssm_model.npz)."
        )
    db_root = Path(bpy.path.abspath(db_raw))
    if not db_root.is_dir():
        raise ValueError(f"ATLAS database_path is not a directory: {db_root}")

    num_pcs_cfg = int(hp.get("num_pcs", 0))
    if num_pcs_cfg < 0:
        num_pcs_cfg = 0

    model_path, dense_path, ssm_path = _resolve_db_paths(db_root)

    z = np.load(ssm_path, allow_pickle=False)
    mean_shape = np.asarray(z["mean_shape"], dtype=np.float64)
    modes = np.asarray(z["modes"], dtype=np.float64)
    eigenvalues = np.asarray(z["eigenvalues"], dtype=np.float64)
    n_modes = int(modes.shape[2]) if modes.ndim == 3 else 0
    if n_modes < 1:
        raise ValueError("SSM has no modes in ssm_model.npz")

    landmarks_ras = _markups_points_ras(dense_path)
    if int(landmarks_ras.shape[0]) != int(mean_shape.shape[0]):
        raise ValueError(
            f"Dense landmark count {landmarks_ras.shape[0]} != SSM rows {mean_shape.shape[0]}"
        )

    n_use = min(num_pcs_cfg, n_modes, len(pc_values))
    coeff = np.zeros(n_modes, dtype=np.float64)
    for i in range(n_use):
        coeff[i] = float(pc_values[i]) * float(np.sqrt(max(eigenvalues[i], 0.0)))
    agg = np.tensordot(modes, coeff, axes=(2, 0))
    target_lm = landmarks_ras + agg

    v0, faces = _import_ply_geometry(str(model_path))
    idx, w_b = _precompute_local_rbf(v0, landmarks_ras)
    v_new = _apply_local_rbf(v0, landmarks_ras, target_lm, idx, w_b)

    scale = float(hp.get("scale", 1.0))
    if scale <= 0.0:
        raise ValueError("ATLAS hyperparameter 'scale' must be positive")
    v_new = v_new * scale

    verts = [tuple(map(float, row)) for row in v_new]
    return AtlasMorphospaceSample(name, verts, faces)
