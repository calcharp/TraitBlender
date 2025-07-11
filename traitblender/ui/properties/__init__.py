import bpy
from . import setup_properties
from . import tb_coords

classes = [
    setup_properties.TraitBlenderSetupProperties,
]


def register():
    r_classes = classes
    for cls in r_classes:
        bpy.utils.register_class(cls)
    # Create the scene property
    bpy.types.Scene.traitblender_setup = bpy.props.PointerProperty(type=setup_properties.TraitBlenderSetupProperties)
    # Register table coordinate properties
    tb_coords.register()


def unregister():
    # Remove the scene property
    del bpy.types.Scene.traitblender_setup
    r_classes = classes
    for cls in r_classes:
        bpy.utils.unregister_class(cls)
    # Unregister table coordinate properties
    tb_coords.unregister()

__all__ = ["register", "unregister", "tb_coords"]