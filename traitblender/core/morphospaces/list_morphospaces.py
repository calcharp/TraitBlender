import os
import importlib.util
import sys
from ..helpers import get_asset_path

def list_morphospaces():
    """
    List all available morphospaces by scanning the assets/morphospace_modules directory.
    Only morphospaces with a required 'Default' orientation are listed.
    
    Returns:
        list: List of morphospace names (folder names)
    """
    morphospace_modules_path = get_asset_path("morphospace_modules")
    
    if not os.path.exists(morphospace_modules_path):
        return []
    
    morphospaces = []
    try:
        for item in os.listdir(morphospace_modules_path):
            item_path = os.path.join(morphospace_modules_path, item)
            # Check if it's a directory and has an __init__.py file
            if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, "__init__.py")):
                # Require Default orientation
                orientations = get_orientations_for_morphospace(item)
                if 'Default' in orientations and callable(orientations.get('Default')):
                    morphospaces.append(item)
                else:
                    print(f"TraitBlender: Skipping morphospace '{item}' - missing required 'Default' in ORIENTATIONS")
    except Exception as e:
        print(f"Error listing morphospaces: {e}")
        return []
    
    return sorted(morphospaces)


def get_orientation_names(morphospace_name):
    """
    Get list of orientation names for a morphospace (for pipeline iteration, etc.).
    Returns e.g. ['Default', ...].
    """
    orientations = get_orientations_for_morphospace(morphospace_name)
    return list(orientations.keys()) if orientations else []


def get_orientations_for_morphospace(morphospace_name):
    """
    Get the ORIENTATIONS dictionary from a morphospace module.
    
    Morphospace modules must export ORIENTATIONS with at least "Default": callable.
    Each callable receives (sample_obj) and orients the object in place.
    
    Returns:
        dict: ORIENTATIONS from the module, or empty dict if not defined/failed
    """
    if not morphospace_name:
        return {}
    
    morphospace_modules_path = get_asset_path("morphospace_modules")
    morphospace_path = os.path.join(morphospace_modules_path, morphospace_name)
    
    if not os.path.exists(morphospace_path):
        return {}
    
    try:
        spec = importlib.util.spec_from_file_location(
            morphospace_name,
            os.path.join(morphospace_path, "__init__.py"),
            submodule_search_locations=[morphospace_path]
        )
        if spec is None or spec.loader is None:
            return {}
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[morphospace_name] = module
        spec.loader.exec_module(module)
        
        return getattr(module, 'ORIENTATIONS', {})
    except Exception as e:
        print(f"TraitBlender: Error loading orientations from {morphospace_name}: {e}")
        return {}