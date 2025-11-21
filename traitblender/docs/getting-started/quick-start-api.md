# Quick Start Guide (API)

Learn how to use TraitBlender programmatically through Python scripts in Blender's Python console or script editor. This approach is ideal for batch processing, automation, and integration into larger workflows.

!!! note "GUI Alternative"
    This guide covers the Python API. If you prefer a graphical interface, see the [Quick Start (GUI)](./quick-start.md) guide.

## Prerequisites

Before starting, ensure you have:

- ✅ Blender 4.3.0+ installed
- ✅ TraitBlender add-on installed and enabled ([Installation Guide](./installation.md))
- ✅ Basic Python knowledge (helpful but not required)

## Basic API Usage

### 1. Setup Museum Scene

```python
import bpy

# Load the museum scene
bpy.ops.traitblender.setup_scene()
```

This loads the pre-configured museum scene with table, lighting, and camera.

### 2. Work with Datasets

```python
# Get the dataset property
dataset = bpy.context.scene.traitblender_dataset

# Set dataset filepath (auto-imports)
dataset.filepath = "/path/to/your/data.csv"

# Access dataset rows
row = dataset.loc("species_name")  # Get row by species name
print(row)  # Shows all trait values for that species

# Get dataset info
print(f"Dataset shape: {dataset.shape}")
print(f"Columns: {dataset.colnames}")
print(f"Rows: {dataset.rownames}")
```

### 3. Generate Morphospace Samples

```python
# Set morphospace (must match folder name in assets/morphospace_modules/)
setup = bpy.context.scene.traitblender_setup
setup.available_morphospaces = "CO_Raup"

# Select a sample from dataset
dataset = bpy.context.scene.traitblender_dataset
dataset.sample = "species_name"  # Use actual species name from your dataset

# Generate the 3D specimen
bpy.ops.traitblender.generate_morphospace_sample()
```

The specimen will be generated and placed at the center of the table.

### 4. Configure Scene Properties

```python
# Access configuration
config = bpy.context.scene.traitblender_config

# Modify camera settings
config.camera.location = (0.0, 0.0, 1.0)
config.camera.focal_length = 50.0
config.camera.resolution_x = 1920
config.camera.resolution_y = 1080

# Modify world settings
config.world.color = (0.0, 0.0, 0.0, 1.0)  # Black background
config.world.strength = 1.0

# Modify lamp settings
config.lamp.location = (0.0, 0.0, 1.0)
config.lamp.power = 10.0
config.lamp.color = (1.0, 1.0, 1.0)
```

### 5. Build Transform Pipeline

```python
# Get transforms config
transforms = bpy.context.scene.traitblender_config.transforms

# Add transforms to pipeline
transforms.add_transform("world.color", "uniform", {"low": 0.0, "high": 1.0})
transforms.add_transform("camera.location", "normal", {"mu": 0, "sigma": 0.5, "n": 3})
transforms.add_transform("world.strength", "beta", {"a": 2, "b": 5})

# Run the pipeline
transforms.run()

# Undo if needed
transforms.undo()
```

### 6. Position Objects Using Table Coordinates

```python
# Get generated specimen object
specimen = bpy.data.objects["species_name"]

# Position relative to table center
specimen.tb_coords = (0.0, 0.0, 0.0)  # Center of table
specimen.tb_rotation = (0.0, 0.0, 0.0)  # Aligned with table

# Move to different position
specimen.tb_coords = (0.5, 0.0, 0.0)  # 0.5 units along table's X axis
```

### 7. Export/Import Configuration

```python
import yaml

# Export current configuration to dict
config_dict = bpy.context.scene.traitblender_config.to_dict()

# Save to YAML file
with open("my_config.yaml", 'w') as f:
    yaml.dump(config_dict, f)

# Load configuration from YAML
with open("my_config.yaml", 'r') as f:
    config_data = yaml.safe_load(f)
    bpy.context.scene.traitblender_config.from_dict(config_data)
```

## Complete Example Script

Here's a complete script that processes a dataset:

```python
import bpy
import yaml

# Setup museum scene
bpy.ops.traitblender.setup_scene()

# Configure scene
config = bpy.context.scene.traitblender_config
config.camera.resolution_x = 1920
config.camera.resolution_y = 1920
config.world.color = (0.0, 0.0, 0.0, 1.0)

# Load dataset
dataset = bpy.context.scene.traitblender_dataset
dataset.filepath = "/path/to/your/dataset.csv"

# Set morphospace
setup = bpy.context.scene.traitblender_setup
setup.available_morphospaces = "CO_Raup"

# Process each species in dataset
for species_name in dataset.rownames:
    print(f"Processing {species_name}...")
    
    # Select and generate specimen
    dataset.sample = species_name
    bpy.ops.traitblender.generate_morphospace_sample()
    
    # Position on table
    specimen = bpy.data.objects[species_name]
    specimen.tb_coords = (0.0, 0.0, 0.0)
    
    # Optional: Apply transforms for variation
    transforms = config.transforms
    if len(transforms) > 0:
        transforms.run()
    
    # Render (configure output path first)
    config.output.output_directory = f"/path/to/output/{species_name}.png"
    bpy.ops.traitblender.imaging_pipeline()
    
    # Clean up for next iteration
    bpy.data.objects.remove(specimen, do_unlink=True)
    if len(transforms) > 0:
        transforms.undo()

print("Batch processing complete!")
```

## Working with Transform Pipelines

### Building Complex Pipelines

```python
transforms = bpy.context.scene.traitblender_config.transforms

# Clear any existing transforms
transforms.clear()

# Add multiple transforms
transforms.add_transform("world.color", "dirichlet", {"alphas": [1.0, 1.0, 1.0, 1.0]})
transforms.add_transform("camera.location", "multivariate_normal", {
    "mu": [0, 0, 0],
    "cov": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
})
transforms.add_transform("lamp.power", "gamma", {"alpha": 2.0, "beta": 1.0})

# Serialize pipeline to YAML
pipeline_yaml = transforms.pipeline_state
print(pipeline_yaml)

# Pipeline is automatically saved in config
```

### Accessing Pipeline Data

```python
import yaml

# Get pipeline as YAML string
yaml_string = bpy.context.scene.traitblender_config.transforms.pipeline_state

# Parse to Python objects
pipeline_data = yaml.safe_load(yaml_string)
print(f"Pipeline has {len(pipeline_data)} transforms")

# Access individual transforms
for i, transform in enumerate(pipeline_data):
    print(f"Transform {i+1}: {transform['property_path']} ~ {transform['sampler_name']}")
```

## Running Scripts

### Method 1: Blender Script Editor
1. Open Blender
2. Switch to **Scripting** workspace
3. Paste your script in the text editor
4. Click **Run Script** (or press `Alt+P`)

### Method 2: Blender Python Console
1. Open Blender
2. Open the **Python Console** (usually in bottom panel)
3. Paste and execute code line by line, or:
```python
exec(open("/path/to/your_script.py").read())
```

### Method 3: Command Line (Background)
```bash
# Run Blender in background with script
blender --background --python your_script.py

# With a specific blend file
blender --background my_scene.blend --python your_script.py
```

## Advanced Features

### Custom Morphospace Integration

```python
# Morphospaces are loaded dynamically from assets/morphospace_modules/
# Each morphospace must have:
# - A 'sample' function that takes parameters and returns a sample object
# - The sample object must have a 'to_blender()' method

# The system automatically maps dataset columns to morphospace parameters
# Column names are converted to lowercase with spaces replaced by underscores
```

### Dataset Manipulation

```python
dataset = bpy.context.scene.traitblender_dataset

# Access specific values
row = dataset.loc("species_name")
trait_value = row["trait_column_name"]

# Use pandas-like indexing
first_five = dataset.head(5)
last_five = dataset.tail(5)

# Iterate over dataset
for species_name in dataset.rownames:
    row_data = dataset.loc(species_name)
    print(f"{species_name}: {row_data}")
```

### Configuration Management

```python
# View all configuration sections
config = bpy.context.scene.traitblender_config
sections = config.get_config_sections()
print(f"Available sections: {list(sections.keys())}")

# Access nested properties
world_color = config.world.color
camera_location = config.camera.location

# Export full configuration
config_yaml = str(config)  # Returns YAML string
print(config_yaml)
```

## Next Steps

🎉 **Congratulations!** You can now use TraitBlender programmatically.

### Explore More:
- **[Configuration Files](../configuration/config-files.md)**: Understanding YAML config structure
- **[API Reference](../api/)**: Complete API documentation (coming soon)
- **[Tutorials](../tutorials/)**: Advanced techniques and workflows

### Tips for API Usage:
- Always run `setup_scene()` before using other features
- Use table coordinates (`tb_coords`) for consistent positioning
- Serialize configurations to YAML for reproducibility
- Test transforms on single specimens before batch processing
- Use try/except blocks for robust error handling

## Troubleshooting

Having issues with the API? Check our [troubleshooting guide](../troubleshooting/common-issues.md) for solutions to common problems.

---

**Estimated time**: 15-20 minutes to set up your first script  
**Skill level**: Intermediate  
**Output**: Automated specimen image generation pipeline

## Previous Step

Want to try the graphical interface first? Check out the **[Quick Start (GUI)](./quick-start.md)** guide. 