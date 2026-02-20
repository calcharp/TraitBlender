"""
Clear scene helper.

Helper functions for clearing and cleaning Blender scenes.
"""

import bpy


def clear_scene(include_materials=True, include_meshes=True, include_curves=True, include_lights=True, include_cameras=True):
    """
    Clear all objects and data from the current Blender scene.
    
    Args:
        include_materials (bool): Whether to remove all materials (default: True)
        include_meshes (bool): Whether to remove all mesh data (default: True)
        include_curves (bool): Whether to remove all curve data (default: True)
        include_lights (bool): Whether to remove all light data (default: True)
        include_cameras (bool): Whether to remove all camera data (default: True)
    
    Returns:
        dict: Dictionary with counts of removed items
        
    Example:
        >>> clear_scene()  # Remove everything
        >>> clear_scene(include_materials=False)  # Keep materials
        >>> clear_scene(include_meshes=False, include_curves=False)  # Keep geometry data
    """
    removed_counts = {
        'objects': 0,
        'materials': 0,
        'meshes': 0,
        'curves': 0,
        'lights': 0,
        'cameras': 0
    }
    
    # Remove all objects
    for obj in bpy.data.objects[:]:
        bpy.data.objects.remove(obj, do_unlink=True)
        removed_counts['objects'] += 1
    
    # Remove materials if requested
    if include_materials:
        for mat in bpy.data.materials[:]:
            bpy.data.materials.remove(mat, do_unlink=True)
            removed_counts['materials'] += 1
    
    # Remove mesh data if requested
    if include_meshes:
        for mesh in bpy.data.meshes[:]:
            bpy.data.meshes.remove(mesh, do_unlink=True)
            removed_counts['meshes'] += 1
    
    # Remove curve data if requested
    if include_curves:
        for curve in bpy.data.curves[:]:
            bpy.data.curves.remove(curve, do_unlink=True)
            removed_counts['curves'] += 1
    
    # Remove light data if requested
    if include_lights:
        for light in bpy.data.lights[:]:
            bpy.data.lights.remove(light, do_unlink=True)
            removed_counts['lights'] += 1
    
    # Remove camera data if requested
    if include_cameras:
        for camera in bpy.data.cameras[:]:
            bpy.data.cameras.remove(camera, do_unlink=True)
            removed_counts['cameras'] += 1
    
    print(f"[TraitBlender] Scene cleared: {removed_counts['objects']} objects, {removed_counts['materials']} materials, {removed_counts['meshes']} meshes, {removed_counts['curves']} curves, {removed_counts['lights']} lights, {removed_counts['cameras']} cameras removed")
    
    return removed_counts
