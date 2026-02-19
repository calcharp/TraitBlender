"""
TraitBlender Table Location System

Provides relative positioning system for objects relative to the Table's top surface.
Allows easy placement of specimens and objects on the museum table.
"""

import bpy
from mathutils import Vector
from bpy.props import FloatVectorProperty

# Corner indices for the top face of the Table's bounding box
CORNERS = [1, 2, 5, 6]

def _get_bottom_center_world(obj):
    """
    World-space point: geometric center of bounding box with Z projected to the lowest point.
    bound_box is in local space; we transform to world via matrix_world.
    """
    mw = obj.matrix_world
    pts = [mw @ Vector(c) for c in obj.bound_box]
    center = sum(pts, Vector()) / len(pts)
    lowest_z = min(p.z for p in pts)
    return Vector((center.x, center.y, lowest_z))


def _get_tb_location(self):
    """
    Getter for tb_location property.
    Returns the object's bottom-center (bbox center projected to bottom) relative to
    Table's top face center, in unit local axes.
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

    # Object's bottom-center in world space (bbox center projected to lowest Z)
    bottom_center = _get_bottom_center_world(self)

    # Vector from table top center to object's bottom-center
    world_dir = bottom_center - top_center

    # Convert to Table's unit local axes
    local = rot.inverted() @ world_dir
    return (local.x, local.y, local.z)

def _set_tb_location(self, value):
    """
    Setter for tb_location property.
    Places the object so its bottom-center (bbox center projected to bottom) is at
    the given coordinates relative to Table's top face center.
    
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

    target_bottom_center = top_center + rot @ Vector(value)
    current_bottom_center = _get_bottom_center_world(self)
    self.location += target_bottom_center - current_bottom_center

def register_tb_location():
    """Register the tb_location property with all Blender objects."""
    bpy.types.Object.tb_location = FloatVectorProperty(
        name="Table Location",
        description="Position relative to Table's top face center in unit local axes",
        size=3,
        subtype='TRANSLATION',
        get=_get_tb_location,
        set=_set_tb_location
    )
    print("TraitBlender: Table location property 'Object.tb_location' registered.")

def unregister_tb_location():
    """Unregister the tb_location property."""
    if hasattr(bpy.types.Object, 'tb_location'):
        del bpy.types.Object.tb_location
        print("TraitBlender: Table location property 'Object.tb_location' unregistered.")
