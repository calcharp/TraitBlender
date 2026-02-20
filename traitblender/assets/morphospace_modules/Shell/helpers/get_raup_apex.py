"""
World-space apex computation for shell objects.
"""

import bpy
from mathutils import Vector


def get_raup_apex(shell):
    """
    World-space centroid of the first ring (apex) for a shell.
    The apex is the tip of the spiral; use as rotation pivot. Updates with object transform.

    Args:
        shell: Blender object or object name (str)

    Returns:
        tuple: (x, y, z) in world space, or (0, 0, 0) if not a valid shell
    """
    obj = bpy.data.objects.get(shell) if isinstance(shell, str) else shell
    if not obj:
        return (0.0, 0.0, 0.0)
    scene = bpy.context.scene
    if (
        not hasattr(scene, "traitblender_dataset")
        or not scene.traitblender_dataset
        or getattr(scene.traitblender_dataset, "sample", None) != obj.name
        or not hasattr(scene, "traitblender_sample")
        or not scene.traitblender_sample
        or not scene.traitblender_sample.props
    ):
        return (0.0, 0.0, 0.0)
    ppb = scene.traitblender_sample.props.raup_points_per_ring
    if not ppb or not hasattr(obj, "data") or obj.type != "MESH":
        return (0.0, 0.0, 0.0)
    mw = obj.matrix_world
    verts = obj.data.vertices
    if len(verts) < ppb:
        return (0.0, 0.0, 0.0)
    world_centroid = sum((mw @ verts[i].co for i in range(ppb)), Vector()) / ppb
    return (world_centroid.x, world_centroid.y, world_centroid.z)
