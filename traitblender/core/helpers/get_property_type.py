"""
Get Blender property type for a given property path (config or full path).

Used for proper YAML representation of config properties.
"""

import bpy

from .constants import VALID_PROPERTY_TYPES


def get_property_type(property_path: str, in_config: bool = True):
    """
    Get the Blender property type for a given property path.
    
    Args:
        property_path (str): Property path (e.g., 'camera.location', 'world.color' if in_config=True,
                           or 'bpy.data.objects["Camera"].location' if in_config=False)
        in_config (bool): If True, treat property_path as relative to traitblender_config.
                         If False, treat property_path as a full Blender path.
        
    Returns:
        str or None: Property type name (e.g., 'FloatVectorProperty', 'EnumProperty') or None if not found
        
    Example:
        >>> get_property_type('camera.location')
        'FloatVectorProperty'
        >>> get_property_type('camera.focal_length')
        'FloatProperty'
        >>> get_property_type('camera.lens_unit')
        'EnumProperty'
        >>> get_property_type('bpy.data.objects["Camera"].location', in_config=False)
        'FloatVectorProperty'
        >>> get_property_type('bpy.data.scenes["Scene"].eevee.taa_render_samples', in_config=False)
        'IntProperty'
    """
    try:
        if in_config:
            # Get the traitblender config
            config = bpy.context.scene.traitblender_config
            if not config:
                return None
            
            # Split the path into parts
            parts = property_path.split('.')
            
            # Navigate to the parent object
            current = config
            for part in parts[:-1]:  # All but the last part
                if not hasattr(current, part):
                    return None
                current = getattr(current, part)
            
            # Get the property name (last part)
            property_name = parts[-1]
            
            # Check if the property exists
            if not hasattr(current, property_name):
                return None
            
            # Get the property's RNA information
            if not hasattr(current, 'bl_rna') or not hasattr(current.bl_rna, 'properties'):
                return None
            
            if property_name not in current.bl_rna.properties:
                return None
            
            property_rna = current.bl_rna.properties[property_name]
            
        else:
            # Handle full Blender paths
            try:
                property_value = eval(property_path, {"bpy": bpy})
            except Exception:
                return None
            
            last_dot_index = property_path.rfind('.')
            if last_dot_index == -1:
                return None
            
            object_path = property_path[:last_dot_index]
            property_name = property_path[last_dot_index + 1:]
            
            try:
                current = eval(object_path, {"bpy": bpy})
            except Exception:
                return None
            
            if not hasattr(current, 'bl_rna') or not hasattr(current.bl_rna, 'properties'):
                return None
            
            if property_name not in current.bl_rna.properties:
                return None
            
            property_rna = current.bl_rna.properties[property_name]
        
        rna_type_name = property_rna.rna_type.identifier
        is_array = False
        if hasattr(property_rna, 'is_array'):
            is_array = property_rna.is_array
        
        if rna_type_name == 'FloatProperty':
            return 'FloatVectorProperty' if is_array else 'FloatProperty'
        elif rna_type_name == 'IntProperty':
            return 'IntVectorProperty' if is_array else 'IntProperty'
        elif rna_type_name == 'BoolProperty':
            return 'BoolVectorProperty' if is_array else 'BoolProperty'
        elif rna_type_name in ['EnumProperty', 'StringProperty']:
            return rna_type_name
        else:
            return None
            
    except Exception as e:
        print(f"Error getting property type for '{property_path}': {e}")
        return None
