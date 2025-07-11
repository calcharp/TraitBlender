"""
Table-based coordinate properties for objects in Blender.
Adds both metric and normalized ([-1,1]) table-relative coordinates to all objects.
Lowest vertex placement logic included.
"""

import bpy
from mathutils import Vector


def get_table_coordinate_system():
    table = bpy.data.objects.get("Table")
    if not table:
        return None
    table_matrix = table.matrix_world
    bbox = [Vector(corner) for corner in table.bound_box]
    max_z = max(corner.z for corner in bbox)
    top_corners_local = [corner for corner in bbox if abs(corner.z - max_z) < 1e-5]
    origin = sum((table_matrix @ corner for corner in top_corners_local), Vector()) / len(top_corners_local)
    z_axis = (table_matrix @ Vector((0, 0, 1))) - (table_matrix @ Vector((0, 0, 0)))
    z_axis.normalize()
    x_axis = (table_matrix @ Vector((1, 0, 0))) - (table_matrix @ Vector((0, 0, 0)))
    x_axis.normalize()
    y_axis = z_axis.cross(x_axis)
    y_axis.normalize()
    x_axis = y_axis.cross(z_axis)
    x_axis.normalize()
    from mathutils import Matrix
    coord_matrix = Matrix.Identity(4)
    coord_matrix.col[0] = Vector((x_axis.x, x_axis.y, x_axis.z, 0))
    coord_matrix.col[1] = Vector((y_axis.x, y_axis.y, y_axis.z, 0))
    coord_matrix.col[2] = Vector((z_axis.x, z_axis.y, z_axis.z, 0))
    coord_matrix.col[3] = Vector((origin.x, origin.y, origin.z, 1))
    return coord_matrix


def get_object_lowest_vertex_z(obj):
    if obj.type == 'MESH' and obj.data.vertices:
        return min((obj.matrix_world @ v.co).z for v in obj.data.vertices)
    return min((obj.matrix_world @ Vector(corner)).z for corner in obj.bound_box)


def world_to_table_coords(world_pos, coord_matrix):
    if coord_matrix is None:
        return Vector((0, 0, 0))
    from mathutils import Vector
    local_pos = coord_matrix.inverted() @ Vector((world_pos.x, world_pos.y, world_pos.z, 1))
    return Vector((local_pos.x, local_pos.y, local_pos.z))


def table_to_world_coords(table_pos, coord_matrix):
    if coord_matrix is None:
        return Vector((0, 0, 0))
    from mathutils import Vector
    world_pos = coord_matrix @ Vector((table_pos.x, table_pos.y, table_pos.z, 1))
    return Vector((world_pos.x, world_pos.y, world_pos.z))


def get_table_coords(self):
    bpy.context.view_layer.update()
    coord_matrix = get_table_coordinate_system()
    world_pos = self.location
    return world_to_table_coords(world_pos, coord_matrix)


def set_table_coords(self, value):
    bpy.context.view_layer.update()
    coord_matrix = get_table_coordinate_system()
    world_pos = table_to_world_coords(Vector(value), coord_matrix)
    lowest_z = get_object_lowest_vertex_z(self)
    offset = world_pos.z - lowest_z
    adjusted_world_pos = Vector((world_pos.x, world_pos.y, self.location.z + offset))
    self.location = adjusted_world_pos


def get_table_coords_norm(self):
    bpy.context.view_layer.update()
    table = bpy.data.objects.get("Table")
    if not table:
        return Vector((0, 0, 0))
    local_pos = table.matrix_world.inverted() @ self.location
    bbox = [Vector(corner) for corner in table.bound_box]
    min_x = min(corner.x for corner in bbox)
    max_x = max(corner.x for corner in bbox)
    min_y = min(corner.y for corner in bbox)
    max_y = max(corner.y for corner in bbox)
    norm_x = 2 * (local_pos.x - min_x) / (max_x - min_x) - 1 if max_x != min_x else 0
    norm_y = 2 * (local_pos.y - min_y) / (max_y - min_y) - 1 if max_y != min_y else 0
    max_z = max(corner.z for corner in bbox)
    norm_z = local_pos.z - max_z
    return Vector((norm_x, norm_y, norm_z))


def set_table_coords_norm(self, value):
    bpy.context.view_layer.update()
    table = bpy.data.objects.get("Table")
    if not table:
        return
    bbox = [Vector(corner) for corner in table.bound_box]
    min_x = min(corner.x for corner in bbox)
    max_x = max(corner.x for corner in bbox)
    min_y = min(corner.y for corner in bbox)
    max_y = max(corner.y for corner in bbox)
    max_z = max(corner.z for corner in bbox)
    local_x = min_x + (value[0] + 1) * (max_x - min_x) / 2
    local_y = min_y + (value[1] + 1) * (max_y - min_y) / 2
    local_z = max_z + value[2]
    local_pos = Vector((local_x, local_y, local_z))
    world_pos = table.matrix_world @ local_pos
    lowest_z = get_object_lowest_vertex_z(self)
    offset = world_pos.z - lowest_z
    adjusted_world_pos = Vector((world_pos.x, world_pos.y, self.location.z + offset))
    self.location = adjusted_world_pos


def register():
    bpy.types.Object.table_coords = bpy.props.FloatVectorProperty(
        name="Table Coordinates",
        description="Position in table coordinate system (origin at table top center, Z is table normal)",
        default=(0.0, 0.0, 0.0),
        subtype='TRANSLATION',
        size=3,
        get=get_table_coords,
        set=set_table_coords,
        update=lambda self, context: None
    )
    bpy.types.Object.table_coords_norm = bpy.props.FloatVectorProperty(
        name="Table Coordinates (Normalized)",
        description="Position in normalized table coordinate system (-1 to 1 on X/Y, meters on Z)",
        default=(0.0, 0.0, 0.0),
        subtype='TRANSLATION',
        size=3,
        get=get_table_coords_norm,
        set=set_table_coords_norm,
        update=lambda self, context: None
    )

def unregister():
    if hasattr(bpy.types.Object, 'table_coords'):
        del bpy.types.Object.table_coords
    if hasattr(bpy.types.Object, 'table_coords_norm'):
        del bpy.types.Object.table_coords_norm 