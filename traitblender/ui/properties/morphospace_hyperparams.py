"""
Morphospace hyperparameters property groups for GUI editing.

Dynamically generates PropertyGroups from each morphospace's HYPERPARAMETERS export.
Values read/write the morphospace config. Used in the morphospaces panel.
"""

import bpy
from bpy.props import IntProperty, FloatProperty, BoolProperty

# Registry of dynamically generated classes: morphospace_name -> (class, scene_attr_name)
_hyperparam_editor_registry = {}
_editors_built = False
_pending_timer = None


def _make_prop_getter(morphospace_name, key, default):
    """Closure for getter that reads from config."""
    def getter(self):
        try:
            config = bpy.context.scene.traitblender_config.morphospace
            return config.get_hyperparam(morphospace_name, key)
        except Exception:
            return default
    return getter


def _make_prop_setter(morphospace_name, key):
    """Closure for setter that writes to config."""
    def setter(self, value):
        try:
            config = bpy.context.scene.traitblender_config.morphospace
            config.set_hyperparam(morphospace_name, key, value)
        except Exception:
            pass
    return setter


def create_hyperparams_property_group(morphospace_name, hyperparams_dict):
    """
    Create a PropertyGroup class for a morphospace from its HYPERPARAMETERS dict.
    Each prop has get/set that read/write the morphospace config.
    """
    safe_name = morphospace_name.replace(".", "_").replace(" ", "_")
    class_name = f"TRAITBLENDER_PG_morphospace_hyperparams_{safe_name}"

    annotations = {}
    for key, default in hyperparams_dict.items():
        getter = _make_prop_getter(morphospace_name, key, default)
        setter = _make_prop_setter(morphospace_name, key)
        display_name = key.replace("_", " ").title()

        if isinstance(default, bool):
            annotations[key] = BoolProperty(
                name=display_name, default=default, get=getter, set=setter
            )
        elif isinstance(default, int):
            annotations[key] = IntProperty(
                name=display_name, default=default, min=1, soft_max=1000,
                get=getter, set=setter
            )
        elif isinstance(default, float):
            annotations[key] = FloatProperty(
                name=display_name, default=default, min=0.0001, max=1000.0,
                step=0.01, precision=4, get=getter, set=setter
            )
        else:
            annotations[key] = FloatProperty(
                name=display_name, default=float(default) if default else 0.0,
                get=getter, set=setter
            )

    cls = type(
        class_name,
        (bpy.types.PropertyGroup,),
        {"__annotations__": annotations, "__module__": __name__},
    )
    return cls


def _do_build_editors():
    """Actually build and register editors. Must run outside draw/readonly context."""
    global _hyperparam_editor_registry, _editors_built
    from ...core.morphospaces import (
        list_morphospaces,
        get_hyperparameters_for_morphospace,
        get_morphospace_display_name,
    )

    _hyperparam_editor_registry.clear()
    for folder_name in list_morphospaces():
        hyperparams = get_hyperparameters_for_morphospace(folder_name)
        if not hyperparams:
            continue

        identifier = get_morphospace_display_name(folder_name)
        cls = create_hyperparams_property_group(identifier, hyperparams)
        bpy.utils.register_class(cls)

        safe_name = identifier.replace(".", "_").replace(" ", "_")
        attr_name = f"traitblender_hyperparams_{safe_name}"

        setattr(bpy.types.Scene, attr_name, bpy.props.PointerProperty(type=cls))
        _hyperparam_editor_registry[identifier] = (cls, attr_name)
    _editors_built = True


def _deferred_build_timer():
    """Timer callback: build editors when not in readonly draw context."""
    global _pending_timer
    _do_build_editors()
    if _pending_timer:
        try:
            bpy.app.timers.unregister(_deferred_build_timer)
        except Exception:
            pass
        _pending_timer = None
    # Trigger redraw so panel shows hyperparams
    try:
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                area.tag_redraw()
    except Exception:
        pass
    return None  # Don't repeat


def _ensure_editors_built():
    """Build editors on first use. Uses timer if called from readonly (draw) context."""
    global _editors_built, _pending_timer
    if _editors_built:
        return
    try:
        _do_build_editors()
    except RuntimeError as e:
        if "readonly" in str(e).lower() and _pending_timer is None:
            _pending_timer = bpy.app.timers.register(_deferred_build_timer, first_interval=0.1)
        else:
            raise


def build_hyperparam_editors():
    """Build editors (used for explicit register-time init if needed)."""
    _ensure_editors_built()


def unbuild_hyperparam_editors():
    """Unregister dynamic classes and remove scene props. Call at addon unregister."""
    global _hyperparam_editor_registry, _editors_built, _pending_timer
    if _pending_timer:
        try:
            bpy.app.timers.unregister(_deferred_build_timer)
        except Exception:
            pass
        _pending_timer = None
    for morphospace_name, (cls, attr_name) in list(_hyperparam_editor_registry.items()):
        try:
            delattr(bpy.types.Scene, attr_name)
        except Exception:
            pass
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass
    _hyperparam_editor_registry.clear()
    _editors_built = False


def get_hyperparam_editor_for(context, morphospace_name):
    """
    Get the scene's editor PropertyGroup for a morphospace, or None.
    Builds editors lazily on first use (avoids policy violation at addon load).
    """
    _ensure_editors_built()
    if morphospace_name not in _hyperparam_editor_registry:
        return None
    _, attr_name = _hyperparam_editor_registry[morphospace_name]
    return getattr(context.scene, attr_name, None)


def get_hyperparam_keys_for(morphospace_identifier):
    """Get ordered list of hyperparam keys for a morphospace."""
    _ensure_editors_built()
    if morphospace_identifier not in _hyperparam_editor_registry:
        return []
    from ...core.morphospaces import get_hyperparameters_for_morphospace
    return list(get_hyperparameters_for_morphospace(morphospace_identifier).keys())
