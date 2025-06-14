"""
TraitBlender Scene Assets

Scene asset management system for Blender objects with enhanced transformation capabilities.
"""

# Import core classes and variables
from .asset_types import ASSET_TYPES

# Import context managers
from .asset_helpers import (
    scene_asset,
    with_scene_asset,
)

__all__ = [
    # Core classes
    "ASSET_TYPES",
    # Context managers
    "scene_asset",
    "with_scene_asset",
] 