"""
TraitBlender Scene Assets

Scene asset management system for Blender objects with enhanced transformation capabilities.
"""

# Import core classes
from .scene_asset import SceneAsset, GenericAsset, SurfaceAsset

# Import context managers
from .context_managers import (
    scene_asset,
)

__all__ = [
    # Core classes
    "SceneAsset",
    "GenericAsset", 
    "SurfaceAsset",
    # Context managers
    "scene_asset",
] 