# Transforms GUI - Standalone Development

This folder contains a standalone DearPyGUI application for building and managing transform pipelines in TraitBlender.

## Purpose

Develop a graphical interface for the transform pipeline system that allows users to:
- Add transforms with proper parameter input
- View and manage transforms in the pipeline
- Edit existing transforms
- Reorder transforms
- Validate parameters before adding
- Clear/reset the pipeline
- Save/load pipeline configurations

## Development Approach

1. **Standalone Development**: Build the DearPyGUI app independently without Blender dependencies
2. **Testing**: Test all functionality in isolation
3. **Integration**: Once working, integrate with TraitBlender's core transform system

## Architecture & Data Flow

### Serialization Format

The transforms pipeline is stored in TraitBlender as a YAML string in `TransformPipelineConfig.pipeline_state`. This mirrors the CSV viewer approach:

**CSV Viewer Pattern:**
```
dataset.csv (string) → pandas DataFrame → DearPyGUI table → CSV string
```

**Transforms GUI Pattern:**
```
pipeline_state (YAML string) → TransformPipeline object → DearPyGUI interface → YAML string
```

### Pipeline YAML Format

```yaml
- property_path: world.color
  sampler_name: dirichlet
  params:
    alphas: [0.3, 0.3, 0.3, 1]
- property_path: lamp.power
  sampler_name: gamma
  params:
    alpha: 2
    beta: 5
- property_path: camera.location
  sampler_name: normal
  params:
    mu: 0
    sigma: 0.1
    n: 3
```

### App Workflow

**1. Launch (Entry Point)**
```python
launch_transform_editor(pipeline_yaml_string: str) -> str | None
```
- Input: Current pipeline state as YAML string from `config.transforms.pipeline_state`
- Output: Modified YAML string (if user exports changes), or `None` (if cancelled)

**2. Internal Processing**
- Parse YAML string → list of transform dicts
- Display in DearPyGUI with editable interface
- User adds/edits/removes/reorders transforms
- Validate parameters before accepting
- Serialize back to YAML string on export

**3. Integration (Blender Side)**
```python
# In operator (e.g., edit_transforms_operator.py)
def execute(self, context):
    config = context.scene.traitblender_config
    current_state = config.transforms.pipeline_state  # Get YAML string
    
    # Launch editor (blocking call)
    new_state = launch_transform_editor(current_state)
    
    if new_state is not None:  # User exported changes
        config.transforms.pipeline_state = new_state
        self.report({'INFO'}, "Transform pipeline updated")
    else:
        self.report({'INFO'}, "Transform editing cancelled")
    
    return {'FINISHED'}
```

## Data Structures

### Transform Dictionary (per transform)
```python
{
    'property_path': str,      # e.g., "world.color"
    'sampler_name': str,       # e.g., "dirichlet"
    'params': dict             # e.g., {"alphas": [0.3, 0.3, 0.3, 1]}
}
```

### Available Samplers (from TRANSFORMS registry)
```python
{
    'uniform': {
        'params': [
            {'name': 'low', 'type': float, 'required': True},
            {'name': 'high', 'type': float, 'required': True},
            {'name': 'n', 'type': int, 'required': False, 'default': None}
        ]
    },
    'dirichlet': {
        'params': [
            {'name': 'alphas', 'type': list[float], 'required': True},
            {'name': 'n', 'type': int, 'required': False, 'default': None}
        ]
    },
    # ... etc for all 10 samplers
}
```

### Available Properties (from config sections)
```python
{
    'world': ['color', 'strength'],
    'camera': ['location', 'rotation', 'focal_length', ...],
    'lamp': ['location', 'power', 'color', ...],
    # ... etc
}
```

## Key Components to Build

### 1. Data Manager
- Parse YAML string → transform list
- Serialize transform list → YAML string
- Validate transform dicts
- Get property type info (scalar vs vector)

### 2. Transform Editor Panel
- Display current transforms in a list/table
- Select transform to edit
- Add new transform button
- Remove transform button
- Reorder transforms (up/down or drag)

### 3. Transform Builder Dialog
- Section dropdown (world, camera, lamp, etc.)
- Property dropdown (filtered by section)
- Sampler dropdown (uniform, normal, etc.)
- **Dynamic parameter inputs** (key feature!)
  - Generate input fields based on sampler signature
  - Support different types: float, int, list[float], list[list[float]]
  - Show parameter descriptions/tooltips
  - Validate before accepting

### 4. Parameter Input Widgets
- Float input
- Int input
- Vector input (list[float]) - multiple float fields or text input
- Matrix input (list[list[float]]) - text area or grid
- Validation feedback (red border, error message)

### 5. Export Control
- "Export Changes" checkbox (like CSV viewer)
- Only update pipeline_state if checked
- Return None if unchecked or cancelled

## Integration Points

### Entry Function
```python
# In transforms_gui_module/transforms_editor.py
def launch_transform_editor(pipeline_yaml: str) -> str | None:
    """
    Launch the transforms editor GUI.
    
    Args:
        pipeline_yaml: Current pipeline state as YAML string
    
    Returns:
        Modified YAML string if changes exported, None otherwise
    """
    pass
```

### Blender Operator
```python
# In ui/operators/edit_transforms_operator.py
class TRAITBLENDER_OT_edit_transforms(Operator):
    """Edit the transform pipeline using DearPyGUI interface"""
    bl_idname = "traitblender.edit_transforms"
    bl_label = "Edit Transforms"
    
    def execute(self, context):
        from ...core.transforms import launch_transform_editor
        config = context.scene.traitblender_config
        new_state = launch_transform_editor(config.transforms.pipeline_state)
        if new_state is not None:
            config.transforms.pipeline_state = new_state
        return {'FINISHED'}
```

### Panel Button
```python
# In ui/panels/main_panel.py - add to transforms panel
row = box.row(align=True)
row.operator("traitblender.edit_transforms", text="Edit Transforms", icon='PREFERENCES')
```

## Important Considerations

### 1. Sampler Signatures
Need to extract parameter info from sampler signatures. Already have utilities:
- `core/transforms/transform_registry_decorator.py` - validates type hints
- `core/helpers/property_type_mapping.py` - maps types to Blender properties
- `core/helpers/pretty_type_hint.py` - formats type names for display

Can use `inspect.signature()` to get parameter info from TRANSFORMS registry.

### 2. Property Path Validation
Need to validate that property paths exist in config before adding transform. Utilities:
- `core/helpers/config_validator.py` - `validate_config_path()`
- `core/helpers/config_validator.py` - `get_config_path_info()`

### 3. Known Bug: Undo History
The `Transform._cache_stack` is NOT serialized in the current YAML format. This is the source of the undo bug. The GUI should:
- Only handle the transform definitions (property_path, sampler_name, params)
- NOT attempt to serialize/deserialize undo history
- Leave undo bug fixing to separate work on the core system

### 4. Type Handling
Different parameter types need different UI widgets:
- `float` → Single float input
- `int` → Single int input  
- `list[float]` → Multiple float inputs or comma-separated text
- `list[list[float]]` → Matrix grid or text area with validation

### 5. Default Values
Samplers have defaults (e.g., `n: int = None`). The GUI should:
- Show default values in the UI
- Allow clearing to default (empty = use default)
- Include only non-default values in serialized params

## Related Files

- Core transform system: `core/transforms/`
- Transform config: `core/config/config_templates/transforms.py`
- Transform operators: `ui/operators/transforms_operators.py`
- Transform panel: `ui/panels/main_panel.py` (lines 166-199)
- CSV viewer reference: `core/datasets/csv_viewer_module/` (similar architecture)
- Config validator: `core/helpers/config_validator.py`
- Type mapping: `core/helpers/property_type_mapping.py`

## Development Checklist

- [ ] Data manager for YAML parsing/serialization
- [ ] Main window layout
- [ ] Transform list display
- [ ] Add transform dialog
- [ ] Dynamic parameter input generation
- [ ] Parameter validation
- [ ] Edit existing transform
- [ ] Remove transform
- [ ] Reorder transforms
- [ ] Export checkbox and logic
- [ ] Test all 10 samplers with various parameters
- [ ] Test with empty pipeline
- [ ] Test with complex nested parameters
- [ ] Integration with Blender operator
- [ ] Integration with panel button

## Notes

- This app will be similar in structure to the CSV viewer (`core/datasets/csv_viewer_module/`)
- Will use DearPyGUI for the UI framework (already included in TraitBlender dependencies)
- Focus on intuitive parameter entry for all 10 statistical samplers
- Support for both scalar and vector properties
- **Most important feature:** Dynamic parameter input based on sampler signature

## Current Files

- `transforms_editor.py` - Main application coordinator
- `transforms_manager.py` - Manages transform pipeline data and operations
- `ui_manager.py` - Handles GUI creation and Blender-like theming
- `test_app.py` - Standalone test script
- `README.md` - This file

## Testing the App

To test the standalone app without Blender:

```bash
cd misc_testing/transforms_gui
python test_app.py
```

This will launch the app with sample transform data. You can:
- View the list of transforms (displayed as cards)
- Delete individual transforms using the "Delete" button on each card
- Add dummy transforms using the "Add Transform" button (placeholder)
- Clear all transforms using the "Clear All" button
- Check "Export Changes" to return the modified YAML when closing

## Current Implementation Status

✅ **Completed:**
- Basic DearPyGUI app structure
- Blender-like dark theme
- YAML string parsing/serialization
- Transform list display as cards
- Delete transform functionality
- Clear all functionality
- Export checkbox logic
- Standalone testing capability

❌ **TODO:**
- Add transform dialog with property/sampler selection
- Dynamic parameter input generation based on sampler signature
- Edit existing transform functionality
- Reorder transforms (drag or up/down buttons)
- Parameter validation
- Property path validation
- Integration with Blender operator

## Status

🚧 **Under Development** - Basic structure complete, parameter input system needed

