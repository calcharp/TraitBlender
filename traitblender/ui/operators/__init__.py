"""
TraitBlender UI Operators

Contains all operator classes for the TraitBlender add-on.
Operators handle user actions and commands.
"""

import bpy

# Scene Setup Operators
from .setup_scene_operator import TRAITBLENDER_OT_setup_scene
from .clear_scene_operator import TRAITBLENDER_OT_clear_scene

### Configuration Operators
from .configure_traitblender import (
    TRAITBLENDER_OT_configure_scene,
    TRAITBLENDER_OT_show_configuration,
    TRAITBLENDER_OT_export_config
)

### Transform Operators
from .transforms_operators import (
    TRAITBLENDER_OT_run_pipeline,
    TRAITBLENDER_OT_undo_pipeline,
)

classes = [
    TRAITBLENDER_OT_setup_scene,
    TRAITBLENDER_OT_clear_scene,
    TRAITBLENDER_OT_configure_scene,
    TRAITBLENDER_OT_show_configuration,
    TRAITBLENDER_OT_export_config,
    TRAITBLENDER_OT_run_pipeline,
    TRAITBLENDER_OT_undo_pipeline,
]


def register():
    r_classes = classes
    for cls in r_classes:
        bpy.utils.register_class(cls)

def unregister():
    r_classes = classes
    for cls in r_classes:
        bpy.utils.unregister_class(cls)
    
__all__ = ["register", "unregister"] 