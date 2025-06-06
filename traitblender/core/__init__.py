"""
TraitBlender Core Module

Contains the core functionality including configuration, datasets, morphospaces, 
transforms, scene assets, and helper functions.

Import everything you need from here:
    from TraitBlender.core import get_asset_path, set_textures, SceneAsset, etc.
"""

# Helper functions and utilities
from .helpers import (
    get_asset_path,
    apply_material,
    set_textures,  # Backward compatibility
    get_texture_info,
    VALID_TEXTURES,
)

# Scene Assets
from .scene_assets import (
    SceneAsset,
    GenericAsset, 
    SurfaceAsset,
)

# Transforms
from .transforms import (
    TransformFactory,
    transform_factory,
    register_transform,
    clear_scene,
    lighting_setup,
)

# Config, morphospaces, and datasets (placeholder for future development)
# from .config import *
# from .morphospaces import *
# from .datasets import *

__all__ = [
    # Helper functions
    "get_asset_path",
    "apply_material",
    "set_textures",  # Backward compatibility
    "get_texture_info",
    "VALID_TEXTURES",
    
    # Scene Assets
    "SceneAsset",
    "GenericAsset", 
    "SurfaceAsset",
    
    # Transforms
    "TransformFactory",
    "transform_factory", 
    "register_transform",
    "clear_scene",
    "lighting_setup",
]
