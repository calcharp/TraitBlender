"""
TraitBlender Config Path Helpers

Utilities for resolving and parsing config property paths, including vector component access.
"""

from .constants import COMPONENT_TO_INDEX


def resolve_config_path(path: str) -> str:
    """Resolve relative path to full traitblender_config property path."""
    return "bpy.context.scene.traitblender_config." + path


def parse_component_path(path: str):
    """
    If path has 3+ parts and last is x/y/z or r/g/b/a, return (parent_path, index). Else None.
    
    Examples:
        "camera.location.x" -> ("camera.location", 0)
        "world.color.r" -> ("world.color", 0)
    """
    parts = path.split(".")
    if len(parts) < 3:
        return None
    last = parts[-1].lower()
    if last in COMPONENT_TO_INDEX:
        return ".".join(parts[:-1]), COMPONENT_TO_INDEX[last]
    return None
