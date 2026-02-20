"""
Object helpers.

Validation utilities: ensure required objects exist in the Blender scene (check_object_exists, must_exist decorator).
"""

import bpy
from functools import wraps
from typing import List, Union, Callable, Any


class ObjectNotFoundError(Exception):
    """Raised when a required object is not found in the scene."""
    pass


def check_object_exists(name: str):
    """
    Checks if the specified object exists in the Blender scene. Raises ObjectNotFoundError if not.
    Args:
        name (str): The name of the object to check for existence.
    Raises:
        ObjectNotFoundError: If the object does not exist in the Blender scene.
    """
    if name not in bpy.data.objects or name not in [obj.name for obj in bpy.context.scene.objects]:
        raise ObjectNotFoundError(f"Object '{name}' does not exist in the Blender scene.")


def must_exist(name: str):
    """
    Decorator that throws an error if the specified object does not exist in the Blender scene.
    Args:
        name (str): The name of the object to check for existence.
    Raises:
        ObjectNotFoundError: If the object does not exist in the Blender scene.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            check_object_exists(name)
            return func(*args, **kwargs)
        return wrapper
    return decorator
