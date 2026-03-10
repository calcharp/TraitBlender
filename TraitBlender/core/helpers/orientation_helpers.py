"""
Bake object rotation into mesh so rotation becomes (0,0,0).
Used at the end of each orientation so transforms work from an applied state.
"""

import bpy


def bake_rotation_to_mesh(object_name):
    """
    Apply the object's current rotation to its mesh data and set rotation to (0,0,0).
    The object keeps the same visual pose; later transforms use the applied orientation as base.

    Args:
        object_name: Name of the Blender object (str).

    Returns:
        bool: True if apply succeeded, False if object not found or apply failed.
    """
    obj = bpy.data.objects.get(object_name)
    if obj is None:
        return False
    if obj.type != 'MESH':
        return False
    try:
        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(rotation=True)
        bpy.context.view_layer.update()
        return True
    except Exception:
        return False
