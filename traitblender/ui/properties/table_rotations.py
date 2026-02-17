"""
TraitBlender Table Rotation System

Provides rotation around object pivot: apex (first ring) for Raup shells,
bottom-center of bounding box for other objects.
"""

import bpy
import math
from mathutils import Matrix, Vector, Euler
from bpy.props import FloatVectorProperty

def _get_rotation_pivot_world(obj):
    """
    Get the rotation pivot in world space.
    For Raup shells (raup_points_per_ring), use the apex (first ring centroid).
    Otherwise use bottom-center of bounding box.
    """
    ppb = obj.get("raup_points_per_ring")
    if ppb and hasattr(obj, "data") and obj.type == "MESH":
        verts = obj.data.vertices
        if len(verts) >= ppb:
            mw = obj.matrix_world
            pivot_world = sum((mw @ verts[i].co for i in range(ppb)), Vector()) / ppb
            return pivot_world
    local_verts = [Vector(v) for v in obj.bound_box]
    lowest_z = min(v.z for v in local_verts)
    pivot_local = Vector((0.0, 0.0, lowest_z))
    return obj.matrix_world @ pivot_local


def rotate_around_bottom_center(obj, rotvec):
    """
    Rotate obj around its pivot (apex for Raup shells, bottom-center otherwise)
    by the axis-angle vector rotvec, adjusted via quaternions and Table rotation.
    """
    pivot_world = _get_rotation_pivot_world(obj)

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
    Applies rotation around the object's pivot (apex for Raup shells, bottom-center otherwise).
    
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
        description="Rotation around object's pivot (apex for shells, bottom-center otherwise)",
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