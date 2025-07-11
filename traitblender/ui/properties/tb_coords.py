"""
Table-based coordinate properties for objects in Blender.
Adds table-relative coordinates to all objects in units of meters.
Lowest vertex placement logic included.
"""

import bpy
from mathutils import Vector, Matrix


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
    local_pos = coord_matrix.inverted() @ Vector((world_pos.x, world_pos.y, world_pos.z, 1))
    return Vector((local_pos.x, local_pos.y, local_pos.z))


def table_to_world_coords(table_pos, coord_matrix):
    if coord_matrix is None:
        return Vector((0, 0, 0))
    world_pos = coord_matrix @ Vector((table_pos.x, table_pos.y, table_pos.z, 1))
    return Vector((world_pos.x, world_pos.y, world_pos.z))


def get_table_coords(self):
    try:
        # Try to update the view layer, but handle potential errors
        try:
            bpy.context.view_layer.update()
        except Exception:
            pass  # Ignore view layer update errors
        
        coord_matrix = get_table_coordinate_system()
        world_pos = self.location
        
        return world_to_table_coords(world_pos, coord_matrix)
    except Exception:
        # Return default coordinates if anything goes wrong
        return Vector((0, 0, 0))


def set_table_coords(self, value):
    try:
        # Try to update the view layer, but handle potential errors
        try:
            bpy.context.view_layer.update()
        except Exception:
            pass  # Ignore view layer update errors
        
        coord_matrix = get_table_coordinate_system()
        
        # Ensure value is a valid Vector
        if isinstance(value, (list, tuple)):
            table_pos = Vector(value)
        else:
            table_pos = value
        
        world_pos = table_to_world_coords(table_pos, coord_matrix)
        
        try:
            lowest_z = get_object_lowest_vertex_z(self)
            offset = world_pos.z - lowest_z
            adjusted_world_pos = Vector((world_pos.x, world_pos.y, self.location.z + offset))
            self.location = adjusted_world_pos
        except Exception:
            # If we can't calculate the offset, just set the position directly
            self.location = world_pos
    except Exception:
        # If anything goes wrong, just set the location to the world position
        try:
            if coord_matrix is not None:
                world_pos = table_to_world_coords(Vector(value), coord_matrix)
                if world_pos is not None:
                    self.location = world_pos
        except Exception:
            pass  # Final fallback - do nothing


def register():
    bpy.types.Object.table_coords = bpy.props.FloatVectorProperty(
        name="Table Coordinates",
        description="Position in table coordinate system (origin at table top center, Z is table normal) in meters",
        default=(0.0, 0.0, 0.0),
        subtype='TRANSLATION',
        size=3,
        get=get_table_coords,
        set=set_table_coords,
        update=lambda self, context: None
    )

def unregister():
    if hasattr(bpy.types.Object, 'table_coords'):
        del bpy.types.Object.table_coords 