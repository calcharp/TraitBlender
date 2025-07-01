import random
import inspect
import bpy
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
        self._cache = None
        
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
            return eval(self.property_path, {"bpy": bpy})
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
        # Cache the original value
        self._cache = self._get_property_value()
        # Sample new value
        new_value = self._call_sampler()
        self._set_property_value(new_value)
        return new_value

    def undo(self):
        """Revert the property to its original value."""
        if self._cache is not None:
            try:
                print(f"Undoing: setting {self.property_path} back to {self._cache}")
                self._set_property_value(self._cache)
                print(f"Undo successful: {self.property_path} = {self._get_property_value()}")
                self._cache = None
            except Exception as e:
                print(f"Undo failed: {e}")
                raise RuntimeError(f"Failed to undo transform: {e}")
        else:
            print("No cached value to undo")

    def __repr__(self):
        return f"Transform(property_path='{self.property_path}', sampler_name='{self.sampler_name}', params={self.params})" 