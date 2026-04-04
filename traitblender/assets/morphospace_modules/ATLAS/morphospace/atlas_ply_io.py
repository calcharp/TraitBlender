"""
Load PLY vertex positions and faces exactly as stored in the file.

Blender's ``wm.ply_import`` applies forward/up axis remapping; ATLAS dense markups are
numeric RAS/LPS coordinates with no such remap. Using the importer desynchronizes
mesh vertices from landmarks and corrupts Local RBF warping (e.g. lateral pulls on PC1).
"""

from __future__ import annotations

import struct
from pathlib import Path

import numpy as np


def read_ply_vertices_and_faces(path: Path) -> tuple[np.ndarray, list[tuple[int, ...]]]:
    """
    Return (vertices Nx3 float64, faces as list of vertex-index tuples).

    Supports ASCII and binary_little_endian / binary_big_endian PLY with x,y,z vertex props.
    Triangulates n-gon faces with a fan (same as typical Slicer VTK exports).
    """
    raw = path.read_bytes()
    if b"end_header\r\n" in raw:
        sep = b"end_header\r\n"
        nl = 2
    elif b"end_header\n" in raw:
        sep = b"end_header\n"
        nl = 1
    else:
        raise ValueError(f"Invalid PLY (no end_header): {path}")

    header_end = raw.index(sep) + len(sep)
    header_text = raw[: header_end - nl].decode("ascii", errors="replace")
    lines = header_text.splitlines()

    fmt = "ascii"
    n_verts = 0
    n_faces = 0
    props: list[tuple[str, str]] = []
    in_vertex = False
    in_face = False
    # Binary face lists: `property list uchar int vertex_indices` (VTK may use int/int)
    face_list_count_type = "uchar"
    face_list_index_type = "int"

    for line in lines:
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "format" and len(parts) >= 2:
            fmt = parts[1]
        elif parts[0] == "element" and len(parts) >= 3:
            in_vertex = parts[1] == "vertex"
            in_face = parts[1] == "face"
            if in_vertex:
                n_verts = int(parts[2])
            elif in_face:
                n_faces = int(parts[2])
        elif parts[0] == "property" and in_vertex and len(parts) >= 3:
            props.append((parts[1], parts[2]))
        elif parts[0] == "property" and in_face and len(parts) >= 5 and parts[1] == "list":
            face_list_count_type = parts[2]
            face_list_index_type = parts[3]

    body = raw[header_end:]

    def dtype_char(t: str) -> str:
        return {
            "char": "b",
            "uchar": "B",
            "short": "h",
            "ushort": "H",
            "int": "i",
            "uint": "I",
            "float": "f",
            "double": "d",
        }[t]

    xi = next((i for i, (_, n) in enumerate(props) if n.lower() in ("x",)), None)
    yi = next((i for i, (_, n) in enumerate(props) if n.lower() in ("y",)), None)
    zi = next((i for i, (_, n) in enumerate(props) if n.lower() in ("z",)), None)
    if xi is None or yi is None or zi is None:
        raise ValueError(f"PLY missing x,y,z vertex properties: {path}")

    if fmt == "ascii":
        text = body.decode("ascii", errors="replace").strip().split()
        floats = [float(x) for x in text]
        stride = len(props)
        verts = np.zeros((n_verts, 3), dtype=np.float64)
        off = 0
        for i in range(n_verts):
            verts[i, 0] = floats[off + xi]
            verts[i, 1] = floats[off + yi]
            verts[i, 2] = floats[off + zi]
            off += stride
        face_list: list[tuple[int, ...]] = []
        if n_faces > 0:
            for _ in range(n_faces):
                nidx = int(floats[off])
                off += 1
                idx = [int(floats[off + j]) for j in range(nidx)]
                off += nidx
                if nidx == 3:
                    face_list.append((idx[0], idx[1], idx[2]))
                elif nidx > 3:
                    for j in range(1, nidx - 1):
                        face_list.append((idx[0], idx[j], idx[j + 1]))
        return verts, face_list

    if fmt not in ("binary_little_endian", "binary_big_endian"):
        raise ValueError(f"Unsupported PLY format: {fmt}")
    endian = "<" if fmt == "binary_little_endian" else ">"
    off = 0
    vertex_fmt = endian + "".join(dtype_char(t) for t, _ in props)
    vstruct = struct.Struct(vertex_fmt)
    verts = np.zeros((n_verts, 3), dtype=np.float64)
    for i in range(n_verts):
        chunk = body[off : off + vstruct.size]
        off += vstruct.size
        vals = vstruct.unpack(chunk)
        verts[i] = (float(vals[xi]), float(vals[yi]), float(vals[zi]))

    face_list = []
    if n_faces > 0:
        cnt_c = dtype_char(face_list_count_type)
        idx_c = dtype_char(face_list_index_type)
        cnt_pack = endian + cnt_c
        cnt_sz = struct.calcsize(cnt_pack)
        idx_sz = struct.calcsize(endian + idx_c)
        for _ in range(n_faces):
            nidx = int(struct.unpack_from(cnt_pack, body, off)[0])
            off += cnt_sz
            idx_fmt = endian + str(nidx) + idx_c
            idx = list(struct.unpack_from(idx_fmt, body, off))
            off += nidx * idx_sz
            if nidx == 3:
                face_list.append((idx[0], idx[1], idx[2]))
            else:
                for j in range(1, nidx - 1):
                    face_list.append((idx[0], idx[j], idx[j + 1]))

    return verts, face_list
