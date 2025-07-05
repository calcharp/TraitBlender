"""
TraitBlender Datasets Module

Contains dataset management functionality for TraitBlender.
"""

import bpy
from . import traitblender_dataset

classes = [
    traitblender_dataset.TRAITBLENDER_PG_dataset,
]


def register():
    r_classes = classes
    for cls in r_classes:
        bpy.utils.register_class(cls)
    
    # Create the scene property
    bpy.types.Scene.traitblender_dataset = bpy.props.PointerProperty(type=traitblender_dataset.TRAITBLENDER_PG_dataset)


def unregister():
    # Remove the scene property
    del bpy.types.Scene.traitblender_dataset
    
    r_classes = classes
    for cls in r_classes:
        bpy.utils.unregister_class(cls)


__all__ = ["register", "unregister"] 