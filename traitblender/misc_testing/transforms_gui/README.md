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
- `property_helper.py` - Helper for getting available sections/properties (standalone + integrated)
- `sampler_helper.py` - Helper for extracting sampler signatures and validating parameters
- `property_dimension_helper.py` - Helper for determining property dimensions and auto-setting 'n' parameter
- `test_app.py` - Standalone test script
- `README.md` - This file

## Property & Sampler Selection System

The GUI uses dropdown menus for property path and sampler selection, matching the current TraitBlender GUI:

### How It Works

1. **Section Dropdown** - Select a configuration section (world, camera, lamp, etc.)
2. **Property Dropdown** - Select a property within that section (auto-updates when section changes)
3. **Sampler Dropdown** - Select a statistical sampler function

### Implementation

`property_helper.py` provides functions that work both standalone and when integrated:

- `get_available_sections()` - Returns list of sections
  - Standalone: Returns hardcoded common sections
  - Integrated: Uses `bpy.context.scene.traitblender_config.get_config_sections()`
  
- `get_properties_for_section(section_name)` - Returns properties for a section
  - Standalone: Returns hardcoded common properties per section
  - Integrated: Uses section object's `__annotations__` to get actual properties

- `get_available_samplers()` - Returns list of available samplers
  - Standalone: Returns hardcoded common samplers
  - Integrated: Uses `core.transforms.registry.TRANSFORMS` registry
  
- `build_property_path(section, property)` - Constructs full path (e.g., "world.color")
- `parse_property_path(path)` - Parses path back to (section, property)

### Usage in Cards

Each transform card displays:
- **Property:** Two cascading dropdowns for section and property selection
- **Sampler:** Dropdown for sampler function selection

When a selection changes:
- The transform's `property_path` or `sampler_name` is automatically updated
- When sampler changes, parameters are cleared and new input fields are generated based on the new sampler's signature

## Dynamic Parameter System

The GUI automatically generates parameter input fields based on the sampler's function signature.

### How It Works

1. **Signature Extraction** (`sampler_helper.py`)
   - Uses Python's `inspect.signature()` to extract parameter info from sampler functions
   - Extracts: parameter name, type hint, default value, required/optional status
   - Works standalone (mock signatures) and integrated (actual TRANSFORMS registry)

2. **Automatic `n` Parameter** (`property_dimension_helper.py`)
   - The `n` parameter is **automatically determined** from the property type and dimension
   - **NOT shown in the UI** - users don't need to set it manually
   - **Scalar properties** (FloatProperty): `n = None` (single value)
   - **Vector properties** (FloatVectorProperty): `n = len(property)` (e.g., 3 for camera.location, 4 for world.color)
   - **Auto-updates** when property path changes
   - Uses `get_property_type()` to determine if property is scalar or vector
   - Evaluates property to get actual dimension using `len()`

3. **Type-Appropriate Widgets**
   - `float` / `int` → Single input box (width: 100px)
   - `list[float]` / `list[int]` → **Row of input boxes** (one per element, sized by property dimension)
   - `list[list[float]]` → **Grid of input boxes** (matrix layout, sized by property dimension)

4. **Real-Time Validation**
   - As you type, values are validated against the expected type
   - **Valid**: White text, value saved to transform
   - **Invalid**: Red text, error logged to console
   - Uses `validate_parameter_value()` to parse and convert strings to proper types

5. **Parameter Display**
   - Shows parameter name, type hint, and required indicator (*)
   - Required parameters: Bright white label
   - Optional parameters: Dim gray label
   - Default values automatically applied by sampler
   - **`n` parameter hidden** - auto-managed by the system

### Examples

**Uniform sampler** (for scalar property like `lamp.power`):
```
  low (float) *     [___100___]
  high (float) *    [___100___]
  (n auto-set to None for scalar)
```

**Uniform sampler** (for vector property like `camera.location`):
```
  low (float) *     [___100___]
  high (float) *    [___100___]
  (n auto-set to 3 for 3D vector)
```

**Dirichlet sampler** (for color property like `world.color`):
```
  alphas (list[float]) *   [0.3] [0.3] [0.3] [1.0]
  (n auto-set to 4 for RGBA)
```

**Multivariate Normal sampler** (for 3D vector):
```
  mu (list[float]) *        [0] [0] [0]
  
  cov (list[list[float]]) * [1] [0] [0]
                            [0] [1] [0]
                            [0] [0] [1]
  (n auto-set to 3 based on property)
```

### Validation Rules

- **float**: Must parse as float (e.g., "1.5", "2", "-0.3")
- **int**: Must parse as integer (e.g., "3", "-5", "0")
- **list[float]**: Each box must be a valid float
- **list[int]**: Each box must be a valid integer
- **list[list[float]]**: Each box in the grid must be a valid float

Empty fields for optional parameters (with defaults) are allowed.

### Grid Sizing

- **Vector inputs**: Number of boxes matches property dimension
  - `camera.location` (3D) → 3 boxes
  - `world.color` (RGBA) → 4 boxes
  
- **Matrix inputs**: Grid size matches property dimension
  - 3D property → 3×3 grid
  - 4D property (color) → 4×4 grid
  - Defaults to identity matrix if no value provided

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
- Drag-and-drop reordering of transforms
- Property path selection using section + property dropdowns
- Property helper module (works standalone and integrated)
- Cascading dropdowns (section selection updates property dropdown)
- Property path editing per transform
- Sampler dropdown per transform
- Sampler selection with automatic parameter clearing
- **Dynamic parameter input generation based on sampler signature**
- **Parameter type checking and validation with visual feedback**
- **Grid-based input system for vectors and matrices**
- **Automatic grid sizing based on property dimension**
- **Real-time parameter validation (red text for errors)**
- **Automatic `n` parameter determination based on property dimension**
- **Property dimension detection (scalar vs vector, vector length)**

❌ **TODO:**
- Add transform dialog for creating new transforms
- Integration with Blender operator
- Improve parameter input UX (hints, tooltips, default value buttons)

## Status

🚧 **Under Development** - Basic structure complete, parameter input system needed

