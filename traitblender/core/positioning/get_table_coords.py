import bpy
from mathutils import Vector

# Indices for the top face corners of the Table's bounding box
CORNERS = [1, 2, 5, 6]


def get_depsgraph():
    """
    Retrieve the current evaluated dependency graph to get up-to-date transforms.
    """
    return bpy.context.evaluated_depsgraph_get()


def get_table_top_center():
    """
    Compute the world-space center of the Table's top face using evaluated data.
    """
    table = bpy.data.objects.get('Table')
    if not table:
        raise RuntimeError("Table object not found in the scene.")
    depsgraph = get_depsgraph()
    table_eval = table.evaluated_get(depsgraph)
    mw = table_eval.matrix_world
    bb = table_eval.bound_box
    pts = [mw @ Vector(bb[i]) for i in CORNERS]
    return sum(pts, Vector()) / len(pts)


def z_dist_to_lowest(obj):
    """
    Distance from an object's origin to its lowest vertex (or 0 for non-meshs), using evaluated data.
    """
    if not hasattr(obj, 'data') or not hasattr(obj.data, 'vertices'):
        return 0.0
    depsgraph = get_depsgraph()
    obj_eval = obj.evaluated_get(depsgraph)
    mw = obj_eval.matrix_world
    origin_z = mw.to_translation().z
    lowest_z = min((mw @ v.co).z for v in obj_eval.data.vertices)
    return origin_z - lowest_z


def world_to_table_coords(world_point, precision=4):
    """
    Convert a world-space point to the Table's local coordinate system (tb_coords).

    Args:
        world_point (Vector): A mathutils.Vector in world-space.
        precision (int): Decimal places for rounding to reduce floating errors.
    Returns:
        tuple: (x, y, z) rounded to `precision` decimals in table-local axes.
    """
    depsgraph = get_depsgraph()
    table = bpy.data.objects.get('Table')
    if not table:
        raise RuntimeError("Table object not found in the scene.")
    table_eval = table.evaluated_get(depsgraph)
    rot = table_eval.matrix_world.to_quaternion().to_matrix()
    top_center = get_table_top_center()

    world_dir = world_point - top_center
    local = rot.inverted() @ world_dir

    return (round(local.x, precision),
            round(local.y, precision),
            round(local.z, precision))





def get_table_axes_coords(length=1.0, precision=4):
    """
    Return a dictionary of the table's local XYZ axis endpoints, expressed in table-local coordinates.

    Args:
        length (float): Length along each axis from the top-center to sample.
        precision (int): Decimal places for rounding.
    Returns:
        dict: {'x': (x, y, z), 'y': ..., 'z': ...}
    """
    depsgraph = get_depsgraph()
    table = bpy.data.objects.get('Table')
    if not table:
        raise RuntimeError("Table object not found in the scene.")
    table_eval = table.evaluated_get(depsgraph)
    rot = table_eval.matrix_world.to_quaternion().to_matrix()
    top_center = get_table_top_center()

    axes_world = {
        'x': top_center + rot.col[0] * length,
        'y': top_center + rot.col[1] * length,
        'z': top_center + rot.col[2] * length,
    }

    # include lift for each axis (if needed, using z_dist_to_lowest on a sample object)
    return {
        axis: world_to_table_coords(pt, precision)
        for axis, pt in axes_world.items()
    }


