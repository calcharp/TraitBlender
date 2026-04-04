"""
ATLAS morphospace: 3D Slicer ATLAS DATABASE bundle (SSM + dense correspondences + template PLY).

Traits: PC1 .. PC64 (σ-multiples per PC, same convention as DATABASE sliders). Increase MAX_ATLAS_PCS in
morphospace/__init__.py if you need more columns exposed.
Hyperparameters: num_pcs, database_path (folder), scale (uniform factor applied to mesh vertices after warp).
"""

from .morphospace import MAX_ATLAS_PCS, generate_atlas_sample
from .orientations import ORIENTATIONS

NAME = "ATLAS"

HYPERPARAMETERS = {
    "num_pcs": 5,
    "database_path": "",
    "scale": 1.0,
}

_pc_sig = ", ".join(f"PC{i}=0.0" for i in range(1, MAX_ATLAS_PCS + 1))
_pc_expr = "[" + ", ".join(f"PC{i}" for i in range(1, MAX_ATLAS_PCS + 1)) + "]"
_exec_src = (
    f"def sample(name='ATLAS', {_pc_sig}, hyperparameters=None):\n"
    f"    return generate_atlas_sample(name, hyperparameters or {{}}, {_pc_expr})\n"
)
_ns: dict = {"generate_atlas_sample": generate_atlas_sample}
exec(_exec_src, _ns)
sample = _ns["sample"]

__all__ = ["NAME", "sample", "HYPERPARAMETERS", "ORIENTATIONS", "MAX_ATLAS_PCS"]
