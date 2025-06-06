"""
TraitBlender Transform Factory

Factory system for registering and applying morphological transforms.
"""

from typing import Dict, Callable, Any, List
import bpy
import math


class TransformFactory:
    """Factory for registering and managing transform functions."""
    
    def __init__(self):
        self._transforms: Dict[str, Callable] = {}
        self._execution_order: List[str] = []
    
    def register(self, name: str):
        """Decorator to register a transform function."""
        def decorator(func: Callable):
            if name in self._transforms:
                raise ValueError(f"Transform '{name}' is already registered")
            
            self._transforms[name] = func
            self._execution_order.append(name)
            
            return func
        return decorator
    
    def execute_pipeline(self, **global_kwargs):
        """Execute all registered transforms in registration order."""
        results = {}
        
        for transform_name in self._execution_order:
            try:
                print(f"Executing transform: {transform_name}")
                
                transform_func = self._transforms[transform_name]
                
                import inspect
                sig = inspect.signature(transform_func)
                func_kwargs = {k: v for k, v in global_kwargs.items() 
                             if k in sig.parameters}
                
                result = transform_func(**func_kwargs)
                results[transform_name] = result
                
            except Exception as e:
                print(f"Error executing transform '{transform_name}': {e}")
                results[transform_name] = f"ERROR: {e}"
        
        return results


# Global factory instance
transform_factory = TransformFactory()

# Convenience decorator
register_transform = transform_factory.register


# Example transforms
@register_transform("clear_scene")
def clear_scene():
    """Remove all mesh objects from the current scene."""
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete(use_global=False)


@register_transform("lighting_setup")
def lighting_setup(key_energy: float = 50.0, fill_energy: float = 20.0):
    """Configure standard museum lighting setup."""
    key_light = bpy.data.objects.get("KeyLight")
    fill_light = bpy.data.objects.get("FillLight")
    
    if key_light and key_light.data:
        key_light.data.energy = key_energy
    
    if fill_light and fill_light.data:
        fill_light.data.energy = fill_energy






