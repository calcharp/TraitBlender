"""
TraitBlender Core Module

Contains the core functionality including configuration, datasets, morphospaces, 
transforms, scene assets, and helper functions.

Import everything you need from here:
    from TraitBlender.core import get_asset_path, SceneAsset, etc.
"""

# Helper functions and utilities
from .helpers import (
    get_asset_path,
    apply_material,
    get_texture_info,
    VALID_TEXTURES,
    set_textures,
    ObjectNotFoundError,
    must_exist,
    check_object_exists,
    clear_scene,
)

# Positioning (currently empty)
# from .positioning import (
#     # No exports currently available
# )

# Transforms
from .transforms import (
    TRANSFORMS,
)

from .positioning import (
    world_to_table_coords,
)

# Config
from .config import CONFIG, register, configs, configure_traitblender

# Config, morphospaces, and datasets (placeholder for future development)
# from .morphospaces import *
# from .datasets import *

__all__ = [
    # Helper functions
    "get_asset_path",
    "apply_material",
    "get_texture_info",
    "VALID_TEXTURES",
    "set_textures",
    "ObjectNotFoundError",
    "must_exist",
    "check_object_exists",
    "clear_scene",
    
    # Positioning
    "world_to_table_coords",
    
    # Transforms
    "TRANSFORMS",
    
    # Config
    "CONFIG",
    "register",
    "configure_traitblender",
    "configs",
]
