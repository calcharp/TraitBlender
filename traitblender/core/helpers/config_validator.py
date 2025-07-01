"""
TraitBlender Config Validator

Helper functions for validating configuration property paths.
"""

import bpy


def validate_config_path(property_path: str) -> bool:
    """
    Check if a property path exists in the traitblender config.
    
    Args:
        property_path (str): Relative property path (e.g., 'world.color', 'camera.location')
        
    Returns:
        bool: True if the path exists, False otherwise
        
    Example:
        >>> validate_config_path('world.color')
        True
        >>> validate_config_path('nonexistent.property')
        False
    """
    if not isinstance(property_path, str):
        return False
    
    # Get the traitblender config
    try:
        config = bpy.context.scene.traitblender_config
    except AttributeError:
        # traitblender_config doesn't exist yet
        return False
    
    # Split the path into parts
    parts = property_path.split('.')
    
    # Navigate through the config structure
    current = config
    for part in parts:
        try:
            # Check if the attribute exists
            if not hasattr(current, part):
                return False
            # Move to the next level
            current = getattr(current, part)
        except Exception:
            return False
    
    return True


def get_config_path_info(property_path: str) -> dict:
    """
    Get information about a config property path.
    
    Args:
        property_path (str): Relative property path (e.g., 'world.color')
        
    Returns:
        dict: Information about the path including:
            - exists (bool): Whether the path exists
            - type (str): Type of the property if it exists
            - sections (list): List of valid config sections
            - error (str): Error message if validation fails
    """
    result = {
        'exists': False,
        'type': None,
        'sections': [],
        'error': None
    }
    
    # Get available sections
    try:
        config = bpy.context.scene.traitblender_config
        sections = config.get_config_sections()
        result['sections'] = list(sections.keys())
    except AttributeError:
        result['error'] = "traitblender_config not found - run setup scene first"
        return result
    
    # Check if path exists
    if not validate_config_path(property_path):
        result['error'] = f"Property path '{property_path}' not found in config"
        return result
    
    # Get property type
    try:
        parts = property_path.split('.')
        current = config
        for part in parts:
            current = getattr(current, part)
        
        # Get the property type from the class annotations
        if hasattr(current, '__class__') and hasattr(current.__class__, '__annotations__'):
            prop_name = parts[-1]
            if prop_name in current.__class__.__annotations__:
                result['type'] = str(current.__class__.__annotations__[prop_name])
        
        result['exists'] = True
    except Exception as e:
        result['error'] = f"Error accessing property: {e}"
    
    return result


def list_config_properties(section: str = None) -> list:
    """
    List all available properties in the traitblender config.
    
    Args:
        section (str, optional): Specific section to list (e.g., 'world', 'camera')
        
    Returns:
        list: List of property paths
    """
    properties = []
    
    try:
        config = bpy.context.scene.traitblender_config
    except AttributeError:
        return properties
    
    if section:
        # List properties for specific section
        if hasattr(config, section):
            section_obj = getattr(config, section)
            if hasattr(section_obj, '__class__') and hasattr(section_obj.__class__, '__annotations__'):
                for prop_name in section_obj.__class__.__annotations__.keys():
                    properties.append(f"{section}.{prop_name}")
    else:
        # List all properties across all sections
        sections = config.get_config_sections()
        for section_name, section_obj in sections.items():
            if hasattr(section_obj, '__class__') and hasattr(section_obj.__class__, '__annotations__'):
                for prop_name in section_obj.__class__.__annotations__.keys():
                    properties.append(f"{section_name}.{prop_name}")
    
    return sorted(properties) 