"""
Initialize user data directories (configs, outputs, cache) and optionally copy assets.
"""

import os
import shutil

from .get_addon_root import get_addon_root
from .get_user_data_dir import get_user_data_dir


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
