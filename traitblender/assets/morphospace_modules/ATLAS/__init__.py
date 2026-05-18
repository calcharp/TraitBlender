"""
ATLAS morphospace: template-centered PCA on dense correspondences + Local RBF warp.

Traits ``pc1`` … ``pcK`` are σ-multiples (ATLAS DATABASE sliders). Reconstruction:
``target = template_dense + Σ z_i √(λ_i) mode_i``, then Local RBF mesh warp (LPS/RAS aware).
"""

from __future__ import annotations

from .morphospace import MAX_ATLAS_PCS, generate_atlas_sample
from .orientations import ORIENTATIONS

NAME = "ATLAS"

HYPERPARAMETERS = {
    "database_dir": "",
    "n_components": 10,
    # traits are σ-multiples (same as ATLAS DATABASE / ATLASViewer sliders)
    "pc_parameterization": "zscore",
    # template PLY is typically LPS; convert for RBF then back (ShapeCommons exports)
    "mesh_from_lps": True,
    # uniform scale applied to deformed vertices after warp
    "scale": 1.0,
}


def get_trait_parameters_with_defaults(merged_hyperparameters):
    """``pc1`` … ``pc{n_components}`` for dataset columns (capped at ``MAX_ATLAS_PCS``)."""
    n = int(merged_hyperparameters.get("n_components", HYPERPARAMETERS["n_components"]))
    n = max(0, min(n, MAX_ATLAS_PCS))
    return {f"pc{i}": 0.0 for i in range(1, n + 1)}


_pc_sig = ", ".join(f"pc{i}=0.0" for i in range(1, MAX_ATLAS_PCS + 1))
_pc_expr = "[" + ", ".join(f"pc{i}" for i in range(1, MAX_ATLAS_PCS + 1)) + "]"
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
