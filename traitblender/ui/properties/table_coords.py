"""
TraitBlender Table Coordinates System

Provides relative positioning system for objects relative to the Table's top surface.
Allows easy placement of specimens and objects on the museum table.
"""

import bpy
from mathutils import Vector
from bpy.props import FloatVectorProperty

# Corner indices for the top face of the Table's bounding box
CORNERS = [1, 2, 5, 6]

def z_dist_to_lowest(obj):
    """
    Calculate the distance from an object's origin to its lowest vertex.
    For non-mesh objects (camera, light, etc.), returns 0.
    
    Args:
        obj: Blender object
        
    Returns:
        float: Distance from origin to lowest point, or 0 for non-mesh objects
    """
    # Check if object has mesh data with vertices
    if not hasattr(obj, 'data') or not hasattr(obj.data, 'vertices'):
        return 0.0
    
    mw = obj.matrix_world
    origin_z = mw.to_translation().z
    lowest_z = min((mw @ v.co).z for v in obj.data.vertices)
    return origin_z - lowest_z

def _get_tb_coords(self):
    """
    Getter for tb_coords property.
    Returns the object's position relative to Table's top face center in unit local axes.
    """
    table = bpy.data.objects.get('Table')
    if not table or self is table:
        return (0.0, 0.0, 0.0)
    
    mw_ref = table.matrix_world
    bb = table.bound_box

    # Get pure rotation matrix (unit axes)
    rot = mw_ref.to_quaternion().to_matrix()

    # Compute world-space top-face center
    pts = [mw_ref @ Vector(bb[i]) for i in CORNERS]
    top_center = sum(pts, Vector()) / len(pts)

    # Account for object's own bottom lift
    dz = z_dist_to_lowest(self)

    # World-space vector from top_center+lift to our origin
    world_dir = self.location - (top_center + Vector((0, 0, dz)))

    # Convert back into Table's *unit* local axes
    local = rot.inverted() @ world_dir
    return (local.x, local.y, local.z)

def _set_tb_coords(self, value):
    """
    Setter for tb_coords property.
    Sets the object's position relative to Table's top face center.
    
    Args:
        value: Tuple of (x, y, z) coordinates in Table's local space
    """
    table = bpy.data.objects.get('Table')
    if not table or self is table:
        return
    
    mw_ref = table.matrix_world
    bb = table.bound_box

    rot = mw_ref.to_quaternion().to_matrix()

    pts = [mw_ref @ Vector(bb[i]) for i in CORNERS]
    top_center = sum(pts, Vector()) / len(pts)

    # Apply *unit* local offset
    offset_world = rot @ Vector(value)

    dz = z_dist_to_lowest(self)
    self.location = top_center + offset_world + Vector((0, 0, dz))

def register_table_coords():
    """Register the tb_coords property with all Blender objects."""
    bpy.types.Object.tb_coords = FloatVectorProperty(
        name="Table Coordinates",
        description="Position relative to Table's top face center in unit local axes",
        size=3,
        subtype='TRANSLATION',
        get=_get_tb_coords,
        set=_set_tb_coords
    )
    print("TraitBlender: Table coordinates property 'Object.tb_coords' registered.")

def unregister_table_coords():
    """Unregister the tb_coords property."""
    if hasattr(bpy.types.Object, 'tb_coords'):
        del bpy.types.Object.tb_coords
        print("TraitBlender: Table coordinates property 'Object.tb_coords' unregistered.") 