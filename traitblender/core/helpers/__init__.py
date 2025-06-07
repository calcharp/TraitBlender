"""
TraitBlender Core Helpers

Utility functions and helpers for the TraitBlender add-on.
"""

import os
from .import_texture import apply_material, get_texture_info, VALID_TEXTURES
from .object_validator import (
    require_objects, 
    ObjectNotFoundError, 
    get_object_safely, 
    list_scene_objects, 
    validate_objects_exist
)
from .selection_manager import (
    with_active_object,
    with_selected_objects,
    SelectionContext
)

def get_asset_path(*path_parts):
    """
    Get the full path to an asset in the addon's assets directory.
    
    Args:
        *path_parts: Path components relative to the assets directory
        
    Returns:
        str: Full path to the asset
        
    Example:
        get_asset_path("objects", "table", "table.fbx")
        get_asset_path("textures", "wood.png")
    """
    # Get the addon root directory (3 levels up from this file)
    addon_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(addon_dir, "assets", *path_parts)

__all__ = [
    "get_asset_path",
    "apply_material",
    "get_texture_info",
    "VALID_TEXTURES",
    # Object validation utilities
    "require_objects",
    "ObjectNotFoundError",
    "get_object_safely",
    "list_scene_objects",
    "validate_objects_exist",
    # Selection management utilities
    "with_active_object",
    "with_selected_objects",
    "SelectionContext",
] 