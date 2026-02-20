"""
Origin manipulation helpers for shell objects.
"""

import bpy
from mathutils import Vector


def set_origin_at_location(obj, location):
    """
    Set the object's origin to the given world-space location via the cursor.
    Restores the cursor location after setting.

    Args:
        obj: Blender object (must be mesh)
        location: (x, y, z) in world space
    """
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    cursor_prev = bpy.context.scene.cursor.location.copy()
    bpy.context.scene.cursor.location = Vector(location)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.context.scene.cursor.location = cursor_prev
    bpy.context.view_layer.update()
