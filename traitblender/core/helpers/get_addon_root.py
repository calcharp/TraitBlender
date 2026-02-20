"""
Add-on root directory resolution.
"""

import os

from .constants import ADDON_PACKAGE


def get_addon_root():
    """
    Get the root directory of the installed add-on package.
    """
    import importlib
    traitblender_pkg = importlib.import_module(ADDON_PACKAGE)
    return os.path.dirname(os.path.abspath(traitblender_pkg.__file__))
