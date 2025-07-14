"""
TraitBlender Origins Module

Contains functions for calculating different types of origins for Blender objects
in table coordinates. These origins can be used for positioning and orientation
calculations in the TraitBlender system.
"""

import bpy
import numpy as np
from mathutils import Vector
from .get_table_coords import world_to_table_coords


def _get_object_origin(obj):
    """
    Get the actual object origin in table coordinates.
    
    Args:
        obj (bpy.types.Object): The Blender object
        
    Returns:
        tuple: Table coordinates of the object's origin (x, y, z)
    """
    return world_to_table_coords(obj.location)


def _get_geometry_bounds_origin(obj):
    """
    Get the center of the object's bounding box in table coordinates.
    
    Args:
        obj (bpy.types.Object): The Blender object
        
    Returns:
        tuple: Table coordinates of the geometric center (x, y, z)
    """
    # Get the object's bounding box in world coordinates
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    
    # Calculate the center of the bounding box
    bbox_center = sum(bbox_corners, Vector()) / len(bbox_corners)
    
    # Convert to table coordinates
    return world_to_table_coords(bbox_center)


def _get_mean_origin(obj):
    """
    Get the mean position of all vertices relative to object origin in table coordinates.
    Ignores vertices with NaN or infinite coordinates and prints warnings with their indices.
    """
    if obj.type != 'MESH' or not obj.data.vertices:
        return (0.0, 0.0, 0.0)
    local_vertices = [vertex.co for vertex in obj.data.vertices]
    valid_vertices = []
    invalid_indices = []
    for i, v in enumerate(local_vertices):
        arr = np.array([v.x, v.y, v.z])
        if np.any(np.isnan(arr)) or np.any(np.isinf(arr)):
            invalid_indices.append(i)
        else:
            valid_vertices.append(v)
    if invalid_indices:
        print(f"[TraitBlender] Warning: Ignoring NaN/Inf vertices at indices: {invalid_indices} in object '{obj.name}' for mean origin calculation.")
    if not valid_vertices:
        print(f"[TraitBlender] Warning: All vertices are invalid in object '{obj.name}' for mean origin calculation.")
        return (0.0, 0.0, 0.0)
    mean_local = sum(valid_vertices, Vector()) / len(valid_vertices)
    mean_tb = Vector(world_to_table_coords(obj.matrix_world @ mean_local)) - Vector(world_to_table_coords(obj.location))
    arr_tb = np.array([mean_tb.x, mean_tb.y, mean_tb.z])
    if np.any(np.isnan(arr_tb)) or np.any(np.isinf(arr_tb)):
        print(f"[TraitBlender] Warning: Mean origin calculation resulted in NaN/Inf for object '{obj.name}'. Returning (0,0,0).")
        return (0.0, 0.0, 0.0)
    return mean_tb


def _get_median_origin(obj):
    """
    Get the median position of all vertices relative to object origin in table coordinates.
    Ignores vertices with NaN or infinite coordinates and prints warnings with their indices.
    """
    if obj.type != 'MESH' or not obj.data.vertices:
        return (0.0, 0.0, 0.0)
    local_vertices = [vertex.co for vertex in obj.data.vertices]
    valid_coords = []
    invalid_indices = []
    for i, v in enumerate(local_vertices):
        arr = np.array([v.x, v.y, v.z])
        if np.any(np.isnan(arr)) or np.any(np.isinf(arr)):
            invalid_indices.append(i)
        else:
            valid_coords.append(arr)
    if invalid_indices:
        print(f"[TraitBlender] Warning: Ignoring NaN/Inf vertices at indices: {invalid_indices} in object '{obj.name}' for median origin calculation.")
    if not valid_coords:
        print(f"[TraitBlender] Warning: All vertices are invalid in object '{obj.name}' for median origin calculation.")
        return (0.0, 0.0, 0.0)
    median_local = np.median(np.array(valid_coords), axis=0)
    median_vector = Vector(median_local)
    median_tb = Vector(world_to_table_coords(obj.matrix_world @ median_vector)) - Vector(world_to_table_coords(obj.location))
    arr_tb = np.array([median_tb.x, median_tb.y, median_tb.z])
    if np.any(np.isnan(arr_tb)) or np.any(np.isinf(arr_tb)):
        print(f"[TraitBlender] Warning: Median origin calculation resulted in NaN/Inf for object '{obj.name}'. Returning (0,0,0).")
        return (0.0, 0.0, 0.0)
    return median_tb


# Dictionary of origin calculation functions
PLACEMENT_LOCAL_ORIGINS_TB = {
    'OBJECT': _get_object_origin,
    'GEOM_BOUNDS': _get_geometry_bounds_origin,
    'MEAN': _get_mean_origin,
    'MEDIAN': _get_median_origin,
}

# Set of all non-redundant axis combinations (order doesn't matter)
LOCATION_SHIFT_AXES_TB = {
    'XY', 'X', 'Y', 'Z',     # XY first (default), then single axes
    'XZ', 'YZ', 'XYZ'        # Other combinations
} 