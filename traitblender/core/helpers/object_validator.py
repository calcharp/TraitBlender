"""
Object Validation Decorator

A decorator that ensures required objects exist in the Blender scene before executing functions.
"""

import bpy
from functools import wraps
from typing import List, Union, Callable, Any


class ObjectNotFoundError(Exception):
    """Raised when a required object is not found in the scene."""
    pass


def require_objects(object_names: Union[str, List[str]], 
                   raise_error: bool = True) -> Callable:
    """
    Decorator that validates the existence of required objects in the Blender scene.
    
    Can be applied to:
    - Functions
    - Methods (like execute() in Blender operators)
    - Classes (automatically decorates the execute method for Blender operators)
    
    Args:
        object_names: Single object name (str) or list of object names to validate
        raise_error: If True, raises ObjectNotFoundError when objects are missing.
                    If False, returns None when objects are missing.
    
    Returns:
        Decorator function
        
    Raises:
        ObjectNotFoundError: When required objects are missing and raise_error=True
        
    Example:
        # On a function
        @require_objects("Camera")
        def move_camera():
            pass
            
        # On a method
        class MyOperator(bpy.types.Operator):
            @require_objects(["Light", "Cube"])
            def execute(self, context):
                return {'FINISHED'}
                
        # On a class (decorates execute method automatically)
        @require_objects(["Camera", "Light"])
        class MyOperator(bpy.types.Operator):
            def execute(self, context):
                return {'FINISHED'}
    """
    
    # Convert single string to list for uniform handling
    if isinstance(object_names, str):
        object_names = [object_names]
    
    def decorator(target):
        # Check if target is a class
        if isinstance(target, type):
            # For classes, wrap the execute method if it exists
            if hasattr(target, 'execute') and callable(getattr(target, 'execute')):
                original_execute = target.execute
                target.execute = _wrap_function(original_execute, object_names, raise_error)
            return target
        else:
            # For functions/methods, wrap directly
            return _wrap_function(target, object_names, raise_error)
    
    return decorator


def _wrap_function(func: Callable, object_names: List[str], raise_error: bool) -> Callable:
    """
    Internal function to wrap a function with object validation.
    
    Args:
        func: Function to wrap
        object_names: List of required object names
        raise_error: Whether to raise errors or return None
        
    Returns:
        Wrapped function
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        missing_objects = []
        
        # Check if all required objects exist
        for obj_name in object_names:
            if obj_name not in bpy.data.objects:
                missing_objects.append(obj_name)
            elif obj_name not in bpy.context.scene.objects:
                # Object exists in data but not in current scene
                missing_objects.append(f"{obj_name} (not in current scene)")
        
        # Handle missing objects
        if missing_objects:
            if raise_error:
                raise ObjectNotFoundError(
                    f"Required objects not found: {', '.join(missing_objects)}. "
                    f"Function '{func.__name__}' requires these objects to exist in the scene."
                )
            else:
                # Return None if objects are missing and raise_error=False
                print(f"Warning: Missing objects {missing_objects} for function '{func.__name__}'. Skipping execution.")
                return None
        
        # All objects exist, execute the function
        return func(*args, **kwargs)
    
    return wrapper


def get_object_safely(object_name: str) -> Union[bpy.types.Object, None]:
    """
    Safely get an object from the scene without raising exceptions.
    
    Args:
        object_name: Name of the object to retrieve
        
    Returns:
        The Blender object if found, None otherwise
        
    Example:
        obj = get_object_safely("Camera")
        if obj:
            obj.location = (0, 0, 5)
    """
    try:
        return bpy.data.objects.get(object_name)
    except (AttributeError, KeyError):
        return None


def list_scene_objects() -> List[str]:
    """
    Get a list of all object names in the current scene.
    
    Returns:
        List of object names in the current scene
        
    Example:
        objects = list_scene_objects()
        print(f"Scene contains: {', '.join(objects)}")
    """
    return [obj.name for obj in bpy.context.scene.objects]


def validate_objects_exist(object_names: Union[str, List[str]]) -> tuple[List[str], List[str]]:
    """
    Check which objects exist and which are missing from the scene.
    
    Args:
        object_names: Single object name (str) or list of object names to check
        
    Returns:
        Tuple of (existing_objects, missing_objects) lists
        
    Example:
        existing, missing = validate_objects_exist(["Camera", "Light", "Cube"])
        if missing:
            print(f"Missing objects: {missing}")
    """
    if isinstance(object_names, str):
        object_names = [object_names]
    
    existing = []
    missing = []
    
    for obj_name in object_names:
        if obj_name in bpy.data.objects and obj_name in [obj.name for obj in bpy.context.scene.objects]:
            existing.append(obj_name)
        else:
            missing.append(obj_name)
    
    return existing, missing


def with_active_object(object_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with SelectionContext(object_name, active=True):
                return func(*args, **kwargs)
        return wrapper
    return decorator 