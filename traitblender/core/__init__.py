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
)

# Scene Assets
from .scene_assets import (
    SceneAsset,
    GenericAsset, 
    scene_asset,
    with_scene_asset,
)

# Transforms
from .transforms import (
    Transform,
)

# Config, morphospaces, and datasets (placeholder for future development)
# from .config import *
# from .morphospaces import *
# from .datasets import *

__all__ = [
    # Helper functions
    "get_asset_path",
    "apply_material",
    "get_texture_info",
    "VALID_TEXTURES",
    
    # Scene Assets
    "SceneAsset",
    "GenericAsset", 
    "scene_asset",
    "with_scene_asset",
    
    # Transforms
    "Transform",
]
