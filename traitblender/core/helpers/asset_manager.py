import os
import shutil
import bpy

# Name of the top-level add-on package (update as needed)
ADDON_PACKAGE = "bl_ext.user_default.traitblender"


def get_addon_root():
    """
    Get the root directory of the installed add-on package.
    """
    # Import inside the function to avoid circular dependencies
    import importlib
    traitblender_pkg = importlib.import_module(ADDON_PACKAGE)
    return os.path.dirname(os.path.abspath(traitblender_pkg.__file__))


def get_user_data_dir():
    """
    Get the user data directory for the add-on (Blender's extension_path_user).
    """
    return bpy.utils.extension_path_user(ADDON_PACKAGE, create=True)


def get_asset_path(*path_parts, prefer_user=True):
    """
    Get the full path to an asset, preferring the user data directory if present.
    
    Args:
        *path_parts: Path components inside the assets directory
        prefer_user (bool): If True, prefer user data directory if asset exists there
    Returns:
        str: Full path to the asset
    
    Example:
        # Get the path to a table texture in the table_material folder
        path = get_asset_path("objects", "table", "table_material", "DIFFUSE_old_table_Albedo.png")
        # Result (if user asset exists):
        #   C:/Users/yourname/AppData/Roaming/Blender Foundation/Blender/4.3/extensions/user_default/traitblender/assets/objects/table/table_material/DIFFUSE_old_table_Albedo.png
        # Result (if not in user dir):
        #   C:/path/to/addon/bl_ext/user_default/traitblender/assets/objects/table/table_material/DIFFUSE_old_table_Albedo.png
    """
    user_asset = os.path.join(get_user_data_dir(), "assets", *path_parts)
    addon_asset = os.path.join(get_addon_root(), "assets", *path_parts)
    if prefer_user and os.path.exists(user_asset):
        return user_asset
    return addon_asset


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