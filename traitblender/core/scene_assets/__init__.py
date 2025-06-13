"""
TraitBlender Scene Assets

Scene asset management system for Blender objects with enhanced transformation capabilities.
"""

# Import core classes and variables
from .scene_asset import SceneAsset, GenericAsset, ASSET_TYPES

# Import context managers
from .asset_helpers import (
    scene_asset,
    with_scene_asset,
)

__all__ = [
    # Core classes
    "SceneAsset",
    "GenericAsset",
    "ASSET_TYPES",
    # Context managers
    "scene_asset",
    "with_scene_asset",
] 