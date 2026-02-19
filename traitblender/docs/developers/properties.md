# Properties

For official Blender documentation on Properties, see: [Blender Python API - Properties](https://docs.blender.org/api/current/bpy.props.html)

---

## Overview

Properties in TraitBlender are Blender property groups and custom properties that store TraitBlender data. Properties provide the data layer that operators and panels access through `context.scene.traitblender_*`.

**Key Principle**: Properties don't exist as standalone Python variables. They are **tied to either the scene or to particular objects**:

- **Scene-level properties**: Registered on `bpy.types.Scene` (e.g., `context.scene.traitblender_config`)
- **Object-level properties**: Registered on `bpy.types.Object` (e.g., `obj.tb_location`)

Properties are registered with Blender's type system, making them accessible throughout the add-on and persistent across Blender sessions. They become part of Blender's data model, not just temporary Python variables, so they can be saved and exported with the rest of the scene via the .blend file.

---

## Architecture: Properties as Data Layer

Properties in TraitBlender serve as the data layer in the architecture:

- **`core/`**: Contains business logic and data structures
- **`ui/operators/`**: Contains operators that execute functionality
- **`ui/panels/`**: Contains panels that display the UI
- **`ui/properties/`**: Contains property groups that store data

Properties in `ui/properties/` typically follow this pattern:

1. **Define data structures** using `bpy.types.PropertyGroup`
2. **Register with Blender** using `bpy.props.PointerProperty` or direct registration
3. **Store TraitBlender state** (configuration, datasets, setup options)
4. **Provide custom properties** on Blender objects (like `tb_location`, `tb_rotation`)

**Example**:
```python
# ui/properties/setup_properties.py
class TraitBlenderSetupProperties(bpy.types.PropertyGroup):
    config_file: StringProperty(name="Config File", default="")
    
# Registered in __init__.py:
bpy.types.Scene.traitblender_setup = bpy.props.PointerProperty(
    type=TraitBlenderSetupProperties
)
# Accessed via:
context.scene.traitblender_setup.config_file
```

---

## Property Groups

### Basic Property Group

Property groups are classes that inherit from `bpy.types.PropertyGroup`:

```python
import bpy
from bpy.props import StringProperty, EnumProperty

class TraitBlenderSetupProperties(bpy.types.PropertyGroup):
    """Property group for TraitBlender setup configuration."""
    
    config_file: StringProperty(
        name="Config File",
        description="Path to YAML configuration file",
        default="",
        subtype='FILE_PATH'
    )
    
    available_morphospaces: EnumProperty(
        name="Available Morphospaces",
        description="List of available morphospace modules",
        items=lambda self, context: self._get_morphospace_items(),
        default=0
    )
    
    def _get_morphospace_items(self):
        """Helper method for enum items."""
        # ... implementation ...
        return items
```

### Registering Property Groups

Property groups must be registered with Blender and attached to a Blender type:

```python
# In ui/properties/__init__.py
def register():
    # Register the class
    bpy.utils.register_class(TraitBlenderSetupProperties)
    
    # Attach to Scene as a PointerProperty
    bpy.types.Scene.traitblender_setup = bpy.props.PointerProperty(
        type=TraitBlenderSetupProperties
    )

def unregister():
    # Remove the property
    del bpy.types.Scene.traitblender_setup
    # Unregister the class
    bpy.utils.unregister_class(TraitBlenderSetupProperties)
```

### TraitBlender's Dynamic Config System

TraitBlender implements a **dynamic decorator-based property registration system** for the configuration file (`traitblender_config`). This system simplifies extending TraitBlender by adding new properties to the config and serializing them to YAML config files.

Instead of manually registering each config section, you use the `@register` decorator in `core/config/config_templates/`, and the system automatically discovers and registers them. See the [Configuration System](../configuration-system.md) documentation for details.

### Accessing Property Groups

Once registered, property groups are accessed through `context.scene`:

```python
# In operators or panels
def execute(self, context):
    setup = context.scene.traitblender_setup
    config_file = setup.config_file
    morphospace = setup.available_morphospaces
```

---

## TraitBlender Property Groups

TraitBlender defines several property groups registered on `bpy.types.Scene`:

- **`traitblender_setup`** (`TraitBlenderSetupProperties`): Setup configuration (config file path, morphospace selection)
- **`traitblender_config`** (`TraitBlenderConfig`): Main configuration (defined in `core/config/` using the dynamic decorator system)
- **`traitblender_dataset`** (`TRAITBLENDER_PG_dataset`): Dataset management (defined in `core/datasets/`)

---

## Property Registration Order

Properties must be registered in the correct order:

1. **Register property group classes** using `bpy.utils.register_class()`
2. **Attach property groups** using `bpy.props.PointerProperty()` or direct assignment

**Example**:
```python
def register():
    # 1. Register the class
    bpy.utils.register_class(TraitBlenderSetupProperties)
    
    # 2. Attach to Scene
    bpy.types.Scene.traitblender_setup = bpy.props.PointerProperty(
        type=TraitBlenderSetupProperties
    )
```

---

## Creating a New Property Group

### Step-by-Step Guide

1. **Create the property group class** in `ui/properties/` (e.g., `my_properties.py`):

```python
import bpy
from bpy.props import StringProperty

class TraitBlenderMyProperties(bpy.types.PropertyGroup):
    """Property group for my feature."""
    
    my_property: StringProperty(
        name="My Property",
        description="Description of my property",
        default=""
    )
```

2. **Register the property group** in `ui/properties/__init__.py`:

```python
from . import my_properties

classes = [
    # ... existing property groups ...
    my_properties.TraitBlenderMyProperties,
]

def register():
    # Register the class
    bpy.utils.register_class(my_properties.TraitBlenderMyProperties)
    
    # Attach to Scene (or another type)
    bpy.types.Scene.traitblender_my = bpy.props.PointerProperty(
        type=my_properties.TraitBlenderMyProperties
    )

def unregister():
    del bpy.types.Scene.traitblender_my
    bpy.utils.unregister_class(my_properties.TraitBlenderMyProperties)
```

3. **Access the property** in operators or panels:

```python
def execute(self, context):
    my_props = context.scene.traitblender_my
    value = my_props.my_property
```

---

## Dynamic Properties

Some properties use dynamic values (like enum items):

```python
available_morphospaces: EnumProperty(
    name="Available Morphospaces",
    items=lambda self, context: self._get_morphospace_items(),
    default=0
)

def _get_morphospace_items(self):
    """Get available morphospaces dynamically."""
    items = []
    try:
        morphospaces = list_morphospaces()  # Call core function
        for name in morphospaces:
            items.append((name, name, f"Morphospace: {name}"))
    except Exception as e:
        print(f"Error getting morphospace items: {e}")
    return items
```

The `items` callable receives `(self, context)` where `self` is the property group instance and `context` is `bpy.context`.

