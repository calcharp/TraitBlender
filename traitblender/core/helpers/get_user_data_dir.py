"""
User data directory for the add-on (Blender extension user path).
"""

import bpy

from .constants import ADDON_PACKAGE


def get_user_data_dir():
    """
    Get the user data directory for the add-on (Blender's extension_path_user).
    """
    return bpy.utils.extension_path_user(ADDON_PACKAGE, create=True)
