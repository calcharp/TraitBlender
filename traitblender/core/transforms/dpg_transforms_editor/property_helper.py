"""
Helper module for getting available properties from SAMPLER_ALLOWED_PATHS.
"""


def _get_all_allowed_paths():
    """Union of all allowed paths across samplers."""
    try:
        from .. import SAMPLER_ALLOWED_PATHS
        paths = set()
        for lst in SAMPLER_ALLOWED_PATHS.values():
            paths.update(lst)
        return paths
    except (ImportError, AttributeError):
        return set()


def get_available_sections():
    """
    Get list of sections that have at least one transformable path.
    
    Returns:
        list: List of tuples (section_name, display_name)
    """
    paths = _get_all_allowed_paths()
    sections = set()
    for path in paths:
        if "." in path:
            section = path.split(".", 1)[0]
            sections.add(section)
    return [(s, s.replace('_', ' ').title()) for s in sorted(sections)]


def get_properties_for_section(section_name):
    """
    Get list of properties in a section that are transformable.
    
    Args:
        section_name: Name of the configuration section
        
    Returns:
        list: List of tuples (property_name, display_name)
    """
    paths = _get_all_allowed_paths()
    prefix = section_name + "."
    result = []
    for path in paths:
        if path.startswith(prefix):
            prop_name = path[len(prefix):]
            result.append((prop_name, prop_name.replace('_', ' ').title()))
    return sorted(result)


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
    Get list of all sampler functions from SAMPLERS dict.
    
    Returns:
        list: List of tuples (sampler_name, display_name)
    """
    try:
        from .. import SAMPLERS
        return [
            (name, name.replace('_', ' ').title())
            for name in sorted(SAMPLERS.keys())
        ]
    except (ImportError, AttributeError):
        return [("normal", "Normal")]


def get_available_samplers_for_property(property_path):
    """
    Get list of samplers that are allowed for the given property path.
    
    Args:
        property_path: Full property path (e.g., "world.color")
        
    Returns:
        list: List of tuples (sampler_name, display_name) for samplers that allow this path
    """
    try:
        from .. import SAMPLER_ALLOWED_PATHS
        result = []
        for sampler_name, allowed_paths in SAMPLER_ALLOWED_PATHS.items():
            if property_path in allowed_paths:
                result.append((sampler_name, sampler_name.replace('_', ' ').title()))
        return sorted(result)
    except (ImportError, AttributeError):
        return [("normal", "Normal")]

