# For Developers

This page provides detailed documentation for developers working on TraitBlender. For a high-level overview of the architecture, see the [Architecture](./architecture.md) page.

---

??? note "Configuration System"
    
    See [Architecture: Configuration System](./architecture.md#1-configuration-system) for an overview.
    
    ## Overview
    
    The Configuration System manages all scene settings (camera, lighting, world, etc.) with automatic synchronization to Blender objects. It uses a dynamic registration system that allows new config sections to be added without modifying core code.
    
    ## How It Works
    
    ### Registration Flow
    
    1. **Config Template Creation**: Each config section is a class decorated with `@register("section_name")`
    2. **AST Discovery**: The `config_templates/__init__.py` uses AST parsing to find all `@register` decorated classes
    3. **Dynamic Class Creation**: `configure_traitblender()` creates a dynamic `TraitBlenderConfig` class with all discovered sections
    4. **Property Registration**: The dynamic class is registered as `bpy.context.scene.traitblender_config`
    
    ### Dynamic Getters/Setters
    
    Config properties use `get_property()` and `set_property()` functions that:
    - Accept a Blender property path string (e.g., `'bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value'`)
    - Check for object dependencies before accessing
    - Handle missing objects gracefully (return defaults or do nothing)
    - Use `eval()`/`exec()` to access/set Blender properties dynamically
    
    ### YAML Serialization
    
    Configs can be serialized to/from YAML:
    - `to_dict()`: Converts config to nested dictionary
    - `from_dict()`: Loads config from dictionary
    - `__str__()`: Returns YAML-formatted string representation
    
    ## Key Components
    
    - **`core/config/register_config.py`**: Base `TraitBlenderConfig` class and `@register` decorator
    - **`core/config/config_templates/`**: Individual config section classes
    - **`core/helpers/property_getset.py`**: Dynamic property getters/setters
    - **`core/helpers/config_validator.py`**: Property path validation
    
    ## Adding a New Config Section
    
    1. Create a new file in `core/config/config_templates/` (e.g., `my_section.py`)
    2. Import `register` and `TraitBlenderConfig`:
       ```python
       import bpy
       from ..register_config import register, TraitBlenderConfig
       from ...helpers import get_property, set_property
       ```
    3. Create a class decorated with `@register("section_name")`:
       ```python
       @register("my_section")
       class MySectionConfig(TraitBlenderConfig):
           print_index = 5  # Optional: controls YAML output order
           
           my_property: bpy.props.FloatProperty(
               name="My Property",
               description="Description",
               default=1.0,
               get=get_property('bpy.data.objects["MyObject"].some_property',
                               object_dependencies={"objects": ["MyObject"]}),
               set=set_property('bpy.data.objects["MyObject"].some_property',
                               object_dependencies={"objects": ["MyObject"]})
           )
       ```
    4. The config section will be automatically discovered and registered
    
    ## Common Pitfalls
    
    - **Object Dependencies**: Always specify `object_dependencies` in getters/setters. Missing objects will cause warnings or errors.
    - **Property Paths**: Use exact Blender property paths. Test paths in Blender's Python console first.
    - **Type Mismatches**: Ensure property types match between config and Blender (FloatProperty → float, etc.)
    - **Circular Dependencies**: Avoid config sections that depend on each other
    
    ## Related Systems
    
    - [Transform Pipeline](#transform-pipeline): Uses config property paths
    - [Asset Management](#asset-management): Config files stored in assets/configs/

---

??? note "Scene Assets"
    
    See [Architecture: Positioning System](./architecture.md#5-positioning-system) for an overview.
    
    ## Overview
    
    The Scene Assets system (also called the Positioning System) provides a table-relative coordinate system for consistent object placement. It includes custom properties on all Blender objects and origin calculation functions.
    
    ## How It Works
    
    ### Table Coordinates (`tb_coords`)
    
    A custom `FloatVectorProperty` on all objects that represents position relative to the Table's top face center:
    - **Getter**: Calculates object's position in table's local coordinate system
    - **Setter**: Transforms table-relative coordinates to world space and sets `object.location`
    - **Coordinate System**: Uses table's rotation matrix (unit axes) for consistent orientation
    
    ### Table Rotation (`tb_rotation`)
    
    A custom `FloatVectorProperty` for rotation around object's bottom-center pivot:
    - **Getter**: Returns object's current `rotation_euler`
    - **Setter**: Rotates object around its bottom-center pivot point
    - **Pivot Calculation**: Finds lowest Z vertex, uses that as pivot point
    
    ### Origin Calculation Functions
    
    Functions in `core/positioning/origins.py` calculate different types of origins:
    - `OBJECT`: Object's actual origin
    - `GEOM_BOUNDS`: Center of bounding box
    - `MEAN`: Mean position of all vertices
    - `MEDIAN`: Median position of all vertices
    
    ## Key Components
    
    - **`ui/properties/table_coords.py`**: `tb_coords` property registration
    - **`ui/properties/table_rotations.py`**: `tb_rotation` property registration
    - **`core/positioning/get_table_coords.py`**: Coordinate transformation utilities
    - **`core/positioning/origins.py`**: Origin calculation functions
    
    ## Adding a New Origin Type
    
    1. Create a function in `core/positioning/origins.py`:
       ```python
       def _get_custom_origin(obj):
           """Calculate custom origin in table coordinates."""
           # Your calculation logic here
           return (x, y, z)  # Table coordinates
       ```
    2. Add to `PLACEMENT_LOCAL_ORIGINS_TB` dictionary:
       ```python
       PLACEMENT_LOCAL_ORIGINS_TB = {
           # ... existing origins ...
           'CUSTOM': _get_custom_origin,
       }
       ```
    3. The new origin will automatically appear in orientation config enums
    
    ## Common Pitfalls
    
    - **Table Object Missing**: `tb_coords` getter/setter check for Table object, but operations may fail if Table doesn't exist
    - **Coordinate System**: Table coordinates use table's rotation, not world axes. Objects rotate with table.
    - **Bottom-Center Calculation**: `tb_rotation` uses lowest Z vertex, which may not be accurate for all object types
    
    ## Related Systems
    
    - [Orientations Config](#configuration-system): Uses origin functions for positioning
    - [Morphospace Development](#morphospace-development): Generated objects use `tb_coords` for placement

---

??? note "Transform Pipeline"
    
    See [Architecture: Transform Pipeline](./architecture.md#2-transform-pipeline) for an overview.
    
    ## Overview
    
    The Transform Pipeline applies statistical randomization to scene properties for data augmentation. It uses a registry-based system for sampler functions and maintains undo history.
    
    ## How It Works
    
    ### Transform Registry
    
    Sampler functions are registered using the `@register_transform('name')` decorator:
    - Functions must have type hints on all parameters
    - Registry stores factory functions that return configured samplers
    - Samplers can be called with parameters to generate random values
    
    ### Transform Class
    
    Each `Transform` object:
    - Stores a property path (e.g., `"world.color"`)
    - Stores a sampler name and parameters
    - Caches original values in a stack for undo operations
    - Can be called to apply the transform or undone to revert
    
    ### Pipeline Class
    
    The `TransformPipeline` manages multiple transforms:
    - Stores transforms in a list
    - Executes transforms in sequence when `run()` is called
    - Undoes transforms in reverse order when `undo()` is called
    - Serializes to YAML for persistence
    
    ## Key Components
    
    - **`core/transforms/registry.py`**: Transform registry and sampler functions
    - **`core/transforms/transform_registry_decorator.py`**: `@register_transform` decorator
    - **`core/transforms/transforms.py`**: `Transform` class
    - **`core/transforms/pipeline.py`**: `TransformPipeline` class
    - **`core/config/config_templates/transforms.py`**: Config integration
    
    ## Adding a New Sampler Function
    
    1. Create a function with type hints in `core/transforms/registry.py`:
       ```python
       @register_transform('my_sampler')
       def my_sampler(param1: float, param2: int, n: int = None) -> float | list[float]:
           # Your sampling logic here
           if n is None:
               return single_value
           return [value1, value2, ...]
       ```
    2. The sampler will automatically appear in the transform registry
    3. Use it in transforms:
       ```python
       transform = Transform("world.color", "my_sampler", {"param1": 1.0, "param2": 2})
       ```
    
    ## Common Pitfalls
    
    - **Type Hints Required**: All parameters must have type hints for the decorator to work
    - **Property Path Validation**: Transforms validate property paths exist in config before creation
    - **Undo Stack**: Each transform call adds to the undo stack. Multiple calls = multiple undo steps.
    - **Serialization**: Pipeline state is stored as YAML string in config. Large pipelines may cause performance issues.
    
    ## Related Systems
    
    - [Configuration System](#configuration-system): Transforms access config properties
    - [Config Validator](#configuration-system): Validates property paths

---

??? note "Morphospace Development"
    
    See [Architecture: Morphospace System](./architecture.md#4-morphospace-system) for an overview.
    
    ## Overview
    
    The Morphospace System dynamically loads and executes morphospace modules to generate 3D specimens. Morphospaces are discovered from the filesystem and loaded on-demand.
    
    ## How It Works
    
    ### Discovery
    
    `list_morphospaces()` scans `assets/morphospace_modules/` for directories containing `__init__.py`:
    - Each directory is a morphospace module
    - Module name = directory name
    - Modules are listed in the UI dropdown
    
    ### Module Loading
    
    When a morphospace is selected:
    1. Module path is constructed: `assets/morphospace_modules/{name}/`
    2. `__init__.py` is loaded using `importlib`
    3. `sample` function is extracted from the module
    4. Function signature is inspected to determine parameters
    
    ### Parameter Mapping
    
    Dataset columns are mapped to function parameters:
    - Column names are lowercased and spaces replaced with underscores
    - Parameters matching function signature are passed
    - `name` parameter is always the species name
    
    ### Object Generation
    
    The `sample()` function:
    - Receives species name and parameter values
    - Generates a 3D object (typically using a morphospace library)
    - Returns an object with a `to_blender()` method
    - Object is added to Blender scene with species name
    
    ## Key Components
    
    - **`core/morphospaces/list_morphospaces.py`**: Discovery function
    - **`ui/operators/generate_morphospace_sample_operator.py`**: Module loading and execution
    - **`assets/morphospace_modules/`**: Morphospace module storage
    
    ## Creating a New Morphospace Module
    
    1. Create a directory in `assets/morphospace_modules/` (e.g., `MyMorphospace/`)
    2. Create `__init__.py` with a `sample()` function:
       ```python
       def sample(name: str, param1: float, param2: float):
           # Generate 3D object using morphospace
           obj = MyMorphospaceObject(param1, param2)
           obj.name = name
           return obj
       ```
    3. The morphospace will automatically appear in the UI dropdown
    4. Ensure the object returned has a `to_blender()` method
    
    ## Expected Interface
    
    Morphospace modules must provide:
    - **`sample(name: str, **params) -> object`**: Function that generates a specimen
    - **Returned object**: Must have `to_blender()` method that adds object to Blender scene
    
    ## Common Pitfalls
    
    - **Module Import Errors**: Ensure all dependencies are available in Blender's Python environment
    - **Parameter Mismatches**: Dataset columns must match function parameter names (case-insensitive, spaces→underscores)
    - **Object Naming**: Generated objects should use the `name` parameter for consistent identification
    - **Blender Integration**: Objects must be properly added to scene using `to_blender()` method
    
    ## Related Systems
    
    - [Dataset Management](#dataset-management): Provides data to morphospaces
    - [Positioning System](#scene-assets): Generated objects use `tb_coords` for placement

---

??? note "Code Structure"
    
    See [Architecture](./architecture.md) for system overview and data flow.
    
    ## Directory Layout
    
    ```
    TraitBlender/
    ├── __init__.py                 # Main addon registration
    ├── core/                       # Core systems
    │   ├── config/                 # Configuration system
    │   │   ├── register_config.py  # Base classes and decorator
    │   │   └── config_templates/   # Individual config sections
    │   ├── datasets/               # Dataset management
    │   ├── helpers/                # Utility functions
    │   ├── morphospaces/           # Morphospace discovery
    │   ├── positioning/            # Table coordinates and origins
    │   └── transforms/             # Transform pipeline
    ├── ui/                         # User interface
    │   ├── operators/              # Blender operators
    │   ├── panels/                 # UI panels
    │   └── properties/             # Property groups
    ├── assets/                     # Static assets
    │   ├── configs/                # Default configs
    │   ├── morphospace_modules/   # Morphospace modules
    │   ├── objects/                # 3D objects and materials
    │   └── scenes/                  # Scene files
    └── docs/                       # Documentation
    ```
    
    ## Import Dependencies
    
    - **Core systems** are independent (config, transforms, datasets, etc.)
    - **UI** depends on **core** systems
    - **Helpers** are used by multiple systems
    - **No circular dependencies** between major systems
    
    ## Registration Order
    
    Registration occurs in this order (see `__init__.py`):
    1. Config discovery and registration
    2. Dataset property group registration
    3. UI components (operators, panels, properties)
    4. Asset initialization
    
    ## Module Boundaries
    
    - **Core**: Business logic, no Blender UI dependencies
    - **UI**: Blender-specific UI code, depends on core
    - **Assets**: Static files, loaded at runtime
    - **Docs**: Documentation, no code dependencies
    
    ## Extension Points
    
    See [Architecture: Extension Points](./architecture.md#extension-points) for high-level overview.
    
    ### Adding New Features
    
    - **Config Section**: Add file to `core/config/config_templates/`
    - **Transform Sampler**: Add function to `core/transforms/registry.py`
    - **Morphospace**: Add directory to `assets/morphospace_modules/`
    - **Operator**: Add file to `ui/operators/`, register in `ui/operators/__init__.py`
    - **Panel**: Add file to `ui/panels/`, register in `ui/panels/__init__.py`
    - **Origin Type**: Add function to `core/positioning/origins.py`
    
    ## Related Systems
    
    - [Architecture](./architecture.md): System overview and interactions
    - [Configuration System](#configuration-system): Config structure
    - [Transform Pipeline](#transform-pipeline): Transform structure

---

??? note "Contributing"
    
    ## Development Workflow
    
    1. **Setup**: Install TraitBlender in development mode
    2. **Modify**: Make changes to code
    3. **Test**: Test in Blender with sample data
    4. **Document**: Update relevant documentation
    5. **Commit**: Follow commit message conventions
    
    ## Common Patterns
    
    ### Property Dependency Pattern
    
    Always specify object dependencies in config properties:
    ```python
    get=get_property('bpy.data.objects["Camera"].location',
                    object_dependencies={"objects": ["Camera"]})
    ```
    
    ### Error Handling Pattern
    
    Use warnings for missing objects, errors for invalid operations:
    ```python
    if not _check_object_dependencies(object_dependencies):
        warnings.warn("Missing objects, using default")
        return default_value
    ```
    
    ### Serialization Pattern
    
    Both configs and transforms use `to_dict()`/`from_dict()`:
    ```python
    def to_dict(self):
        return {"key": value}
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    ```
    
    ## Troubleshooting
    
    ### Config Properties Not Updating
    
    - Check object dependencies exist
    - Verify property paths are correct (test in Blender console)
    - Check for type mismatches
    
    ### Transforms Not Working
    
    - Verify property path exists in config
    - Check sampler function parameters match
    - Ensure sampler is registered correctly
    
    ### Morphospaces Not Appearing
    
    - Check directory has `__init__.py`
    - Verify module name matches directory name
    - Check for import errors in module
    
    ### Table Coordinates Not Working
    
    - Ensure Table object exists in scene
    - Check object has mesh data (for bottom-center calculation)
    - Verify table coordinates are set after object creation
    
    ## Testing Strategies
    
    - **Unit Tests**: Test individual functions (getters/setters, transforms)
    - **Integration Tests**: Test system interactions (config → transform → render)
    - **Manual Testing**: Test in Blender with real data
    
    ## Related Systems
    
    - [Architecture](./architecture.md): Understanding system interactions
    - [Code Structure](#code-structure): File organization
    - [Configuration System](#configuration-system): Config patterns
    - [Transform Pipeline](#transform-pipeline): Transform patterns

