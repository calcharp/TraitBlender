"""
TraitBlender Property Type Checker

Helper functions for checking Blender property types to ensure proper YAML representation.
"""

import bpy


# Valid Blender property types from bpy.props
VALID_PROPERTY_TYPES = {
    'BoolProperty',
    'BoolVectorProperty', 
    'EnumProperty',
    'FloatProperty',
    'FloatVectorProperty',
    'IntProperty',
    'IntVectorProperty',
    'StringProperty'
}


def get_property_type(property_path: str):
    """
    Get the Blender property type for a given property path.
    
    Args:
        property_path (str): Relative property path (e.g., 'camera.location', 'world.color')
        
    Returns:
        str or None: Property type name (e.g., 'FloatVectorProperty', 'EnumProperty') or None if not found
        
    Example:
        >>> get_property_type('camera.location')
        'FloatVectorProperty'
        >>> get_property_type('camera.focal_length')
        'FloatProperty'
        >>> get_property_type('camera.lens_unit')
        'EnumProperty'
    """
    try:
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
        
        # Get the RNA type name
        rna_type_name = property_rna.rna_type.identifier
        
        # Check if it's an array property
        is_array = False
        if hasattr(property_rna, 'is_array'):
            is_array = property_rna.is_array
        
        # Map the base type to the correct property type based on is_array
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