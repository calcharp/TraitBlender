import bpy
from . import setup_properties

classes = [
    setup_properties.TraitBlenderSetupProperties,
]


def register():
    r_classes = classes
    for cls in r_classes:
        bpy.utils.register_class(cls)
    
    # Create the scene property
    bpy.types.Scene.traitblender_setup = bpy.props.PointerProperty(type=setup_properties.TraitBlenderSetupProperties)


def unregister():
    # Remove the scene property
    del bpy.types.Scene.traitblender_setup
    
    r_classes = classes
    for cls in r_classes:
        bpy.utils.unregister_class(cls)

__all__ = ["register", "unregister"]