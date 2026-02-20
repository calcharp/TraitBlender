"""
Add-on path and user directory helpers.

Resolve add-on root, asset paths, user data directory, and initialize user dirs (configs, outputs, cache, optional assets copy).
"""

import os
import shutil
import importlib

import bpy

from .constants import ADDON_PACKAGE


def get_addon_root():
    """
    Get the root directory of the installed add-on package.
    """
    traitblender_pkg = importlib.import_module(ADDON_PACKAGE)
    return os.path.dirname(os.path.abspath(traitblender_pkg.__file__))


def get_user_data_dir():
    """
    Get the user data directory for the add-on (Blender's extension_path_user).
    """
    return bpy.utils.extension_path_user(ADDON_PACKAGE, create=True)


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
    addon_dir = get_addon_root()
    assets_dir = os.path.join(addon_dir, "assets")
    return os.path.join(assets_dir, *path_parts)


def init_user_dirs(copy_assets=False):
    """
    Initialize user data directories (configs, outputs, cache) and optionally copy assets.

    Args:
        copy_assets (bool): If True, copy the entire assets directory to the user data dir if not present
    """
    user_base = get_user_data_dir()
    for sub in ["configs", "outputs", "cache"]:
        os.makedirs(os.path.join(user_base, sub), exist_ok=True)
    if copy_assets:
        user_assets = os.path.join(user_base, "assets")
        addon_assets = os.path.join(get_addon_root(), "assets")
        if not os.path.exists(user_assets):
            shutil.copytree(addon_assets, user_assets)
