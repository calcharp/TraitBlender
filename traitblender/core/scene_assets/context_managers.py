"""
SceneAsset Context Managers

Context managers for temporary SceneAsset instances with automatic validation.
"""

from contextlib import contextmanager
from typing import Union, Dict, Type, Any, Tuple

from .scene_asset import SceneAsset, GenericAsset, SurfaceAsset
from ..helpers import validate_objects_exist, ObjectNotFoundError


def _get_default_asset_type() -> Type[SceneAsset]:
    """
    Returns the default SceneAsset type.
    GenericAsset works for any object and doesn't make assumptions.
    """
    return GenericAsset


@contextmanager
def scene_asset(object_name: str, asset_type: Type[SceneAsset] = None):
    """
    Context manager for temporary SceneAsset instances.
    
    Args:
        object_name: Name of the Blender object
        asset_type: Optional SceneAsset subclass to use. Defaults to GenericAsset.
        
    Yields:
        SceneAsset instance of the specified type
        
    Raises:
        ObjectNotFoundError: If the object doesn't exist in the scene
        
    Example:
        with scene_asset("Table") as table:  # GenericAsset
            table.location = (0, 0, 0)
            
        with scene_asset("Table", SurfaceAsset) as table:  # SurfaceAsset
            table.place(specimen, (0, 0))
    """
    # Validate object exists
    existing, missing = validate_objects_exist(object_name)
    if missing:
        raise ObjectNotFoundError(f"Cannot create scene asset: object '{object_name}' not found")
    
    # Use specified type or default
    if asset_type is None:
        asset_type = _get_default_asset_type()
    
    # Create and yield asset
    asset = asset_type(object_name)
    try:
        yield asset
    finally:
        # No cleanup needed for SceneAsset instances
        pass


 