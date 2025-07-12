"""
Table-based coordinate properties for objects in Blender.
Adds table-relative coordinates to all objects.
"""

import bpy
from mathutils import Vector


# Unit scale factor to fix coordinate system mismatch
# Adjust this value if your table model uses different units than Blender
UNIT_SCALE_FACTOR = 0.01  # Change this to 0.01 if you want to scale down instead


def get_table_surface_offset(table=None):
    """Get the offset from table origin to table surface (halfway between vertices 2 and 5)."""
    if table is None:
        table = bpy.data.objects.get("Table")
    if table is None:
        return Vector((0, 0, 0))
    
    # Get the table's bounding box in world space
    bbox_corners = [table.matrix_world @ Vector(corner) for corner in table.bound_box]
    
    # Vertices 2 and 5 are the top corners of the bounding box
    # (assuming standard bounding box vertex order)
    vertex_2 = bbox_corners[2]  # Top front right
    vertex_5 = bbox_corners[5]  # Top back left
    
    # Surface point is halfway between these two vertices
    surface_point = (vertex_2 + vertex_5) / 2
    
    # Convert surface point to table local coordinates
    surface_local = table.matrix_world.inverted() @ surface_point
    
    return surface_local


def world_to_table_coords(world_pos, table=None):
    """Convert world coordinates to table local coordinates."""
    if table is None:
        table = bpy.data.objects.get("Table")
    if table is None:
        return Vector(world_pos)
    
    # Convert to table local coordinates
    table_local = table.matrix_world.inverted() @ Vector(world_pos)
    
    # Adjust for surface offset (subtract the surface offset to make surface Z=0)
    surface_offset = get_table_surface_offset(table)
    table_local -= surface_offset
    
    # Apply unit scale factor
    table_local *= UNIT_SCALE_FACTOR
    
    return table_local


def table_to_world_coords(table_pos, table=None):
    """Convert table local coordinates to world coordinates."""
    if table is None:
        table = bpy.data.objects.get("Table")
    if table is None:
        return Vector(table_pos)
    
    # Remove unit scale factor
    adjusted_table_pos = Vector(table_pos) / UNIT_SCALE_FACTOR
    
    # Add back the surface offset
    surface_offset = get_table_surface_offset(table)
    adjusted_table_pos += surface_offset
    
    # Convert to world coordinates
    return table.matrix_world @ adjusted_table_pos


def get_table_coords(self):
    """Get the object's position in table local coordinates."""
    try:
        table = bpy.data.objects.get("Table")
        world_pos = self.location
        return world_to_table_coords(world_pos, table)
    except Exception:
        return Vector((0, 0, 0))


def set_table_coords(self, value):
    """Set the object's position using table local coordinates."""
    try:
        table = bpy.data.objects.get("Table")
        world_pos = table_to_world_coords(value, table)
        self.location = world_pos
    except Exception as e:
        print(f"Error in set_table_coords: {e}")


def register():
    bpy.types.Object.table_coords = bpy.props.FloatVectorProperty(
        name="Table Coordinates",
        description="Position in table coordinate system (Z=0 at table surface, or world coordinates if no table exists)",
        default=(0.0, 0.0, 0.0),
        subtype='TRANSLATION',
        size=3,
        get=get_table_coords,
        set=set_table_coords
    )


def unregister():
    if hasattr(bpy.types.Object, 'table_coords'):
        del bpy.types.Object.table_coords 