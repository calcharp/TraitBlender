"""
TraitBlender core mesh utilities (3D exports).
"""

import os
import bpy

from .export_registry import EXPORTERS, export_type_items


def export_current_sample(*, filepath: str, export_type: str | None = None, context=None, **options) -> dict:
    """
    Export the current sample (by name) to a mesh file.

    - Sample is referenced by the string name in `scene.traitblender_dataset.sample`.
    - Export type defaults to `scene.traitblender_config.meshes.file_export_type` if not provided.
    """
    ctx = context or bpy.context
    scene = ctx.scene

    sample_name = getattr(scene.traitblender_dataset, "sample", None)
    if not sample_name or sample_name == "NONE":
        raise RuntimeError("No sample selected to export.")

    cfg_type = None
    try:
        cfg_type = scene.traitblender_config.meshes.file_export_type
    except Exception:
        cfg_type = None

    etype = (export_type or cfg_type or "").lower().strip()
    if not etype:
        raise RuntimeError("No mesh export type selected.")

    exporter = EXPORTERS.get(etype)
    if exporter is None:
        raise RuntimeError(f"Unsupported mesh export type: '{etype}'. Supported: {sorted(EXPORTERS.keys())}")

    # If filepath has no extension, append based on type for convenience
    base, ext = os.path.splitext(filepath)
    out_path = filepath if ext else f"{filepath}.{etype}"

    return exporter(object_name=sample_name, filepath=out_path, **options)


__all__ = [
    "EXPORTERS",
    "export_type_items",
    "export_current_sample",
]

