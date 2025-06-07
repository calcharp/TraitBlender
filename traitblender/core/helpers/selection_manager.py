"""
Selection Management Decorator

Decorator for managing Blender object selection and active object state.
"""

import bpy
from functools import wraps
from typing import List, Union, Callable, Any, Optional

from .object_validator import validate_objects_exist, ObjectNotFoundError


def with_active_object(object_name: Union[str, Callable] = None, 
                      param_name: str = "object_name",
                      restore_selection: bool = True):
    """
    Decorator that sets a specific object as active before running a function,
    then restores the original selection state afterward.
    
    Args:
        object_name: Either:
            - str: Name of the object to make active
            - None: Extract object name from function parameter
        param_name: Name of the function parameter containing the object name
                   (only used when object_name is None)
        restore_selection: Whether to restore the original selection state
        
    Returns:
        Decorator function
        
    Raises:
        ObjectNotFoundError: When the specified object doesn't exist
        
    Example:
        # Fixed object name
        @with_active_object("Camera")
        def move_camera():
            bpy.ops.transform.translate(value=(0, 0, 5))
            
        # Object name from parameter
        @with_active_object()
        def transform_object(object_name: str, translation):
            bpy.ops.transform.translate(value=translation)
            
        # Custom parameter name
        @with_active_object(param_name="obj_name")
        def scale_object(obj_name: str, scale_factor):
            bpy.ops.transform.resize(value=(scale_factor,) * 3)
    """
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Determine object name
            target_object_name = None
            
            if isinstance(object_name, str):
                # Fixed object name provided
                target_object_name = object_name
            else:
                # Extract from function parameters
                if param_name in kwargs:
                    target_object_name = kwargs[param_name]
                else:
                    # Try to get from positional args using function signature
                    import inspect
                    sig = inspect.signature(func)
                    param_names = list(sig.parameters.keys())
                    
                    if param_name in param_names:
                        param_index = param_names.index(param_name)
                        if param_index < len(args):
                            target_object_name = args[param_index]
                
                if target_object_name is None:
                    raise ValueError(
                        f"Could not find object name parameter '{param_name}' "
                        f"in function '{func.__name__}'"
                    )
            
            # Validate object exists
            existing, missing = validate_objects_exist(target_object_name)
            if missing:
                raise ObjectNotFoundError(
                    f"Object '{target_object_name}' not found for function '{func.__name__}'"
                )
            
            # Store current selection state
            original_selected = list(bpy.context.selected_objects) if restore_selection else []
            original_active = bpy.context.active_object
            
            try:
                # Set new active object
                target_obj = bpy.data.objects[target_object_name]
                
                # Clear selection and select target object
                bpy.ops.object.select_all(action='DESELECT')
                target_obj.select_set(True)
                bpy.context.view_layer.objects.active = target_obj
                
                # Execute the original function
                result = func(*args, **kwargs)
                
                return result
                
            finally:
                # Restore original selection state
                if restore_selection:
                    # Clear current selection
                    bpy.ops.object.select_all(action='DESELECT')
                    
                    # Restore original selection
                    for obj in original_selected:
                        if obj and obj.name in bpy.data.objects:  # Check object still exists
                            obj.select_set(True)
                    
                    # Restore original active object
                    if original_active and original_active.name in bpy.data.objects:
                        bpy.context.view_layer.objects.active = original_active
                    elif original_selected:
                        # If original active no longer exists, use first selected
                        bpy.context.view_layer.objects.active = original_selected[0]
                    else:
                        bpy.context.view_layer.objects.active = None
                        
        return wrapper
    
    # Handle case where decorator is used without parentheses
    if callable(object_name):
        # @with_active_object (without parentheses)
        func = object_name
        object_name = None
        return decorator(func)
    else:
        # @with_active_object(...) (with parentheses)
        return decorator


def with_selected_objects(*object_names: str, clear_existing: bool = True):
    """
    Decorator that selects specific objects before running a function,
    then restores the original selection state afterward.
    
    Args:
        *object_names: Names of objects to select
        clear_existing: Whether to clear existing selection first
        
    Returns:
        Decorator function
        
    Raises:
        ObjectNotFoundError: When any specified objects don't exist
        
    Example:
        @with_selected_objects("Cube", "Sphere", "Cylinder")
        def delete_selected():
            bpy.ops.object.delete()
            
        @with_selected_objects("Camera", "Light", clear_existing=False)
        def add_to_selection():
            # Adds Camera and Light to existing selection
            pass
    """
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if not object_names:
                raise ValueError("At least one object name must be provided")
            
            # Validate all objects exist
            existing, missing = validate_objects_exist(list(object_names))
            if missing:
                raise ObjectNotFoundError(
                    f"Objects not found for function '{func.__name__}': {missing}"
                )
            
            # Store current selection state
            original_selected = list(bpy.context.selected_objects)
            original_active = bpy.context.active_object
            
            try:
                # Clear existing selection if requested
                if clear_existing:
                    bpy.ops.object.select_all(action='DESELECT')
                
                # Select target objects
                for obj_name in object_names:
                    obj = bpy.data.objects[obj_name]
                    obj.select_set(True)
                    
                    # Set first object as active if no active object
                    if bpy.context.active_object is None:
                        bpy.context.view_layer.objects.active = obj
                
                # Execute the original function
                result = func(*args, **kwargs)
                
                return result
                
            finally:
                # Restore original selection state
                bpy.ops.object.select_all(action='DESELECT')
                
                # Restore original selection
                for obj in original_selected:
                    if obj and obj.name in bpy.data.objects:
                        obj.select_set(True)
                
                # Restore original active object
                if original_active and original_active.name in bpy.data.objects:
                    bpy.context.view_layer.objects.active = original_active
                elif original_selected:
                    bpy.context.view_layer.objects.active = original_selected[0]
                else:
                    bpy.context.view_layer.objects.active = None
                    
        return wrapper
    return decorator


class SelectionContext:
    """
    Context manager for temporary object selection.
    
    Example:
        with SelectionContext("Cube", active=True):
            bpy.ops.transform.translate(value=(0, 0, 1))
            
        with SelectionContext(["Cube", "Sphere"], clear_existing=True):
            bpy.ops.object.delete()
    """
    
    def __init__(self, 
                 objects: Union[str, List[str]], 
                 active: bool = False,
                 clear_existing: bool = True):
        """
        Initialize selection context.
        
        Args:
            objects: Object name(s) to select
            active: If True, make the first object active
            clear_existing: Whether to clear existing selection
        """
        if isinstance(objects, str):
            objects = [objects]
        
        self.object_names = objects
        self.make_active = active
        self.clear_existing = clear_existing
        
        self.original_selected = []
        self.original_active = None
    
    def __enter__(self):
        # Validate objects exist
        existing, missing = validate_objects_exist(self.object_names)
        if missing:
            raise ObjectNotFoundError(f"Objects not found: {missing}")
        
        # Store current state
        self.original_selected = list(bpy.context.selected_objects)
        self.original_active = bpy.context.active_object
        
        # Clear existing selection if requested
        if self.clear_existing:
            bpy.ops.object.select_all(action='DESELECT')
        
        # Select target objects
        for obj_name in self.object_names:
            obj = bpy.data.objects[obj_name]
            obj.select_set(True)
            
            # Set as active if requested and no current active
            if self.make_active and bpy.context.active_object is None:
                bpy.context.view_layer.objects.active = obj
                self.make_active = False  # Only set first object as active
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore original selection
        bpy.ops.object.select_all(action='DESELECT')
        
        for obj in self.original_selected:
            if obj and obj.name in bpy.data.objects:
                obj.select_set(True)
        
        # Restore original active object
        if self.original_active and self.original_active.name in bpy.data.objects:
            bpy.context.view_layer.objects.active = self.original_active
        elif self.original_selected:
            bpy.context.view_layer.objects.active = self.original_selected[0]
        else:
            bpy.context.view_layer.objects.active = None 