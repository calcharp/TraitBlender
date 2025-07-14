import bpy
from . import setup_properties
from . import table_coords
from . import table_rotations

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
    table_coords.register_table_coords()
    # Register table rotation properties
    table_rotations.register_table_rotations()


def unregister():
    # Remove the scene property
    del bpy.types.Scene.traitblender_setup
    r_classes = classes
    for cls in r_classes:
        bpy.utils.unregister_class(cls)
    # Unregister table coordinate properties
    table_coords.unregister_table_coords()
    # Unregister table rotation properties
    table_rotations.unregister_table_rotations()

__all__ = ["register", "unregister"]