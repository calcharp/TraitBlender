"""
Register the unified TraitBlender config on Blender's Scene.
"""

import bpy
from .config_subsection_register import CONFIG
from ..traitblender_config import TraitBlenderConfig


def config_register():
    """Build and register the unified config class with all sections."""
    dyn_class = type(
        "TraitBlenderConfig",
        (TraitBlenderConfig,),
        {"__annotations__": CONFIG}
    )
    bpy.utils.register_class(dyn_class)
    bpy.types.Scene.traitblender_config = bpy.props.PointerProperty(type=dyn_class)
    print("TraitBlenderConfig registered")
