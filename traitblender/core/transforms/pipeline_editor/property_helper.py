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


def get_available_samplers():
    """
    Get list of available sampler functions.
    In standalone mode, returns common samplers.
    When integrated, will use the TRANSFORMS registry.
    
    Returns:
        list: List of tuples (sampler_name, display_name)
    """
    try:
        # Try to import from TraitBlender
        import sys
        import os
        # Add parent directories to path if needed
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        from core.transforms.registry import TRANSFORMS
        return [
            (sampler_name, sampler_name.replace('_', ' ').title())
            for sampler_name in sorted(TRANSFORMS.keys())
        ]
    except (ImportError, AttributeError):
        # Standalone mode - return actual samplers from registry
        return [
            ("uniform", "Uniform"),
            ("normal", "Normal"),
            ("beta", "Beta"),
            ("gamma", "Gamma"),
            ("dirichlet", "Dirichlet"),
            ("multivariate_normal", "Multivariate Normal"),
            ("poisson", "Poisson"),
            ("exponential", "Exponential"),
            ("cauchy", "Cauchy"),
            ("discrete_uniform", "Discrete Uniform"),
        ]

