import inspect
from ..helpers import get_bpy_prop_from_type_hint
from .registry import TRANSFORMS

def register_transform(key):
    def decorator(func):
        sig = inspect.signature(func)
        for name, param in sig.parameters.items():
            if param.annotation is inspect.Parameter.empty:
                raise TypeError(f"All arguments for sampler '{key}' must have type hints. Missing for '{name}'.")
            # This will raise if not allowed
            get_bpy_prop_from_type_hint(param.annotation)
        # Store a factory in the registry
        def factory(*args, **kwargs):
            return func  # For now, just return the function; can wrap/partial if needed
        TRANSFORMS[key] = factory
        return func
    return decorator 