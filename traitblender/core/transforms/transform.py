"""
Transform class: samples a value and assigns it to a property path.
"""

import copy
import bpy

from .samplers import SAMPLERS, SAMPLER_ALLOWED_PATHS


def _resolve_path(path):
    """Resolve path to config property."""
    return "bpy.context.scene.traitblender_config." + path


def _parse_component_path(path):
    """If path has 3+ parts and last is numeric, return (parent_path, index). Else None."""
    parts = path.split(".")
    if len(parts) >= 3 and parts[-1].isdigit():
        return ".".join(parts[:-1]), int(parts[-1])
    return None


class Transform:
    """
    A transform samples a new value and assigns it to a property path.
    Caches the previous value for undo.
    """

    def __init__(self, property_path: str, sampler_name: str, params: dict = None):
        if not isinstance(property_path, str):
            raise TypeError(f"property_path must be a string, got {type(property_path)}")
        if not isinstance(sampler_name, str):
            raise TypeError(f"sampler_name must be a string, got {type(sampler_name)}")

        allowed = SAMPLER_ALLOWED_PATHS.get(sampler_name, [])
        if property_path not in allowed:
            raise ValueError(
                f"Property path '{property_path}' not allowed for sampler '{sampler_name}'. "
                f"Allowed: {allowed}"
            )
        if sampler_name not in SAMPLERS:
            raise ValueError(
                f"Unknown sampler '{sampler_name}'. Available: {list(SAMPLERS.keys())}"
            )

        self.property_path = property_path
        self.sampler_name = sampler_name
        self.params = params or {}
        self._full_path = _resolve_path(property_path)
        self._cache_stack = []

    def _get_property_value(self):
        try:
            parsed = _parse_component_path(self.property_path)
            if parsed:
                parent_path, idx = parsed
                full_parent = _resolve_path(parent_path)
                vec = eval(full_parent, {"bpy": bpy})
                arr = list(vec) if hasattr(vec, "__iter__") and not isinstance(vec, str) else [vec]
                return arr[idx] if idx < len(arr) else 0.0
            value = eval(self._full_path, {"bpy": bpy})
            if hasattr(value, "__iter__") and not isinstance(value, str):
                return tuple(value)
            return value
        except Exception as e:
            raise RuntimeError(f"Failed to get '{self.property_path}': {e}")

    def _set_property_value(self, value):
        try:
            parsed = _parse_component_path(self.property_path)
            if parsed:
                parent_path, idx = parsed
                full_parent = _resolve_path(parent_path)
                vec = eval(full_parent, {"bpy": bpy})
                arr = list(vec) if hasattr(vec, "__iter__") and not isinstance(vec, str) else [vec]
                arr = arr + [0.0] * (idx - len(arr) + 1) if idx >= len(arr) else arr
                arr[idx] = float(value)
                exec(f"{full_parent} = tuple(arr)", {"bpy": bpy, "arr": arr, "tuple": tuple})
            else:
                exec(f"{self._full_path} = value", {"bpy": bpy, "value": value})
        except Exception as e:
            raise RuntimeError(f"Failed to set '{self.property_path}' to {value}: {e}")

    def _call_sampler(self):
        sampler = SAMPLERS[self.sampler_name]
        return sampler(**self.params)

    def __call__(self):
        current_value = copy.deepcopy(self._get_property_value())
        if hasattr(current_value, "__iter__") and not isinstance(current_value, str):
            cached_value = current_value.copy() if hasattr(current_value, "copy") else copy.deepcopy(current_value)
        else:
            cached_value = current_value
        self._cache_stack.append(cached_value)

        new_value = self._call_sampler()
        self._set_property_value(new_value)
        bpy.context.view_layer.update()
        print(f"{self.property_path}: {current_value} → {new_value}")
        return new_value

    def undo(self):
        if not self._cache_stack:
            return
        try:
            current_value = self._get_property_value()
            previous_value = self._cache_stack.pop()
            self._set_property_value(previous_value)
            bpy.context.view_layer.update()
            print(f"{self.property_path}: {current_value} ← {previous_value}")
        except Exception as e:
            raise RuntimeError(f"Failed to undo transform: {e}")

    def undo_all(self):
        if not self._cache_stack:
            return
        try:
            current_value = self._get_property_value()
            original_value = self._cache_stack[0]
            self._set_property_value(original_value)
            self._cache_stack.clear()
            bpy.context.view_layer.update()
            print(f"{self.property_path}: {current_value} ← {original_value} (original)")
        except Exception as e:
            raise RuntimeError(f"Failed to undo all: {e}")

    def get_history(self):
        return self._cache_stack.copy()

    def __str__(self):
        param_str = ", ".join(f"{k}={v}" for k, v in self.params.items())
        return f"{self.property_path} ~ {self.sampler_name}({param_str})"

    def __repr__(self):
        return f"Transform('{self.property_path}', '{self.sampler_name}', {self.params})"

    def to_dict(self):
        serializable_cache = []
        for item in self._cache_stack:
            serializable_cache.append(list(item) if isinstance(item, tuple) else item)
        return {
            "property_path": self.property_path,
            "sampler_name": self.sampler_name,
            "params": self.params.copy(),
            "_cache_stack": serializable_cache,
        }

    @classmethod
    def from_dict(cls, d):
        transform = cls(
            property_path=d["property_path"],
            sampler_name=d["sampler_name"],
            params=d.get("params", {}),
        )
        if "_cache_stack" in d and d["_cache_stack"]:
            cache = []
            for item in d["_cache_stack"]:
                cache.append(tuple(item) if isinstance(item, list) else item)
            transform._cache_stack = cache
        return transform
