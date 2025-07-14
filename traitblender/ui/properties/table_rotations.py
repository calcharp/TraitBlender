"""
TraitBlender Table Rotation System

Provides rotation system for objects around their bottom-center pivot.
Allows easy rotation of specimens and objects while maintaining proper pivot points.
"""

import bpy
import math
from mathutils import Matrix, Vector, Euler
from bpy.props import FloatVectorProperty

def rotate_around_bottom_center(obj, rotvec):
    """
    Rotate obj around its bottom-center pivot by the axis-angle vector rotvec,
    adjusted by computing the true delta via quaternions, and including any
    'Table' object's rotation.
    """
    # compute bottom-center pivot in world space
    local_verts = [Vector(v) for v in obj.bound_box]
    lowest_z = min(v.z for v in local_verts)
    pivot_local = Vector((0.0, 0.0, lowest_z))
    pivot_world = obj.matrix_world @ pivot_local

    # combine user rotation with table rotation (if present)
    total_rot = Vector(rotvec)
    if 'Table' in bpy.data.objects:
        total_rot += Vector(bpy.data.objects['Table'].rotation_euler)

    # compute true rotation delta via quaternions
    q_target  = Euler(total_rot, obj.rotation_mode).to_quaternion()
    q_current = obj.rotation_euler.to_quaternion()
    q_delta   = q_target @ q_current.inverted()
    if q_delta.angle == 0:
        return
    axis      = q_delta.axis
    angle_rad = q_delta.angle

    # build and apply the transform
    to_origin = Matrix.Translation(-pivot_world)
    rot_mat   = Matrix.Rotation(angle_rad, 4, axis)
    back      = Matrix.Translation(pivot_world)
    obj.matrix_world = back @ rot_mat @ to_origin @ obj.matrix_world

def _get_tb_rotation(self):
    """
    Getter for tb_rotation property.
    Returns the object's current rotation euler angles.
    """
    return self.rotation_euler

def _set_tb_rotation(self, value):
    """
    Setter for tb_rotation property.
    Applies rotation around the object's bottom-center pivot.
    
    Args:
        value: Tuple of (x, y, z) rotation angles in radians
    """
    # apply the bottom-center rotation
    rotate_around_bottom_center(self, value)
    # sync Euler to the new world matrix so no drift remains
    self.rotation_euler = self.matrix_world.to_euler(self.rotation_mode)

def register_table_rotations():
    """Register the tb_rotation property with all Blender objects."""
    bpy.types.Object.tb_rotation = FloatVectorProperty(
        name="Rotation from Bottom",
        description="Rotation around object's bottom-center pivot",
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