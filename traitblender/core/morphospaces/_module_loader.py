"""Shared loader for morphospace modules."""

import os
import importlib.util
import sys

from ..helpers import get_asset_path


def load_morphospace_module(morphospace_name):
    """
    Load a morphospace module by name.
    
    Returns:
        Module object or None if not found/failed
    """
    if not morphospace_name:
        return None
    
    morphospace_modules_path = get_asset_path("morphospace_modules")
    morphospace_path = os.path.join(morphospace_modules_path, morphospace_name)
    
    if not os.path.exists(morphospace_path):
        return None
    
    try:
        spec = importlib.util.spec_from_file_location(
            morphospace_name,
            os.path.join(morphospace_path, "__init__.py"),
            submodule_search_locations=[morphospace_path]
        )
        if spec is None or spec.loader is None:
            return None
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[morphospace_name] = module
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"TraitBlender: Error loading morphospace '{morphospace_name}': {e}")
        return None
