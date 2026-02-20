"""
Orientation functions for shell objects.
"""

import bpy
import math
from ..helpers import get_raup_apex, set_origin_at_location


def _orient_default(sample_obj):
    """
    Default orientation: set origin to apex, center on table, rotate by -t so all apertures align.
    t is the spiral parameter (radians) from the morphospace; the aperture
    position correlates with t, so rotating by -t brings them to a common orientation.
    """
    apex_world = get_raup_apex(sample_obj)
    if apex_world != (0.0, 0.0, 0.0):
        set_origin_at_location(sample_obj, apex_world)

    sample_obj.tb_location = (0.0, 0.0, 0.0)

    t_val = 0
    try:
        dataset = bpy.context.scene.traitblender_dataset
        row = dataset.loc(sample_obj.name)
        for col in row.index:
            if str(col).lower().strip() == "t":
                t_val = float(row[col])
                break
    except (KeyError, TypeError, ValueError, AttributeError):
        pass

    # Use modulo 2π so apertures align regardless of how many whorls (t can be 20+ radians)
    rotation_z = (t_val % (math.pi*2)) + 1.4*math.pi
    sample_obj.tb_rotation = (0.0, 0.0, rotation_z)

    bpy.context.view_layer.objects.active = sample_obj
    sample_obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

    # Ensure centered on table after rotation
    sample_obj.tb_location = (0.0, 0.0, 0.0)
    bpy.context.view_layer.update()


def _orient_geometric_center_xflipped(sample_obj):
    """
    Default orientation plus 180° flip on X. Simple rotation add.
    """
    _orient_default(sample_obj)

    bpy.context.view_layer.objects.active = sample_obj
    sample_obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

    sample_obj.tb_rotation.x += math.pi
    sample_obj.tb_rotation.z -= math.pi/2

    bpy.context.view_layer.objects.active = sample_obj
    sample_obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

    # Ensure centered on table after rotation
    sample_obj.tb_location = (0.0, 0.0, 0.0)
    bpy.context.view_layer.update()
