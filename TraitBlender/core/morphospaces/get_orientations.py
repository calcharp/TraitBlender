"""Orientation functions for morphospaces."""

from ._module_loader import load_morphospace_module


def get_orientations_for_morphospace(morphospace_name):
    """
    Get the ORIENTATIONS dictionary from a morphospace module.
    
    Morphospace modules must export ORIENTATIONS with at least "Default": callable.
    Each callable receives (sample_obj) and orients the object in place.
    
    Returns:
        dict: ORIENTATIONS from the module, or empty dict if not defined/failed
    """
    module = load_morphospace_module(morphospace_name)
    if module is None:
        return {}
    return getattr(module, 'ORIENTATIONS', {})


def get_orientation_names(morphospace_name):
    """
    Get list of orientation names for a morphospace (for pipeline iteration, etc.).
    Returns e.g. ['Default', ...].
    """
    orientations = get_orientations_for_morphospace(morphospace_name)
    return list(orientations.keys()) if orientations else []
