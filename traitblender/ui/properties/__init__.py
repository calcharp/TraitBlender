import bpy
from . import setup_properties
from . import orientation_properties
from . import sample_properties
from . import tb_location
from . import table_rotations
from . import morphospace_hyperparams

classes = [
    setup_properties.TraitBlenderSetupProperties,
    orientation_properties.TRAITBLENDER_PG_orientation,
    sample_properties.TRAITBLENDER_PG_sample_props,
    sample_properties.TRAITBLENDER_PG_sample,
]


def register():
    r_classes = classes
    for cls in r_classes:
        bpy.utils.register_class(cls)
    # Create the scene properties
    bpy.types.Scene.traitblender_setup = bpy.props.PointerProperty(type=setup_properties.TraitBlenderSetupProperties)
    bpy.types.Scene.traitblender_orientation = bpy.props.PointerProperty(type=orientation_properties.TRAITBLENDER_PG_orientation)
    bpy.types.Scene.traitblender_sample = bpy.props.PointerProperty(type=sample_properties.TRAITBLENDER_PG_sample)
    # Hyperparam editors are built lazily when morphospaces panel is first drawn
    # Register table location properties
    tb_location.register_tb_location()
    # Register table rotation properties
    table_rotations.register_table_rotations()


def unregister():
    morphospace_hyperparams.unbuild_hyperparam_editors()
    # Remove the scene properties
    del bpy.types.Scene.traitblender_sample
    del bpy.types.Scene.traitblender_orientation
    del bpy.types.Scene.traitblender_setup
    r_classes = classes
    for cls in r_classes:
        bpy.utils.unregister_class(cls)
    # Unregister table location properties
    tb_location.unregister_tb_location()
    # Unregister table rotation properties
    table_rotations.unregister_table_rotations()

__all__ = ["register", "unregister"]