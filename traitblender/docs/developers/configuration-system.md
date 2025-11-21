# Configuration System

For Blender's property system documentation, see: [Blender Python API - Properties](https://docs.blender.org/api/current/bpy.props.html)

---

## Overview

TraitBlender's workflow begins by loading in the standard museum scene and adjusting the configuration of the scene's objects and their properties.

The Configuration System controls **how your museum scene is set up**:
- Where the camera is positioned
- How bright the lights are
- What color the background is
- How glossy the specimen mat appears
- Dozens of other scene settings



**How it works:**

- Config sections (camera, lamp, world, etc.) are defined in `core/config/config_templates/`
- Each section uses the `@register("name")` decorator to auto-register with Blender
- Properties use `get_property()` and `set_property()` to sync with actual Blender objects
- The entire config can be exported to/imported from YAML files
- All settings accessed via `bpy.context.scene.traitblender_config`

---

## Registration System

### The `@register` Decorator

Config sections are registered using `@register("name")` in `core/config/register_config.py`:

```python
@register("world")
class WorldConfig(TraitBlenderConfig):
    color: bpy.props.FloatVectorProperty(...)
    strength: bpy.props.FloatProperty(...)
```

The decorator ensures the class inherits from `TraitBlenderConfig`, registers it with Blender via `bpy.utils.register_class()`, and stores it in the global `CONFIG` dictionary as a `PointerProperty`.

### Auto-Discovery

Config files in `core/config/config_templates/` are automatically discovered using Abstract Syntax Tree (AST) parsing (see `find_registered_classes()` in `config_templates/__init__.py`). The system scans Python files for classes decorated with `@register`, which means you can add new config sections just by creating a new file with the decorator - no manual imports needed.

### Class Assembly

Once discovered, `configure_traitblender()` in `core/config/register_config.py` creates a unified config class by combining all registered sections, registers it with Blender, and attaches it to `bpy.types.Scene.traitblender_config`.

---

## TraitBlenderConfig Base Class

All config sections inherit from `TraitBlenderConfig` in `core/config/register_config.py`:

### Core Methods

The `TraitBlenderConfig` base class provides these methods (see `core/config/register_config.py` for implementation details):

**`__str__()` and `_to_yaml()`** - Converts the entire config tree to YAML format for display or export. Recursively traverses all config sections and formats properties with proper indentation. Config sections can set a `print_index` attribute to control their ordering in the YAML output (lower numbers appear first).

**`to_dict()`** - Converts the config to a nested Python dictionary. Recursively converts nested config sections and handles vectors/arrays properly. Used for serialization and export.

**`from_dict()`** - Loads config values from a nested dictionary. Recursively applies values to nested sections and silently skips invalid properties. Used when loading YAML config files.

**`get_config_sections()`** - Returns a dictionary of all nested `TraitBlenderConfig` sections. Useful for introspection and iteration over config sections.

---

## Dynamic Property System

### Getters and Setters

Config properties use dynamic getters/setters defined in `core/helpers/prop_gettersetter.py`:

```python
# In a config template:
@register("camera")
class CameraConfig(TraitBlenderConfig):
    location: bpy.props.FloatVectorProperty(
        name="Camera Location",
        get=get_property("bpy.data.objects['Camera'].location",
                        object_dependencies={"objects": ["Camera"]}),
        set=set_property("bpy.data.objects['Camera'].location",
                        object_dependencies={"objects": ["Camera"]})
    )
```

**`get_property()`** - Creates a getter function that reads from actual Blender objects. Validates that required objects (Camera, Lamp, etc.) exist in the scene, evaluates the property path (e.g., `bpy.data.objects['Camera'].location`), and returns the value or a sensible default if objects are missing. Handles enum properties by converting strings to indices.

**`set_property()`** - Creates a setter function that writes to actual Blender objects. Validates that required objects exist, converts enum indices back to string values if needed, uses `exec()` to set the property value in Blender, and warns or raises errors if objects are missing.

**Object Dependencies** - The `object_dependencies` parameter specifies which Blender objects must exist for a property to work. If any required object is missing, getters return default values and setters do nothing (preventing errors).

```python
object_dependencies = {
    "objects": ["Camera", "Lamp"],      # bpy.data.objects
    "cameras": ["Camera"],              # bpy.data.cameras
    "worlds": ["World"],                # bpy.data.worlds
    "lights": ["Lamp"],                 # bpy.data.lights
    "materials": ["mat_material"]       # bpy.data.materials
}
```

---

## Transform Pipeline Integration

The transform pipeline is integrated as a special config section in `core/config/config_templates/transforms.py`. Unlike other config sections that directly map to Blender objects, `TransformPipelineConfig` acts as a wrapper around the `TransformPipeline` class.

**How it connects:**

- Registered as `@register("transforms")` like other config sections
- Stores pipeline state as a serialized YAML string in Blender properties
- Delegates methods like `add_transform()`, `run()`, and `undo()` to the underlying `TransformPipeline` object
- Accessed via `config.transforms.add_transform(...)` just like other config properties

This allows the transform pipeline to be saved/loaded with the rest of the config while maintaining complex state (transform list, undo history, execution history) that wouldn't fit in simple Blender properties.

See [Transform Pipeline](./transform-pipeline.md) for details on how transforms work.

---

## Creating a New Config Section

### Step-by-Step Guide

**1. Create config template file** in `core/config/config_templates/`:

```python
# core/config/config_templates/my_section.py
import bpy
from ..register_config import register, TraitBlenderConfig
from ...helpers import get_property, set_property

@register("my_section")
class MySectionConfig(TraitBlenderConfig):
    print_index = 5  # Controls YAML output order (optional)
    
    my_property: bpy.props.FloatProperty(
        name="My Property",
        description="Description of property",
        default=1.0,
        min=0.0,
        get=get_property('bpy.data.objects["MyObject"].some_property',
                        object_dependencies={"objects": ["MyObject"]}),
        set=set_property('bpy.data.objects["MyObject"].some_property',
                        object_dependencies={"objects": ["MyObject"]})
    )
    
    my_color: bpy.props.FloatVectorProperty(
        name="My Color",
        description="Color property",
        default=(1.0, 1.0, 1.0),
        min=0.0,
        max=1.0,
        size=3,
        subtype='COLOR',
        get=get_property('bpy.data.materials["MyMaterial"].diffuse_color',
                        object_dependencies={"materials": ["MyMaterial"]}),
        set=set_property('bpy.data.materials["MyMaterial"].diffuse_color',
                        object_dependencies={"materials": ["MyMaterial"]})
    )
```

**2. Config section is automatically discovered** via AST parsing (no import needed)

**3. Access in code:**

```python
config = bpy.context.scene.traitblender_config
value = config.my_section.my_property
config.my_section.my_color = (1.0, 0.5, 0.0)
```

**4. YAML export includes new section:**

```yaml
---
# ... other sections ...
my_section:
  my_property: 1.0
  my_color: [1.0, 0.5, 0.0]
```


