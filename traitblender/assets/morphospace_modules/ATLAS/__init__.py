"""
ATLAS morphospace: 3D Slicer ATLAS DATABASE bundle (SSM + dense correspondences + template PLY).

Trait columns are ``PC1`` … ``PC{num_pcs}`` (from hyperparameter ``num_pcs``, capped at ``MAX_ATLAS_PCS``);
see ``get_trait_parameters_with_defaults``. The ``sample()`` signature still includes up to ``MAX_ATLAS_PCS``
parameters so extra PCs default to 0 if present in older CSVs.

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


def get_trait_parameters_with_defaults(merged_hyperparameters):
    """
    Optional morphospace hook: define dataset columns / validation traits from merged hyperparameters.

    Returns:
        Ordered map ``PC1`` … ``PC{num_pcs}`` (σ-multiples, DATABASE-style), each default ``0.0``.
    """
    n = int(merged_hyperparameters.get("num_pcs", HYPERPARAMETERS["num_pcs"]))
    n = max(0, min(n, MAX_ATLAS_PCS))
    return {f"PC{i}": 0.0 for i in range(1, n + 1)}

_pc_sig = ", ".join(f"PC{i}=0.0" for i in range(1, MAX_ATLAS_PCS + 1))
_pc_expr = "[" + ", ".join(f"PC{i}" for i in range(1, MAX_ATLAS_PCS + 1)) + "]"
_exec_src = (
    f"def sample(name='ATLAS', {_pc_sig}, hyperparameters=None):\n"
    f"    return generate_atlas_sample(name, hyperparameters or {{}}, {_pc_expr})\n"
)
_ns: dict = {"generate_atlas_sample": generate_atlas_sample}
exec(_exec_src, _ns)
sample = _ns["sample"]

__all__ = [
    "NAME",
    "sample",
    "HYPERPARAMETERS",
    "ORIENTATIONS",
    "MAX_ATLAS_PCS",
    "get_trait_parameters_with_defaults",
]
