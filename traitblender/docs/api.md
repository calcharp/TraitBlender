# API Documentation

!!! note "TODO: Module Import Instructions"
    **Standard Blender Access**: Configs, properties, operators, and panels can be accessed through `bpy` like other Blender add-ons:
    - `bpy.context.scene.traitblender_config`
    - `bpy.ops.traitblender.setup_scene()`
    - etc.
    
    **TraitBlender-Specific Functions**: Helper functions and internal modules must be imported using Blender's non-standard import path (instructions to be added here).
    
    **For Developers**: When working within the TraitBlender codebase itself, standard Python imports work normally.

---

??? note "Museum Setup"
    
    ## Operators
    
    **`bpy.ops.traitblender.setup_scene()`**
    
    Load the TraitBlender museum scene for morphological imaging
    
    **Description**: Load the pre-configured museum scene with lighting and camera setup
    
    **Returns**: 
    - `{'FINISHED'}` on success
    - `{'CANCELLED'}` on error
    
    **Note**: Shows confirmation dialog if scene has unsaved changes
    
    ---
    
    **`bpy.ops.traitblender.clear_scene()`**
    
    Clear all objects and data from the current scene
    
    **Description**: Remove all objects, materials, and data from the current scene
    
    **Returns**: 
    - `{'FINISHED'}` on success
    - `{'CANCELLED'}` on error
    
    **Note**: Shows confirmation dialog before clearing
    
    ---
    
    **`bpy.ops.traitblender.configure_scene(filepath="")`**
    
    Configure TraitBlender scene from YAML file
    
    **Description**: Load and apply configuration from YAML file
    
    **Parameters**:
    - `filepath` (str, optional): Path to the YAML configuration file. If not provided, uses `context.scene.traitblender_setup.config_file`. If neither is set, opens file browser.
    
    **Returns**: 
    - `{'FINISHED'}` on success
    - `{'CANCELLED'}` on error
    
    **Note**: Requires museum scene to be loaded first (via `setup_scene()`)
    
    ---
    
    **`bpy.ops.traitblender.show_configuration()`**
    
    Show current TraitBlender configuration in YAML format
    
    **Description**: Display current configuration in YAML format
    
    **Returns**: `{'FINISHED'}`
    
    **Note**: Opens a dialog window displaying the current configuration
    
    ---
    
    **`bpy.ops.traitblender.export_config(filepath="")`**
    
    Export current TraitBlender configuration to a YAML file
    
    **Description**: Export the current configuration to a YAML file
    
    **Parameters**:
    - `filepath` (str): Path to export YAML file (opens file browser if not provided)
    
    **Returns**: 
    - `{'FINISHED'}` on success
    - `{'CANCELLED'}` on error
    
    ---
    
    ## Properties
    
    **`bpy.context.scene.traitblender_setup`**
    
    Property group for TraitBlender setup configuration.
    
    **Attributes**:
    - `config_file` (str): Path to YAML configuration file
    - `available_morphospaces` (EnumProperty): List of available morphospace modules (read-only, auto-populated)
    
    **Example**:
    ```python
    setup = bpy.context.scene.traitblender_setup
    setup.config_file = "/path/to/config.yaml"
    ```
    

??? note "Configuration"
    
    ## Accessing Configuration
    
    **`bpy.context.scene.traitblender_config`**
    
    Main configuration object containing all TraitBlender settings.
    
    **Example**:
    ```python
    config = bpy.context.scene.traitblender_config
    
    # Access config sections
    world = config.world
    camera = config.camera
    lamp = config.lamp
    ```
    
    ---
    
    ## Getting and Setting Properties
    
    Configuration properties automatically sync with Blender objects. Access them directly:
    
    ```python
    config = bpy.context.scene.traitblender_config
    
    # Get property values
    world_color = config.world.color
    camera_location = config.camera.location
    lamp_power = config.lamp.power
    
    # Set property values
    config.world.color = (0.1, 0.1, 0.1, 1.0)
    config.camera.location = (0.0, 0.0, 1.0)
    config.lamp.power = 5.0
    ```
    
    **Note**: Properties use dynamic getters/setters that check for required Blender objects. If objects don't exist, getters return default values and setters do nothing (with warnings).
    
    ---
    
    ## Serialization
    
    ### `to_dict()`
    
    Convert the configuration to a nested dictionary.
    
    **Returns**: `dict` - Dictionary representation of the configuration
    
    **Example**:
    ```python
    config = bpy.context.scene.traitblender_config
    config_dict = config.to_dict()
    # Returns: {'world': {'color': [0.0, 0.0, 0.0, 1.0], 'strength': 1.0}, ...}
    ```
    
    ---
    
    ### `from_dict(data_dict)`
    
    Load configuration values from a dictionary.
    
    **Parameters**:
    - `data_dict` (dict): Dictionary containing configuration values. Can contain nested dictionaries for nested config sections.
    
    **Example**:
    ```python
    config = bpy.context.scene.traitblender_config
    config_data = {
        'world': {'color': [0.1, 0.1, 0.1, 1.0], 'strength': 2.0},
        'camera': {'location': [0.0, 0.0, 1.5], 'focal_length': 50.0}
    }
    config.from_dict(config_data)
    ```
    
    ---
    
    ### `__str__()` / YAML Export
    
    Convert the configuration to YAML format.
    
    **Returns**: `str` - YAML string representation
    
    **Example**:
    ```python
    config = bpy.context.scene.traitblender_config
    yaml_string = str(config)
    print(yaml_string)
    # Output:
    # ---
    # world:
    #   color: [0.0, 0.0, 0.0, 1.0]
    #   strength: 1.0
    # camera:
    #   location: [0.0, 0.0, 0.0]
    #   ...
    ```
    
    ---
    
    ## Config Sections
    
    ### `get_config_sections()`
    
    Get all nested config sections.
    
    **Returns**: `dict` - Dictionary mapping section names to their config objects
    
    **Example**:
    ```python
    config = bpy.context.scene.traitblender_config
    sections = config.get_config_sections()
    # Returns: {'world': <WorldConfig>, 'camera': <CameraConfig>, ...}
    
    for section_name, section_obj in sections.items():
        print(f"Section: {section_name}")
    ```
    
    ---
    
    ## Common Operations
    
    ### Export Configuration to File
    
    ```python
    import yaml
    
    config = bpy.context.scene.traitblender_config
    config_dict = config.to_dict()
    
    with open('my_config.yaml', 'w') as f:
        yaml.dump(config_dict, f)
    ```
    
    ---
    
    ### Import Configuration from File
    
    ```python
    import yaml
    
    with open('my_config.yaml', 'r') as f:
        config_data = yaml.safe_load(f)
    
    config = bpy.context.scene.traitblender_config
    config.from_dict(config_data)
    ```
    
    ---
    
    ### Access Nested Properties
    
    ```python
    config = bpy.context.scene.traitblender_config
    
    # Direct access
    world_color = config.world.color
    
    # Using getattr for dynamic access
    section = getattr(config, 'world')
    color = getattr(section, 'color')
    
    # Using getattr for safe access
    if hasattr(config, 'world') and hasattr(config.world, 'color'):
        color = config.world.color
    ```
    
    ---
    
    ## Available Config Sections
    
    The following sections are available in `traitblender_config`:
    
    - `world` - World background color and strength
    - `camera` - Camera location, rotation, focal length, resolution, etc.
    - `lamp` - Lamp location, rotation, color, power, etc.
    - `mat` - Specimen mat properties
    - `render` - Render engine settings
    - `output` - Output format and directory
    - `metadata` - Image metadata/stamp settings
    - `orientations` - Specimen orientation settings
    - `transforms` - Transform pipeline configuration
    
    Each section can be accessed as `config.section_name` and contains properties specific to that section.
    

??? note "Morphospaces"
    
    ## Operators
    
    **`bpy.ops.traitblender.generate_morphospace_sample()`**
    
    Generate a 3D specimen from the selected morphospace and dataset row.
    
    **Description**: Creates a 3D mesh object in Blender using the selected morphospace model and parameters from the currently selected dataset sample.
    
    **Returns**: 
    - `{'FINISHED'}` on success
    - `{'CANCELLED'}` on error
    
    **Requirements**:
    - A morphospace must be selected (via `traitblender_setup.available_morphospaces`)
    - A dataset sample must be selected (via `traitblender_dataset.sample`)
    - Dataset must be loaded with data
    
    **Note**: The generated object is automatically positioned at the center of the table (tb_coords = (0, 0, 0)) and named after the selected sample.
    
    **Example**:
    ```python
    # Select morphospace and dataset sample first
    setup = bpy.context.scene.traitblender_setup
    dataset = bpy.context.scene.traitblender_dataset
    
    setup.available_morphospaces = "CO_Raup"
    dataset.sample = "SpeciesName"
    
    # Generate the specimen
    bpy.ops.traitblender.generate_morphospace_sample()
    ```
    
    ---
    
    ## Properties
    
    **`bpy.context.scene.traitblender_setup.available_morphospaces`**
    
    Enum property for selecting the active morphospace module.
    
    **Type**: `EnumProperty` (read-only, auto-populated)
    
    **Description**: Lists all available morphospace modules found in `assets/morphospace_modules/`. The value is the morphospace folder name.
    
    **Example**:
    ```python
    setup = bpy.context.scene.traitblender_setup
    
    # Get current selection
    current_morphospace = setup.available_morphospaces
    print(f"Selected morphospace: {current_morphospace}")
    
    # Set morphospace (if "CO_Raup" is available)
    setup.available_morphospaces = "CO_Raup"
    ```
    
    **Note**: The enum items are dynamically generated by scanning the morphospace modules directory. Only morphospaces with a valid `__init__.py` file are included.
    
    ---
    
    ## Workflow
    
    ### Complete Morphospace Generation Workflow
    
    ```python
    # 1. Load museum scene
    bpy.ops.traitblender.setup_scene()
    
    # 2. Import dataset
    dataset = bpy.context.scene.traitblender_dataset
    dataset.filepath = "/path/to/dataset.csv"
    
    # 3. Select morphospace
    setup = bpy.context.scene.traitblender_setup
    setup.available_morphospaces = "CO_Raup"
    
    # 4. Select a sample from the dataset
    dataset.sample = "MySpecies"
    
    # 5. Generate the specimen
    bpy.ops.traitblender.generate_morphospace_sample()
    
    # The generated object is now in the scene at the table center
    obj = bpy.data.objects.get("MySpecies")
    ```
    

??? note "Datasets"
    
    ## Accessing Dataset
    
    **`bpy.context.scene.traitblender_dataset`**
    
    Main dataset object for managing morphological data.
    
    **Example**:
    ```python
    dataset = bpy.context.scene.traitblender_dataset
    ```
    
    ---
    
    ## Operators
    
    **`bpy.ops.traitblender.import_dataset()`**
    
    Import dataset from file and convert to CSV string.
    
    **Description**: Imports a dataset from CSV, TSV, or Excel file. Requires `dataset.filepath` to be set first.
    
    **Returns**: 
    - `{'FINISHED'}` on success
    - `{'CANCELLED'}` on error
    
    **Supported Formats**: CSV, TSV (.tsv), Excel (.xlsx, .xls)
    
    **Example**:
    ```python
    dataset = bpy.context.scene.traitblender_dataset
    dataset.filepath = "/path/to/dataset.csv"
    bpy.ops.traitblender.import_dataset()
    ```
    
    **Note**: Setting `dataset.filepath` automatically imports the dataset, so calling this operator is usually not necessary.
    
    ---
    
    **`bpy.ops.traitblender.edit_dataset()`**
    
    Open CSV editor to edit the dataset.
    
    **Description**: Opens a DearPyGui-based CSV viewer/editor for viewing and editing dataset values.
    
    **Returns**: 
    - `{'FINISHED'}` on success
    - `{'CANCELLED'}` on error
    
    **Note**: Requires a dataset to be loaded first. Changes are saved back to the dataset when the editor is closed.
    
    **Example**:
    ```python
    dataset = bpy.context.scene.traitblender_dataset
    if dataset.csv:  # Check if dataset is loaded
        bpy.ops.traitblender.edit_dataset()
    ```
    
    ---
    
    ## Properties
    
    **`filepath`**
    
    Path to the dataset file. Automatically imports the dataset when set.
    
    **Type**: `StringProperty` (FILE_PATH)
    
    **Supported Formats**: CSV, TSV, Excel (.xlsx, .xls)
    
    **Example**:
    ```python
    dataset = bpy.context.scene.traitblender_dataset
    dataset.filepath = "/path/to/dataset.csv"
    # Dataset is automatically imported
    ```
    
    ---
    
    **`sample`**
    
    Enum property for selecting a sample (species/specimen) from the dataset.
    
    **Type**: `EnumProperty` (read-only, auto-populated from dataset)
    
    **Description**: Lists all samples in the dataset. The value is the species/specimen name (from the first column).
    
    **Example**:
    ```python
    dataset = bpy.context.scene.traitblender_dataset
    
    # Get current selection
    current_sample = dataset.sample
    print(f"Selected sample: {current_sample}")
    
    # Set sample (use actual name from your dataset)
    dataset.sample = "SpeciesName"
    ```
    
    ---
    
    ## Data Access Methods
    
    **`loc(species_name)` or `loc(species_name, column_name)`**
    
    Access rows and columns by label (pandas-like loc accessor).
    
    **Parameters**:
    - `species_name` (str): Species/specimen name (row index)
    - `column_name` (str, optional): Column name. If omitted, returns the entire row.
    
    **Returns**: 
    - `pandas.Series` if accessing a row
    - Value if accessing a specific cell
    
    **Example**:
    ```python
    dataset = bpy.context.scene.traitblender_dataset
    
    # Get entire row for a species
    row = dataset.loc("SpeciesName")
    print(row)
    
    # Get specific column value
    value = dataset.loc("SpeciesName", "column_name")
    print(value)
    ```
    
    ---
    
    **`iloc(row_index)` or `iloc(row_index, column_index)`**
    
    Access rows and columns by integer position (pandas-like iloc accessor).
    
    **Parameters**:
    - `row_index` (int): Row index (0-based)
    - `column_index` (int, optional): Column index. If omitted, returns the entire row.
    
    **Returns**: 
    - `pandas.Series` if accessing a row
    - Value if accessing a specific cell
    
    **Example**:
    ```python
    dataset = bpy.context.scene.traitblender_dataset
    
    # Get first row
    first_row = dataset.iloc(0)
    
    # Get value at row 0, column 1
    value = dataset.iloc(0, 1)
    ```
    
    ---
    
    **`head(n=5)`**
    
    Return the first n rows of the dataset.
    
    **Parameters**:
    - `n` (int, optional): Number of rows to return (default: 5)
    
    **Returns**: `pandas.DataFrame` - First n rows
    
    **Example**:
    ```python
    dataset = bpy.context.scene.traitblender_dataset
    first_five = dataset.head(5)
    print(first_five)
    ```
    
    ---
    
    **`tail(n=5)`**
    
    Return the last n rows of the dataset.
    
    **Parameters**:
    - `n` (int, optional): Number of rows to return (default: 5)
    
    **Returns**: `pandas.DataFrame` - Last n rows
    
    **Example**:
    ```python
    dataset = bpy.context.scene.traitblender_dataset
    last_five = dataset.tail(5)
    print(last_five)
    ```
    
    ---
    
    ## Dataset Properties
    
    **`colnames`**
    
    List of column names in the dataset.
    
    **Type**: `property` (returns `list`)
    
    **Example**:
    ```python
    dataset = bpy.context.scene.traitblender_dataset
    columns = dataset.colnames
    print(f"Columns: {columns}")
    # Output: ['species', 'b', 'd', 'z', 'a', ...]
    ```
    
    ---
    
    **`rownames`**
    
    List of row names (species/specimen names) in the dataset.
    
    **Type**: `property` (returns `list`)
    
    **Example**:
    ```python
    dataset = bpy.context.scene.traitblender_dataset
    species_list = dataset.rownames
    print(f"Species: {species_list[:5]}")  # First 5 species
    ```
    
    ---
    
    **`shape`**
    
    Shape of the dataset as (rows, columns) tuple.
    
    **Type**: `property` (returns `tuple`)
    
    **Example**:
    ```python
    dataset = bpy.context.scene.traitblender_dataset
    rows, cols = dataset.shape
    print(f"Dataset has {rows} rows and {cols} columns")
    ```
    
    ---
    
    ## Special Methods
    
    **`len(dataset)`**
    
    Get the number of rows in the dataset.
    
    **Example**:
    ```python
    dataset = bpy.context.scene.traitblender_dataset
    num_rows = len(dataset)
    print(f"Dataset has {num_rows} rows")
    ```
    
    ---
    
    **`str(dataset)`**
    
    Get a string representation of the dataset.
    
    **Example**:
    ```python
    dataset = bpy.context.scene.traitblender_dataset
    print(str(dataset))
    ```
    
    ---
    
    **`iter(dataset)`**
    
    Iterate over column names.
    
    **Example**:
    ```python
    dataset = bpy.context.scene.traitblender_dataset
    for column_name in dataset:
        print(column_name)
    ```
    
    ---
    
    ## Common Operations
    
    ### Import and Inspect Dataset
    
    ```python
    dataset = bpy.context.scene.traitblender_dataset
    
    # Import dataset
    dataset.filepath = "/path/to/dataset.csv"
    
    # Inspect dataset
    print(f"Shape: {dataset.shape}")
    print(f"Columns: {dataset.colnames}")
    print(f"First 5 species: {dataset.rownames[:5]}")
    
    # View first few rows
    print(dataset.head(5))
    ```
    
    ---
    
    ### Get Row Data for a Species
    
    ```python
    dataset = bpy.context.scene.traitblender_dataset
    
    # Get all data for a species
    row = dataset.loc("SpeciesName")
    print(row)
    
    # Get specific parameter value
    param_value = dataset.loc("SpeciesName", "parameter_name")
    print(f"Parameter value: {param_value}")
    ```
    
    ---
    
    ### Iterate Over All Species
    
    ```python
    dataset = bpy.context.scene.traitblender_dataset
    
    for species_name in dataset.rownames:
        row_data = dataset.loc(species_name)
        print(f"Processing {species_name}: {row_data}")
        # Use row_data for morphospace generation, etc.
    ```
    
    ---
    
    ### Dataset Format Requirements
    
    Datasets should have:
    
    - **First column**: Species/specimen names (automatically detected from: species, label, tips, name, id, etc.)
    - **Remaining columns**: Morphological traits/parameters that map to morphospace parameters
    
    TraitBlender automatically:
    - Detects the species column (case-insensitive)
    - Moves the species column to the first position
    - Uses the species column as the row index
    
    **Supported File Formats**: CSV, TSV, Excel (.xlsx, .xls)
    

??? note "Orientations"
    
    Each morphospace defines orientation functions in its `ORIENTATIONS` dictionary. These functions are called with the sample object and modify it in place (e.g., rotating so the aperture faces the camera).
    
    ## Operators
    
    **`bpy.ops.traitblender.apply_orientation()`**
    
    Apply the selected orientation function to the current sample.
    
    **Returns**: 
    - `{'FINISHED'}` on success
    - `{'CANCELLED'}` on error
    
    **Requirements**:
    - A dataset sample must be selected (via `traitblender_dataset.sample`)
    - The sample object must exist in the scene
    - An orientation other than "NONE" must be selected
    
    **Example**:
    ```python
    config = bpy.context.scene.traitblender_config
    config.orientations.orientation = "Aperture Up"  # Morphospace-specific
    bpy.ops.traitblender.apply_orientation()
    ```
    
    ---
    
    ## Configuration Properties
    
    **`bpy.context.scene.traitblender_config.orientations`**
    
    **Properties**:
    - `orientation` (EnumProperty): Orientation function to apply. Options come from the selected morphospace's `ORIENTATIONS` dict (e.g., "Default", "Center on Table", "Aperture Up" for CO_Raup). Use "NONE" to skip.
    
    ---
    
    ## Object Properties
    
    **`bpy.data.objects["ObjectName"].tb_coords`**
    
    Table coordinates property for positioning objects relative to the table surface.
    
    **Type**: `FloatVectorProperty` (3D vector)
    
    **Description**: Position relative to Table's top face center in table's local coordinate system. The origin (0,0,0) is at the center of the table top.
    
    **Example**:
    ```python
    obj = bpy.data.objects["MySpecimen"]
    
    # Get current table coordinates
    coords = obj.tb_coords
    print(f"Table coordinates: {coords}")
    
    # Set position at table center
    obj.tb_coords = (0.0, 0.0, 0.0)
    
    # Move 1 meter along X axis
    obj.tb_coords = (1.0, 0.0, 0.0)
    ```
    
    ---
    
    **`bpy.data.objects["ObjectName"].tb_rotation`**
    
    Table rotation property for rotating objects relative to the table.
    
    **Type**: `FloatVectorProperty` (3D vector, Euler angles)
    
    **Description**: Rotation relative to the table's coordinate system (in radians).
    
    **Example**:
    ```python
    obj = bpy.data.objects["MySpecimen"]
    
    # Get current rotation
    rotation = obj.tb_rotation
    print(f"Table rotation: {rotation}")
    
    # Set rotation
    obj.tb_rotation = (0.0, 0.0, 0.0)
    ```
    
    ---
    
    ## Common Operations
    
    ### Position Specimen at Table Center
    
    ```python
    obj = bpy.data.objects["MySpecimen"]
    obj.tb_coords = (0.0, 0.0, 0.0)
    obj.tb_rotation = (0.0, 0.0, 0.0)
    ```
    
    ---
    
    ### Apply Orientation
    
    ```python
    config = bpy.context.scene.traitblender_config
    config.orientations.orientation = "Aperture Up"  # Morphospace-specific
    bpy.ops.traitblender.apply_orientation()
    ```
    

??? note "Transforms"
    
    ## Operators
    
    **`bpy.ops.traitblender.run_pipeline()`**
    
    Execute all transforms in the pipeline.
    
    **Description**: Runs all transforms in the transform pipeline in sequence, applying statistical variations to scene properties.
    
    **Returns**: 
    - `{'FINISHED'}` on success
    - `{'CANCELLED'}` on error
    
    **Example**:
    ```python
    # Build pipeline first (see Configuration section)
    config = bpy.context.scene.traitblender_config
    config.transforms.add_transform("camera.focal_length", "uniform", {"low": 30, "high": 100})
    
    # Run the pipeline
    bpy.ops.traitblender.run_pipeline()
    ```
    
    ---
    
    **`bpy.ops.traitblender.undo_pipeline()`**
    
    Undo all transforms in the pipeline.
    
    **Description**: Reverts all transforms in reverse order, restoring original property values.
    
    **Returns**: 
    - `{'FINISHED'}` on success
    - `{'CANCELLED'}` on error
    
    **Example**:
    ```python
    # Undo all applied transforms
    bpy.ops.traitblender.undo_pipeline()
    ```
    
    ---
    
    ## Configuration Methods
    
    **`bpy.context.scene.traitblender_config.transforms`**
    
    Transform pipeline configuration object.
    
    ### `add_transform(property_path, sampler_name, params=None)`
    
    Add a transform to the pipeline.
    
    **Parameters**:
    - `property_path` (str): Relative property path (e.g., 'world.color', 'camera.focal_length')
    - `sampler_name` (str): Name of the sampler function (e.g., 'uniform', 'normal', 'beta')
    - `params` (dict, optional): Parameters for the sampler function
    
    **Returns**: `TransformPipelineConfig` - Self for method chaining
    
    **Example**:
    ```python
    config = bpy.context.scene.traitblender_config
    transforms = config.transforms
    
    # Add a uniform transform
    transforms.add_transform("camera.focal_length", "uniform", {"low": 30, "high": 100})
    
    # Add a normal distribution transform
    transforms.add_transform("camera.location", "normal", {"mu": 0, "sigma": 1, "n": 3})
    
    # Add a color transform (dirichlet for vectors)
    transforms.add_transform("world.color", "dirichlet", {"alphas": [0.3, 0.3, 0.3, 1]})
    ```
    
    ---
    
    ### `run()`
    
    Execute all transforms in the pipeline.
    
    **Returns**: `list` - List of results from each transform execution
    
    **Example**:
    ```python
    config = bpy.context.scene.traitblender_config
    results = config.transforms.run()
    print(f"Applied {len(results)} transforms")
    ```
    
    ---
    
    ### `undo()`
    
    Undo all transforms in reverse order.
    
    **Returns**: `list` - List of results from each undo operation
    
    **Example**:
    ```python
    config = bpy.context.scene.traitblender_config
    results = config.transforms.undo()
    print(f"Undid {len(results)} transforms")
    ```
    
    ---
    
    ### `clear()`
    
    Clear all transforms from the pipeline.
    
    **Returns**: `TransformPipelineConfig` - Self for method chaining
    
    **Example**:
    ```python
    config = bpy.context.scene.traitblender_config
    config.transforms.clear()
    ```
    
    ---
    
    ### `remove_transform(index)`
    
    Remove a transform from the pipeline by index.
    
    **Parameters**:
    - `index` (int): Zero-based index of the transform to remove
    
    **Returns**: `bool` - True if successful, False otherwise
    
    **Example**:
    ```python
    config = bpy.context.scene.traitblender_config
    # Remove the first transform (index 0)
    config.transforms.remove_transform(0)
    ```
    
    ---
    
    ## Pipeline Properties
    
    **`len(transforms)`**
    
    Get the number of transforms in the pipeline.
    
    **Example**:
    ```python
    config = bpy.context.scene.traitblender_config
    num_transforms = len(config.transforms)
    print(f"Pipeline has {num_transforms} transforms")
    ```
    
    ---
    
    **`transforms[index]`**
    
    Access a transform by index.
    
    **Example**:
    ```python
    config = bpy.context.scene.traitblender_config
    first_transform = config.transforms[0]
    print(first_transform)
    ```
    
    ---
    
    ## Common Operations
    
    ### Build and Run a Transform Pipeline
    
    ```python
    config = bpy.context.scene.traitblender_config
    transforms = config.transforms
    
    # Clear any existing transforms
    transforms.clear()
    
    # Add transforms
    transforms.add_transform("camera.focal_length", "uniform", {"low": 50, "high": 100})
    transforms.add_transform("world.color", "dirichlet", {"alphas": [0.2, 0.2, 0.2, 1]})
    transforms.add_transform("lamp.power", "normal", {"mu": 5.0, "sigma": 1.0})
    
    # Run the pipeline
    transforms.run()
    
    # Later, undo if needed
    transforms.undo()
    ```
    
    ---
    
    ### Available Samplers
    
    The following sampler functions are available:
    
    - `uniform` - Uniform distribution between low and high
    - `normal` - Normal (Gaussian) distribution
    - `beta` - Beta distribution
    - `gamma` - Gamma distribution
    - `dirichlet` - Dirichlet distribution (for color vectors)
    - `multivariate_normal` - Multivariate normal distribution
    - `poisson` - Poisson distribution
    - `exponential` - Exponential distribution
    - `cauchy` - Cauchy distribution
    - `discrete_uniform` - Discrete uniform distribution
    
    Each sampler has specific parameter requirements. See the transform system documentation for details.
    

??? note "Imaging"
    
    ## Operators
    
    **`bpy.ops.traitblender.imaging_pipeline()`**
    
    Run the imaging pipeline to render specimens.
    
    **Description**: Iterates through the dataset and renders images for each specimen. Applies any configured transforms before rendering.
    
    **Returns**: 
    - `{'FINISHED'}` on success
    - `{'CANCELLED'}` on error
    
    **Note**: This operator is currently under development. Functionality may be limited.
    
    **Example**:
    ```python
    # Configure output settings first
    config = bpy.context.scene.traitblender_config
    config.output.output_directory = "/path/to/output"
    config.output.file_format = "PNG"
    
    # Run the imaging pipeline
    bpy.ops.traitblender.imaging_pipeline()
    ```
    
    ---
    
    ## Configuration
    
    Imaging uses settings from the `output` and `render` config sections:
    
    **`bpy.context.scene.traitblender_config.output`**
    
    - `output_directory` (str): Directory to save rendered images
    - `file_format` (EnumProperty): Image format (PNG, JPEG, etc.)
    
    **`bpy.context.scene.traitblender_config.render`**
    
    - Render engine settings (Cycles, Eevee, etc.)
    - Resolution and quality settings
    
    **Example**:
    ```python
    config = bpy.context.scene.traitblender_config
    
    # Set output directory
    config.output.output_directory = "/path/to/output/images"
    
    # Set file format
    config.output.file_format = "PNG"
    
    # Configure render settings
    config.render.resolution_x = 1920
    config.render.resolution_y = 1080
    ```
    
    ---
    
    ## Workflow
    
    ### Basic Rendering Workflow
    
    ```python
    # 1. Setup scene and load dataset
    bpy.ops.traitblender.setup_scene()
    dataset = bpy.context.scene.traitblender_dataset
    dataset.filepath = "/path/to/dataset.csv"
    
    # 2. Configure output
    config = bpy.context.scene.traitblender_config
    config.output.output_directory = "/path/to/output"
    config.output.file_format = "PNG"
    
    # 3. (Optional) Configure transforms for data augmentation
    config.transforms.add_transform("camera.focal_length", "uniform", {"low": 50, "high": 100})
    
    # 4. Run imaging pipeline
    bpy.ops.traitblender.imaging_pipeline()
    ```
    
    ---
    
    ### Manual Rendering
    
    You can also render manually using Blender's standard rendering:
    
    ```python
    # Configure output path
    config = bpy.context.scene.traitblender_config
    config.output.output_directory = "/path/to/output"
    
    # Set render filepath
    bpy.context.scene.render.filepath = f"{config.output.output_directory}/image.png"
    
    # Render
    bpy.ops.render.render(write_still=True)
    ```
    
