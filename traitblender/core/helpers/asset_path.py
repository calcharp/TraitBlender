"""
Asset path resolution for TraitBlender.
"""

import os


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
