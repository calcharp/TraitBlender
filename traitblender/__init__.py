"""
TraitBlender - Blender Add-on for Generating Museum-Style Morphological Images

Main add-on initialization file.
"""

import bpy

# Import UI components
from .ui.operators import TRAITBLENDER_OT_setup_scene

# List of all classes to register
classes = [
    TRAITBLENDER_OT_setup_scene,
]


def register():
    """Register all add-on classes"""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister all add-on classes"""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
