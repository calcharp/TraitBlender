"""Trait parameter functions for morphospaces."""

import inspect

from ._module_loader import load_morphospace_module


def get_trait_parameters_for_morphospace(morphospace_name):
    """
    Get trait parameter names and defaults for a morphospace (sample() params excluding name, hyperparameters).
    Used for default dataset columns when no file is imported.
    
    Returns:
        list: Ordered list of trait param names (e.g. ['b', 'd', 'z', 'a', 'phi', 'psi', ...])
    """
    traits = get_trait_parameters_with_defaults_for_morphospace(morphospace_name)
    return list(traits.keys())


def get_trait_parameters_with_defaults_for_morphospace(morphospace_name):
    """
    Get trait parameters and their default values for a morphospace.
    
    Returns:
        dict: {param_name: default_value} in signature order (for default dataset row)
    """
    module = load_morphospace_module(morphospace_name)
    if module is None:
        return {}
    
    sample_func = getattr(module, 'sample', None)
    if not callable(sample_func):
        return {}
    
    sig = inspect.signature(sample_func)
    hyperparams = set(getattr(module, 'HYPERPARAMETERS', {}).keys()) | {'hyperparameters'}
    exclude = {'name'} | hyperparams
    
    result = {}
    for pname, param in sig.parameters.items():
        if pname in exclude:
            continue
        default = param.default
        if default is inspect.Parameter.empty:
            default = 0.0
        result[pname] = default
    return result
