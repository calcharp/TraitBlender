import random
import inspect
import bpy
import copy
from .registry import TRANSFORMS
from ..helpers import validate_config_path, get_config_path_info

class Transform:
    """
    A general transform that randomizes the value of a property using a specified sampler function.
    Caches the original value for undoing.
    
    Args:
        property_path (str): Relative property path (e.g., 'world.color').
        sampler_name (str): Name of the sampler function from TRANSFORMS registry.
        params (dict): Dictionary of parameters to pass to the sampler function.
    
    Call the transform to apply it: transform()
    Use undo() to revert.
    """
    def __init__(self, property_path: str, sampler_name: str, params: dict = None):
        # Input validation
        if not isinstance(property_path, str):
            raise TypeError(f"property_path must be a string, got {type(property_path)}")
        if not isinstance(sampler_name, str):
            raise TypeError(f"sampler_name must be a string, got {type(sampler_name)}")
        
        self.property_path = "bpy.context.scene.traitblender_config." + property_path
        self.sampler_name = sampler_name
        self.params = params or {}
        self._cache_stack = []  # Stack to store previous values
        
        # Validate sampler exists
        if sampler_name not in TRANSFORMS:
            raise ValueError(f"Unknown sampler '{sampler_name}'. Available: {list(TRANSFORMS.keys())}")
        
        # Validate property path exists in config
        if not validate_config_path(property_path):
            # Get helpful error information
            path_info = get_config_path_info(property_path)
            if path_info['error']:
                raise ValueError(f"Invalid property path '{property_path}': {path_info['error']}")
            else:
                available_sections = path_info.get('sections', [])
                if available_sections:
                    raise ValueError(f"Property path '{property_path}' not found. Available sections: {available_sections}")
                else:
                    raise ValueError(f"Property path '{property_path}' not found. No config sections available - run setup scene first.")

    def _get_property_value(self):
        """Get the current value of the property."""
        try:
            value = eval(self.property_path, {"bpy": bpy})
            # Ensure we get the actual value, not a property reference
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # Convert to tuple to get actual values
                return tuple(value)
            return value
        except Exception as e:
            raise RuntimeError(f"Failed to get property '{self.property_path}': {e}")

    def _set_property_value(self, value):
        """Set the value of the property."""
        try:
            exec(f"{self.property_path} = value", {"bpy": bpy, "value": value})
        except Exception as e:
            raise RuntimeError(f"Failed to set property '{self.property_path}' to value '{value}': {e}")

    def _call_sampler(self):
        """Call the sampler function with the provided parameters using introspection."""
        sampler = TRANSFORMS[self.sampler_name]
        
        # Get function signature
        sig = inspect.signature(sampler)
        
        try:
            # Try to bind all arguments
            bound_args = sig.bind(**self.params)
            bound_args.apply_defaults()
        except TypeError as e:
            # If binding fails, provide a more helpful error message
            required_params = [name for name, param in sig.parameters.items() 
                             if param.default == inspect.Parameter.empty]
            raise ValueError(f"Invalid parameters for sampler '{self.sampler_name}'. "
                           f"Required: {required_params}, Provided: {list(self.params.keys())}. "
                           f"Error: {e}")
        
        # Call with positional arguments in correct order
        return sampler(*bound_args.args, **bound_args.kwargs)

    def __call__(self):
        """Apply the transform to the property."""
        print(f"DEBUG: Starting transform for {self.property_path}")
        
        # Get current value BEFORE applying transform
        current_value = copy.deepcopy(self._get_property_value())
        print(f"DEBUG: Got current value: {current_value}")
        
        # Cache the current value (it will become the "previous" value for next time)
        if len(self._cache_stack) == 0:  # First application - store original
            print(f"Caching starting value: {current_value}")
        else:
            print(f"Storing new value: {current_value}, previous value: {self._cache_stack[-1]}")
        
        # Cache a copy of the value, not the reference
        if hasattr(current_value, '__iter__') and not isinstance(current_value, str):
            # For iterables (tuples, lists, vectors), create a deep copy
            if hasattr(current_value, 'copy'):
                cached_value = current_value.copy()
            else:
                cached_value = copy.deepcopy(current_value)
        else:
            # For scalars, just copy the value
            cached_value = current_value
        
        print(f"DEBUG: Caching value: {cached_value}")
        self._cache_stack.append(cached_value)
        print("Cache stack: ", self._cache_stack, sep="\n\t")
        
        # Sample new value
        new_value = self._call_sampler()
        print(f"New sampled value: {new_value}")
        
        # Apply the new value
        print(f"DEBUG: Setting property to: {new_value}")
        self._set_property_value(new_value)
        
        # Verify the value was set
        verify_value = self._get_property_value()
        print(f"DEBUG: Property after setting: {verify_value}")
        
        # Update view layer to see changes immediately
        bpy.context.view_layer.update()
        return new_value

    def undo(self):
        """Revert the property to the previous value in the stack."""
        if not self._cache_stack:
            print("No cached values to undo")
            return
        
        try:
            # Pop the previous value from stack
            previous_value = self._cache_stack.pop()
            print(f"Undoing: setting {self.property_path} back to {previous_value}")
            self._set_property_value(previous_value)
            current_value = self._get_property_value()
            print(f"Undo successful: {self.property_path} = {current_value}")
            # Update view layer to see changes immediately
            bpy.context.view_layer.update()
        except Exception as e:
            print(f"Undo failed: {e}")
            raise RuntimeError(f"Failed to undo transform: {e}")

    def undo_all(self):
        """Revert the property to the original value (first cached value)."""
        if not self._cache_stack:
            print("No cached values to undo")
            return
        
        try:
            # Get the original value (first in stack)
            original_value = self._cache_stack[0]
            print(f"Undoing all: setting {self.property_path} back to original {original_value}")
            self._set_property_value(original_value)
            current_value = self._get_property_value()
            print(f"Undo all successful: {self.property_path} = {current_value}")
            # Clear the stack
            self._cache_stack.clear()
            # Update view layer to see changes immediately
            bpy.context.view_layer.update()
        except Exception as e:
            print(f"Undo all failed: {e}")
            raise RuntimeError(f"Failed to undo all transforms: {e}")

    def get_history(self):
        """Get the history of values (original + all applied values)."""
        return self._cache_stack.copy()

    def __repr__(self):
        return f"Transform(property_path='{self.property_path}', sampler_name='{self.sampler_name}', params={self.params})" 