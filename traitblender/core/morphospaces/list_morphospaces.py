import os
from ..helpers import get_asset_path

def list_morphospaces():
    """
    List all available morphospaces by scanning the assets/morphospace_modules directory.
    
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
                morphospaces.append(item)
    except Exception as e:
        print(f"Error listing morphospaces: {e}")
        return []
    
    return sorted(morphospaces) 