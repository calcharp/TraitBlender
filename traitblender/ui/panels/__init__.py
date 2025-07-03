"""
TraitBlender UI Panels

Contains all panel classes for the TraitBlender add-on.
Panels define the user interface layout and elements.
"""

import bpy

# Import all panel classes here
from .main_panel import TRAITBLENDER_PT_main_panel, TRAITBLENDER_PT_config_panel, TRAITBLENDER_PT_morphospaces_panel, TRAITBLENDER_PT_datasets_panel, TRAITBLENDER_PT_transforms_panel, TRAITBLENDER_PT_imaging_panel

classes = [
    TRAITBLENDER_PT_main_panel,
    TRAITBLENDER_PT_config_panel,
    TRAITBLENDER_PT_morphospaces_panel,
    TRAITBLENDER_PT_datasets_panel,
    TRAITBLENDER_PT_transforms_panel,
    TRAITBLENDER_PT_imaging_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

__all__ = [
    "TRAITBLENDER_PT_main_panel",
    "TRAITBLENDER_PT_config_panel",
    "TRAITBLENDER_PT_morphospaces_panel",
    "TRAITBLENDER_PT_datasets_panel",
    "TRAITBLENDER_PT_transforms_panel",
    "TRAITBLENDER_PT_imaging_panel",
    "register",
    "unregister",
] 

