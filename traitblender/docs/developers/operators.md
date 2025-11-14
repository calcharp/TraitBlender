# Operators

For official Blender documentation on Operators, see: [Blender Python API - Operators](https://docs.blender.org/api/current/bpy.types.Operator.html)

---

## Overview

Operators are the standard way all Blender add-ons provide functionality. Instead of using standard Python functions, Blender add-ons use operators (accessed through `bpy.ops`) for several important reasons:

1. **GUI and API Integration**: Operators provide a unified interface that works seamlessly between the GUI (buttons, menus) and programmatic API access. The same operator can be called from a button click or from Python code.

2. **Automatic Synchronous Handling**: Blender's operator system automatically handles synchronous operation issues, ensuring operations complete properly and the scene state is consistent.

3. **Undo/Redo Support**: Operators integrate with Blender's undo/redo system when using `bl_options = {'REGISTER', 'UNDO'}`.

4. **Error Reporting**: Operators have built-in error reporting through `self.report()`, which displays messages in Blender's UI.

5. **Modal Operations**: Operators support modal execution for interactive operations (file browsers, confirmation dialogs, etc.).

**TraitBlender Convention**: TraitBlender follows this standard Blender pattern. All TraitBlender functionality that needs to be accessible from both GUI and API is implemented as operators, accessed through `bpy.ops.traitblender.*`.

### Architecture: Operators as Thin Wrappers

TraitBlender's architecture separates core business logic from user-facing operators:

- **`core/`**: Contains the primary business logic, data structures, and algorithms (configuration system, datasets, transforms, morphospaces, positioning, helpers)
- **`ui/operators/`**: Contains thin operator wrappers that provide the Blender operator interface (`bpy.ops.traitblender.*`)

Operators in `ui/operators/` typically follow this pattern:

1. **Access TraitBlender data** through `context.scene.traitblender_*`
2. **Call methods or functions** from `core/` modules
3. **Handle error reporting** and return status codes

**Example**:
```python
# ui/operators/transforms_operators.py
class TRAITBLENDER_OT_run_pipeline(Operator):
    def execute(self, context):
        # Access config (which is defined in core/config/)
        transforms_config = context.scene.traitblender_config.transforms
        # Call the run() method (implemented in core/config/config_templates/transforms.py)
        results = transforms_config.run()
        return {'FINISHED'}
```

This separation keeps core logic independent of Blender's operator system, making it easier to test, reuse, and maintain.

---

## Naming Conventions

### Class Names vs. `bpy.ops` Access

Operators have two different names that serve different purposes:

1. **Class Name** (for Python code): Long, descriptive identifier
2. **Operator ID** (`bl_idname`): Short identifier used in `bpy.ops`

### Class Names

All TraitBlender operators follow the naming pattern:

```python
TRAITBLENDER_OT_<action_name>
```

**Examples**:
- `TRAITBLENDER_OT_setup_scene`
- `TRAITBLENDER_OT_generate_morphospace_sample`
- `TRAITBLENDER_OT_run_pipeline`

**Pattern**: `TRAITBLENDER_OT_` prefix + snake_case action name

**Purpose**: Used in Python code when defining and registering the operator class.

### Operator IDs (`bl_idname`)

Operator IDs use the format:

```python
bl_idname = "traitblender.<action_name>"
```

**Examples**:
- `"traitblender.setup_scene"`
- `"traitblender.generate_morphospace_sample"`
- `"traitblender.run_pipeline"`

**Pattern**: `traitblender.` prefix + dot-separated action name

**Purpose**: Used to access the operator through `bpy.ops`.

### The Mapping

When you register an operator, Blender creates a mapping between the class and the `bl_idname`:

```python
# In your operator file
class TRAITBLENDER_OT_setup_scene(Operator):
    bl_idname = "traitblender.setup_scene"  # This is what matters for bpy.ops
    # ...

# When registered, Blender maps:
# Class: TRAITBLENDER_OT_setup_scene
# → bpy.ops.traitblender.setup_scene()
```

**Important**: The `bl_idname` is what determines how you access the operator through `bpy.ops`, not the class name.

**Example**:
```python
# Class name: TRAITBLENDER_OT_setup_scene
# bl_idname: "traitblender.setup_scene"
# Access via: bpy.ops.traitblender.setup_scene()

# The class name is only used in Python code:
from ui.operators.setup_scene_operator import TRAITBLENDER_OT_setup_scene
bpy.utils.register_class(TRAITBLENDER_OT_setup_scene)

# The bl_idname is used when calling the operator:
bpy.ops.traitblender.setup_scene()  # Uses bl_idname, not class name
```

### Why Two Names?

- **Class Name**: Must be unique within Python's namespace. Uses long, descriptive names with prefixes to avoid conflicts.
- **`bl_idname`**: Must be unique within Blender's operator registry. Uses shorter, dot-separated names that are easier to type and remember.

The `bl_idname` is what users and scripts actually use when calling operators, while the class name is an internal implementation detail.

---

## Standard Operator Structure

### Basic Template

```python
import bpy
from bpy.types import Operator

class TRAITBLENDER_OT_example(Operator):
    """Brief description of what the operator does"""
    
    bl_idname = "traitblender.example"
    bl_label = "Example Operation"
    bl_description = "Detailed description of what this operator does"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        """Execute the operation"""
        try:
            # Access TraitBlender data through context
            config = context.scene.traitblender_config
            dataset = context.scene.traitblender_dataset
            
            # Perform operation
            # ...
            
            self.report({'INFO'}, "Operation completed successfully")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Operation failed: {str(e)}")
            return {'CANCELLED'}
```

### Required Properties

- **`bl_idname`**: Unique identifier for the operator (used in `bpy.ops.traitblender.<idname>()`)
- **`bl_label`**: Display name shown in UI
- **`bl_description`**: Tooltip/help text
- **`bl_options`**: Usually `{'REGISTER', 'UNDO'}` for undo support

---

## Accessing TraitBlender Data

Operators access TraitBlender data through `context.scene` properties, **not** through direct imports:

```python
def execute(self, context):
    # ✅ Correct: Access through context
    config = context.scene.traitblender_config
    dataset = context.scene.traitblender_dataset
    setup = context.scene.traitblender_setup
    
    # ❌ Incorrect: Direct imports (don't do this)
    # from core.config import TraitBlenderConfig
    # config = TraitBlenderConfig()
```

**Why?** Operators run in Blender's execution context. Accessing data through `context.scene` ensures you're working with the actual scene data that Blender knows about, not a separate instance.

---

## Error Handling and Reporting

### Using `self.report()`

Operators use `self.report()` to communicate with the user:

```python
# Success message
self.report({'INFO'}, "Operation completed successfully")

# Warning message
self.report({'WARNING'}, "Operation completed with warnings")

# Error message
self.report({'ERROR'}, "Operation failed: reason")
```

### Return Values

Operators must return status codes:

- **`{'FINISHED'}`**: Operation completed successfully
- **`{'CANCELLED'}`**: Operation was cancelled or failed
- **`{'RUNNING_MODAL'}`**: Operation is running in modal mode (for file browsers, etc.)

**Example**:
```python
def execute(self, context):
    try:
        # ... operation ...
        self.report({'INFO'}, "Success")
        return {'FINISHED'}
    except Exception as e:
        self.report({'ERROR'}, f"Failed: {e}")
        return {'CANCELLED'}  # Always return CANCELLED on error
```

---

## Creating a New Operator

### Step-by-Step Guide

1. **Create the operator file** in `ui/operators/` (e.g., `my_operator.py`)

2. **Define the operator class**:
   ```python
   import bpy
   from bpy.types import Operator
   
   class TRAITBLENDER_OT_my_operation(Operator):
       """Description of what this operator does"""
       
       bl_idname = "traitblender.my_operation"
       bl_label = "My Operation"
       bl_description = "Detailed description"
       bl_options = {'REGISTER', 'UNDO'}
       
       def execute(self, context):
           # Your implementation
           return {'FINISHED'}
   ```

3. **Register the operator** in `ui/operators/__init__.py`:
   ```python
   from . import my_operator
   
   classes = [
       # ... existing operators ...
       my_operator.TRAITBLENDER_OT_my_operation,
   ]
   ```

4. **Use the operator**:
   ```python
   bpy.ops.traitblender.my_operation()
   ```

