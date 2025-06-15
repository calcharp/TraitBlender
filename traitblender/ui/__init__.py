"""
TraitBlender UI Module

Contains all user interface components including operators and panels.
"""

# Don't import submodules explicitly to avoid exposing them globally
# Import specific classes only when needed
from .operators import (
    TRAITBLENDER_OT_setup_scene,
    TRAITBLENDER_OT_set_camera_type,
    TRAITBLENDER_OT_set_camera_lens,
    TRAITBLENDER_OT_set_camera_lens_unit,
    TRAITBLENDER_OT_set_camera_shift,
    TRAITBLENDER_OT_set_camera_clip,
    TRAITBLENDER_OT_set_camera_sensor,
    TRAITBLENDER_OT_camera_render,
    TRAITBLENDER_OT_register_config,
)
from .panels import (
    TRAITBLENDER_PT_main_panel,
    TRAITBLENDER_PT_camera_panel,
)

__all__ = [
    # Operators
    "TRAITBLENDER_OT_setup_scene",
    "TRAITBLENDER_OT_set_camera_type",
    "TRAITBLENDER_OT_set_camera_lens",
    "TRAITBLENDER_OT_set_camera_lens_unit",
    "TRAITBLENDER_OT_set_camera_shift",
    "TRAITBLENDER_OT_set_camera_clip",
    "TRAITBLENDER_OT_set_camera_sensor",
    "TRAITBLENDER_OT_camera_render",
    "TRAITBLENDER_OT_register_config",
    # Panels
    "TRAITBLENDER_PT_main_panel",
    "TRAITBLENDER_PT_camera_panel",
]
