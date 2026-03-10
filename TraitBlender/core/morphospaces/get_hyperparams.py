"""Hyperparameter functions for morphospaces."""

from ._module_loader import load_morphospace_module


def get_hyperparameters_for_morphospace(morphospace_name):
    """
    Get the HYPERPARAMETERS dictionary from a morphospace module.
    Returns default values and schema (param names, types from defaults).
    
    Returns:
        dict: HYPERPARAMETERS from the module, or empty dict if not defined
    """
    module = load_morphospace_module(morphospace_name)
    if module is None:
        return {}
    return dict(getattr(module, 'HYPERPARAMETERS', {}))
