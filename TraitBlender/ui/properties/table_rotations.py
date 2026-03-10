"""
TraitBlender Table Rotation System

tb_rotation is a wrapper around the object's rotation_euler for use in table-based layouts.
"""

import bpy
from bpy.props import FloatVectorProperty


def _get_tb_rotation(self):
    """Getter for tb_rotation: returns the object's rotation_euler."""
    return self.rotation_euler


def _set_tb_rotation(self, value):
    """Setter for tb_rotation: assigns directly to rotation_euler."""
    self.rotation_euler = value


def register_table_rotations():
    """Register the tb_rotation property with all Blender objects."""
    bpy.types.Object.tb_rotation = FloatVectorProperty(
        name="Rotation",
        description="Object rotation (Euler angles) for table layout",
        size=3,
        subtype='EULER',
        get=_get_tb_rotation,
        set=_set_tb_rotation
    )
    print("TraitBlender: Table rotation property 'Object.tb_rotation' registered.")

def unregister_table_rotations():
    """Unregister the tb_rotation property."""
    if hasattr(bpy.types.Object, 'tb_rotation'):
        del bpy.types.Object.tb_rotation
        print("TraitBlender: Table rotation property 'Object.tb_rotation' unregistered.") 