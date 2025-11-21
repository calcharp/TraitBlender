"""
Helper module for getting available properties from TraitBlender config.
Works both standalone (with mock data) and when integrated with Blender.
"""

def get_available_sections():
    """
    Get list of available configuration sections.
    In standalone mode, returns common sections.
    When integrated, will use bpy.context.scene.traitblender_config.
    
    Returns:
        list: List of tuples (section_name, display_name)
    """
    try:
        import bpy
        config = bpy.context.scene.traitblender_config
        sections = config.get_config_sections()
        return [
            (section_name, section_name.replace('_', ' ').title()) 
            for section_name in sections.keys()
            if section_name.lower() != "transforms"
        ]
    except (ImportError, AttributeError):
        # Standalone mode - return common sections
        return [
            ("world", "World"),
            ("camera", "Camera"),
            ("lamp", "Lamp"),
            ("output", "Output"),
            ("orientations", "Orientations"),
        ]


def get_properties_for_section(section_name):
    """
    Get list of properties available in a given section.
    
    Args:
        section_name: Name of the configuration section
        
    Returns:
        list: List of tuples (property_name, display_name)
    """
    try:
        import bpy
        config = bpy.context.scene.traitblender_config
        section_obj = getattr(config, section_name, None)
        if section_obj and hasattr(section_obj, '__class__') and hasattr(section_obj.__class__, '__annotations__'):
            return [
                (prop_name, prop_name.replace('_', ' ').title())
                for prop_name in section_obj.__class__.__annotations__.keys()
                if prop_name != "show"
            ]
        return []
    except (ImportError, AttributeError):
        # Standalone mode - return common properties per section
        mock_properties = {
            "world": [
                ("color", "Color"),
                ("hdri_path", "HDRI Path"),
                ("hdri_strength", "HDRI Strength"),
            ],
            "camera": [
                ("location", "Location"),
                ("rotation", "Rotation"),
                ("focal_length", "Focal Length"),
                ("sensor_width", "Sensor Width"),
            ],
            "lamp": [
                ("type", "Type"),
                ("power", "Power"),
                ("color", "Color"),
                ("location", "Location"),
            ],
            "output": [
                ("resolution_x", "Resolution X"),
                ("resolution_y", "Resolution Y"),
                ("samples", "Samples"),
                ("file_format", "File Format"),
            ],
            "orientations": [
                ("object_location_origin", "Object Location Origin"),
                ("object_rotation_origin", "Object Rotation Origin"),
                ("location_shift_axes", "Location Shift Axes"),
            ],
        }
        return mock_properties.get(section_name, [])


def build_property_path(section, property_name):
    """
    Build a property path from section and property names.
    
    Args:
        section: Section name
        property_name: Property name within the section
        
    Returns:
        str: Full property path (e.g., "world.color")
    """
    return f"{section}.{property_name}"


def parse_property_path(property_path):
    """
    Parse a property path into section and property components.
    
    Args:
        property_path: Full property path (e.g., "world.color")
        
    Returns:
        tuple: (section, property) or (None, None) if invalid
    """
    if not property_path or "." not in property_path:
        return None, None
    
    parts = property_path.split(".", 1)
    return parts[0], parts[1]

