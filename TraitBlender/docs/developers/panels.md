# Panels

For official Blender documentation on Panels, see: [Blender Python API - Panels](https://docs.blender.org/api/current/bpy.types.Panel.html)

---

## Overview

Panels in TraitBlender define the user interface that appears in Blender's sidebar. Panels provide the GUI layer that users interact with, calling operators and displaying properties. Like operators, panels are a standard Blender add-on pattern.

**Key Principle**: Panels are the visual interface that connects users to TraitBlender functionality. They display properties, provide buttons that call operators, and organize the UI into logical sections.

---

## Architecture: Panels as UI Layer

Panels in TraitBlender serve as the UI layer in the architecture:

- **`core/`**: Contains business logic and data structures
- **`ui/operators/`**: Contains operators that execute functionality
- **`ui/panels/`**: Contains panels that display the UI and call operators

Panels in `ui/panels/` typically follow this pattern:

1. **Access TraitBlender data** through `bpy.context.scene.traitblender_*`
2. **Display properties** using `layout.prop()`
3. **Call operators** using `layout.operator()`
4. **Organize UI** using layout containers (rows, boxes, separators, etc...)

**Example**:
```python
# ui/panels/main_panel.py
class TRAITBLENDER_PT_main_panel(Panel):
    def draw(self, context):
        layout = self.layout
        # Call an operator (note that Blender recognizes that traitblender.setup_scene is is already in bpy.ops)
        layout.operator("traitblender.setup_scene", text="Import Museum")
        # Display a property
        layout.prop(context.scene.traitblender_setup, "config_file", text="Config File")
```

---

## Naming Conventions

### Class Names

All TraitBlender panels follow the naming pattern:

```python
TRAITBLENDER_PT_<panel_name>
```

**Examples**:
- `TRAITBLENDER_PT_main_panel`
- `TRAITBLENDER_PT_config_panel`
- `TRAITBLENDER_PT_datasets_panel`

**Pattern**: `TRAITBLENDER_PT_` prefix + snake_case panel name

### Panel IDs (`bl_idname`)

Panel IDs use the same format as class names:

```python
bl_idname = "TRAITBLENDER_PT_<panel_name>"
```

**Examples**:
- `"TRAITBLENDER_PT_main_panel"`
- `"TRAITBLENDER_PT_config_panel"`

**Note**: Unlike operators, panel IDs typically match the class name exactly.

---

## Standard Panel Structure

### Basic Template

```python
import bpy
from bpy.types import Panel

class TRAITBLENDER_PT_example(Panel):
    bl_label = "Example Panel"
    bl_idname = "TRAITBLENDER_PT_example"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TraitBlender'
    
    def draw(self, context):
        layout = self.layout
        # UI elements go here
```

### Required Properties

- **`bl_label`**: Display name shown in the panel header
- **`bl_idname`**: Unique identifier for the panel
- **`bl_space_type`**: Where the panel appears (usually `'VIEW_3D'` for 3D viewport)
- **`bl_region_type`**: Region type (usually `'UI'` for sidebar)
- **`bl_category`**: Tab category in the sidebar (usually `'TraitBlender'`)

### The `draw()` Method

The `draw()` method is called by Blender to render the panel UI. It receives `context` (which is `bpy.context`) and uses `self.layout` to build the UI:

```python
def draw(self, context):
    layout = self.layout  # Get the layout manager
    
    # Access TraitBlender data
    config = context.scene.traitblender_config
    
    # Build UI elements
    layout.operator("traitblender.some_operator")
    layout.prop(config, "some_property")
```

---

## Accessing TraitBlender Data

Panels access TraitBlender data through `context.scene` properties:

```python
def draw(self, context):
    # ✅ Correct: Access through context
    config = context.scene.traitblender_config
    dataset = context.scene.traitblender_dataset
    setup = context.scene.traitblender_setup
    
    # Display properties
    layout.prop(config, "some_property")
    layout.prop(dataset, "sample")
```

---

## Layout System

Blender's layout system provides methods to organize UI elements:

### Basic Layout Methods

```python
def draw(self, context):
    layout = self.layout
    
    # Create a row (horizontal layout)
    row = layout.row()
    row.operator("traitblender.operator1")
    row.operator("traitblender.operator2")
    
    # Create a row with alignment
    row = layout.row(align=True)  # Aligns elements tightly
    
    # Create a box (grouped section)
    box = layout.box()
    box.label(text="Section Title")
    box.prop(config, "property")
    
    # Add a separator (spacing)
    layout.separator()
```

---

## TraitBlender Panel System

TraitBlender uses a 7-panel system, numbered 1-7, all in the `'TraitBlender'` category:

1. **Museum Setup** (`TRAITBLENDER_PT_main_panel`): Scene setup and configuration loading
2. **Configuration** (`TRAITBLENDER_PT_config_panel`): Configuration settings display
3. **Morphospaces** (`TRAITBLENDER_PT_morphospaces_panel`): Morphospace selection
4. **Datasets** (`TRAITBLENDER_PT_datasets_panel`): Dataset import and sample generation
5. **Orientations** (`TRAITBLENDER_PT_orientations_panel`): Object orientation settings
6. **Transforms** (`TRAITBLENDER_PT_transforms_panel`): Transform pipeline controls
7. **Imaging** (`TRAITBLENDER_PT_imaging_panel`): Imaging pipeline controls

All panels use:
- `bl_space_type = 'VIEW_3D'`
- `bl_region_type = 'UI'`
- `bl_category = 'TraitBlender'`
---

## Calling Operators from Panels

Panels call operators using `layout.operator()`:

```python
def draw(self, context):
    layout = self.layout
    
    # Basic operator call
    layout.operator("traitblender.setup_scene", text="Import Museum")
    
    # Operator with icon
    layout.operator("traitblender.clear_scene", text="Clear Scene", icon='TRASH')
    
    # Operators in a row
    row = layout.row(align=True)
    row.operator("traitblender.run_pipeline", text="Run Pipeline", icon='PLAY')
    row.operator("traitblender.undo_pipeline", text="Undo Pipeline", icon='LOOP_BACK')
```

The operator ID (`"traitblender.setup_scene"`) must match the operator's `bl_idname`.

---

## Displaying Properties

Panels display properties using `layout.prop()`:

```python
def draw(self, context):
    layout = self.layout
    config = context.scene.traitblender_config
    dataset = context.scene.traitblender_dataset
    
    # Display a property with custom label
    layout.prop(config.orientations, "object_location_origin", text="Object Location Origin")
    
    # Display a property (uses property's default label)
    layout.prop(dataset, "sample", text="Sample")
    
    # Display nested properties
    layout.prop(config.world, "color", text="World Color")
```

---

## Creating a New Panel

### Step-by-Step Guide

1. **Add the panel class** to `ui/panels/main_panel.py`:

```python
import bpy
from bpy.types import Panel

class TRAITBLENDER_PT_my_panel(Panel):
    bl_label = "My Panel"
    bl_idname = "TRAITBLENDER_PT_my_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TraitBlender'
    
    def draw(self, context):
        layout = self.layout
        # Your UI code here
        layout.operator("traitblender.some_operator")
```

2. **Register the panel** in `ui/panels/__init__.py`:

```python
from .main_panel import TRAITBLENDER_PT_my_panel

classes = [
    # ... existing panels ...
    TRAITBLENDER_PT_my_panel,
]
```

3. **The panel will appear** in Blender's sidebar under the "TraitBlender" tab.

---

## Helper Methods

Panels can define helper methods to organize complex UI drawing:

```python
class TRAITBLENDER_PT_config_panel(Panel):
    def draw(self, context):
        layout = self.layout
        config = context.scene.traitblender_config
        
        # Use helper method
        for section_name, section_obj in config.get_config_sections().items():
            self._draw_config_section(layout, section_name, section_obj)
    
    def _draw_config_section(self, layout, section_name, section_obj):
        """Helper method to draw a config section"""
        box = layout.box()
        box.label(text=section_name.replace('_', ' ').title())
        # ... draw section content ...
```

Helper methods are useful for:
- Repeating UI patterns
- Organizing complex layouts
- Sharing code between panels

