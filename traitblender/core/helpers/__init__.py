"""
TraitBlender Core Helpers

Utility functions and helpers for the TraitBlender add-on.
"""

from .import_texture import apply_material, get_texture_info, VALID_TEXTURES, set_textures
from .object_validator import (
    ObjectNotFoundError,
    must_exist,
    check_object_exists,
)   
from .property_getset import get_property, set_property
from .asset_manager import get_addon_root, get_user_data_dir, init_user_dirs
from .asset_path import get_asset_path
from .config_validator import validate_config_path, get_config_path_info, list_config_properties
from .property_type_checker import get_property_type, VALID_PROPERTY_TYPES
from .scene_cleaner import clear_scene
from .pretty_type_hint import pretty_type_hint

# Import table coordinates functions
try:
    from ..ui.properties.table_coords import _get_tb_coords, _set_tb_coords
    from ..positioning.get_table_coords import z_dist_to_lowest
except ImportError:
    # Fallback if modules are not available
    z_dist_to_lowest = None
    _get_tb_coords = None
    _set_tb_coords = None

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
    # Scene cleaner functions
    "clear_scene",
    "pretty_type_hint",
    # Table coordinates functions
    "z_dist_to_lowest",
    "_get_tb_coords",
    "_set_tb_coords",
] 