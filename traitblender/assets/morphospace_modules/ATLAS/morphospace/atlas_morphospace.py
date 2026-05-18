"""
ATLAS morphospace sample generation (TraitBlender wrapper around atlas_core).
"""

from __future__ import annotations

from pathlib import Path

import bpy
import numpy as np

from .atlas_core import build_deformed_mesh_arrays, load_ssm, resolve_database_paths
from .atlas_morphospace_sample import AtlasMorphospaceSample


def _log(msg: str) -> None:
    print(f"[ATLAS] {msg}")


def generate_atlas_sample(
    name: str,
    hyperparameters: dict | None,
    pc_values: list[float],
) -> AtlasMorphospaceSample:
    hp = dict(hyperparameters or {})
    db_raw = (hp.get("database_dir") or hp.get("database_path") or "").strip()
    if not db_raw:
        raise ValueError(
            "ATLAS morphospace: set hyperparameter 'database_dir' to your DATABASE folder "
            "(manifest + template model + dense correspondences + ssm_model.npz)."
        )
    db_root = Path(bpy.path.abspath(db_raw))
    if not db_root.is_dir():
        raise ValueError(f"ATLAS database_dir is not a directory: {db_root}")

    n_comp_cfg = max(0, int(hp.get("n_components", 10)))
    scale = float(hp.get("scale", 1.0))

    if scale <= 0.0:
        raise ValueError("ATLAS hyperparameter 'scale' must be positive")

    _log(f"sample {name!r}: database_dir={db_root}")
    _log(f"  n_components={n_comp_cfg}, scale={scale}")

    paths = resolve_database_paths(db_root)
    _log(
        "  files — "
        f"model={paths['model'].name}, dense={paths['dense'].name}, ssm={paths['ssm'].name}"
    )

    ssm = load_ssm(paths)
    n_modes = int(ssm["n_modes"])
    if n_modes < 1:
        raise ValueError("SSM has no modes in ssm_model.npz")

    sigma = np.zeros(n_modes, dtype=np.float64)
    n_use = min(n_comp_cfg, n_modes, len(pc_values))
    sigma[:n_use] = np.asarray(pc_values[:n_use], dtype=np.float64)

    active = [i for i in range(n_use) if abs(sigma[i]) > 1e-12]
    if active:
        desc = ", ".join(f"PC{i + 1}={sigma[i]:.4g}σ" for i in active[:8])
        more = f" … (+{len(active) - 8} more)" if len(active) > 8 else ""
        _log(f"  active PCs: {desc}{more}")
    else:
        _log("  active PCs: none (template dense shape)")

    vertices, faces = build_deformed_mesh_arrays(
        paths,
        sigma,
        mesh_from_lps=True,
    )

    if scale != 1.0:
        _log(f"  uniform scale={scale}")
        vertices = vertices * scale

    _log(f"  mesh: {vertices.shape[0]} verts, {len(faces)} faces")
    verts = [tuple(map(float, row)) for row in vertices]
    return AtlasMorphospaceSample(name, verts, faces)
