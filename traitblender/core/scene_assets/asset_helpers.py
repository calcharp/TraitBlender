from contextlib import contextmanager
from .scene_asset import ASSET_TYPES
from functools import wraps
from ..helpers import check_object_exists

@contextmanager
def scene_asset(name: str, type: str = "GenericAsset"):
    """
    Context manager that temporarily treats a Blender object as a SceneAsset.
    
    Args:
        object_name (str): Name of the Blender object to manage
        asset_type (str, optional): Type of SceneAsset to use. Must be a key in ASSET_TYPES.
            Defaults to "GenericAsset".
    
    Yields:
        SceneAsset: The object wrapped as a SceneAsset of the specified type
    
    Raises:
        KeyError: If the specified asset_type is not found in ASSET_TYPES
    """
    check_object_exists(name)
    if type not in ASSET_TYPES:
        raise KeyError(f"Asset type '{type}' not found in ASSET_TYPES. Available types: {list(ASSET_TYPES.keys())}")
    
    asset_class = ASSET_TYPES[type]
    asset = asset_class(name)
    
    try:
        yield asset
    finally:
        # Cleanup if needed
        pass


def with_scene_asset(name: str = None, type: str = "GenericAsset"):
    """
    Decorator that provides a scene asset to the decorated function as an 'active_asset' parameter.
    
    Args:
        name (str, optional): Name of the Blender object to manage. If None, the function must provide it.
        type (str, optional): Type of SceneAsset to use. Must be a key in ASSET_TYPES.
            Defaults to "GenericAsset".
    
    The decorated function will receive the scene asset as an 'active_asset' parameter.
    If name is None, the decorated function must accept a 'name' parameter.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # If name wasn't provided to decorator, get it from kwargs
            asset_name = name or kwargs.pop('name')
            
            with scene_asset(asset_name, type) as active_asset:
                # Add active_asset to kwargs
                kwargs['active_asset'] = active_asset
                return func(*args, **kwargs)
        return wrapper
    return decorator 