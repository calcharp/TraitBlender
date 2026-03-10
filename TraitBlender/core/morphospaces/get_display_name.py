"""Display name for morphospace modules."""

from ._module_loader import load_morphospace_module


def get_morphospace_display_name(morphospace_name):
    """
    Get display name for a morphospace.
    Uses NAME from module if defined, otherwise falls back to folder name.

    Returns:
        str: Display name for GUI and config references
    """
    module = load_morphospace_module(morphospace_name)
    if module is None:
        return morphospace_name
    return getattr(module, 'NAME', morphospace_name)
