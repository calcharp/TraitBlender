"""
TraitBlender Core Helpers

Utility functions and helpers for the TraitBlender add-on.
"""

import os
from .import_texture import apply_material, get_texture_info, VALID_TEXTURES, set_textures
from .object_validator import (
    ObjectNotFoundError,
    must_exist,
    check_object_exists,
)   
from .prop_gettersetter import get_property, set_property
from .asset_manager import get_addon_root, get_user_data_dir, get_asset_path, init_user_dirs
from .config_validator import validate_config_path, get_config_path_info, list_config_properties
from .property_type_checker import get_property_type, VALID_PROPERTY_TYPES

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
    addon_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    assets_dir = os.path.join(addon_dir, "assets")
    return os.path.join(assets_dir, *path_parts)

__all__ = [
    "get_asset_path",
    "get_addon_root",
    "get_user_data_dir",
    "init_user_dirs",
    "apply_material",
    "get_texture_info",
    "VALID_TEXTURES",
    "set_textures",
    # Object validation utilities
    "ObjectNotFoundError",
    "must_exist",
    "check_object_exists",
    # Property getter/setter
    "get_property",
    "set_property",
    # Config validator functions
    "validate_config_path",
    "get_config_path_info",
    "list_config_properties",
    # Property type checker functions
    "get_property_type",
    "VALID_PROPERTY_TYPES",
] 