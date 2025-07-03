import inspect
from ..helpers import get_bpy_prop_from_type_hint, pretty_type_hint
from .registry import TRANSFORMS

def register_transform(key):
    def decorator(func):
        sig = inspect.signature(func)
        for name, param in sig.parameters.items():
            if param.annotation is inspect.Parameter.empty:
                raise TypeError(f"All arguments for sampler '{key}' must have type hints. Missing for '{name}'.")
            # This will raise if not allowed
            get_bpy_prop_from_type_hint(param.annotation)
        # Store a flexible factory in the registry
        def factory(**factory_kwargs):
            def sampler(**sampler_kwargs):
                all_kwargs = {**factory_kwargs, **sampler_kwargs}
                return func(**all_kwargs)
            # Build docstring for the sampler
            preset = ", ".join(f"{k}={v!r}" for k, v in factory_kwargs.items()) or "None"
            remaining = [name for name in sig.parameters if name not in factory_kwargs]
            remaining_docs = [
                f"{name}: "
                f"{pretty_type_hint(sig.parameters[name].annotation)}"
                f"{'=' + str(sig.parameters[name].default) if sig.parameters[name].default is not inspect.Parameter.empty else ''}"
                for name in remaining
            ]
            params_str = ", ".join(remaining_docs) or "None"
            sampler.__doc__ = f"Presets: {preset}\nParams: {params_str}"
            return sampler
        TRANSFORMS[key] = factory
        return func
    return decorator 