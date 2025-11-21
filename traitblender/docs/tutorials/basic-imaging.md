# Basic Specimen Imaging Tutorial

This tutorial will guide you through creating your first museum-style specimen images using TraitBlender. By the end, you'll be able to import datasets, generate 3D specimens, and render high-quality images.

## Prerequisites

- TraitBlender installed and enabled in Blender 4.3+
- Basic familiarity with Blender interface
- A CSV/Excel file with morphological data (or use the example format below)

## Tutorial Overview

We'll create a complete workflow to:
1. Load the museum scene
2. Import a morphological dataset
3. Generate 3D specimens from the dataset
4. Configure camera and lighting
5. Render museum-style images

## Step 1: Setup Museum Scene

### 1.1 Load the Museum Scene

```python
import bpy

# Load the pre-configured museum scene
bpy.ops.traitblender.setup_scene()
```

This loads:
- Museum table
- Camera with proper positioning
- Lighting setup
- Specimen mat
- Default configuration

### 1.2 Verify Scene Setup

```python
# Check that key objects exist
required_objects = ["Table", "Camera", "Mat"]
for obj_name in required_objects:
    if obj_name in bpy.data.objects:
        print(f"✓ {obj_name} loaded")
    else:
        print(f"✗ {obj_name} missing")
```

## Step 2: Prepare Your Dataset

### 2.1 Dataset Format

Your dataset should be a CSV or Excel file with:
- **First column**: Species/specimen names (automatically detected)
- **Remaining columns**: Morphological traits that map to morphospace parameters

Example CSV format for CO_Raup morphospace:

```csv
species,b,d,z,a,phi,psi,c_depth,c_n,n_depth,n,t,length
species1,0.1,4,0,1,0,0,0.1,70,0,0,20,0.015
species2,0.15,5,0,1.2,0.1,0.2,0.15,80,0.05,5,25,0.02
species3,0.08,3.5,0,0.9,0,0,0.08,60,0,0,18,0.012
```

### 2.2 Import Dataset

```python
# Get dataset property
dataset = bpy.context.scene.traitblender_dataset

# Set filepath (auto-imports)
dataset.filepath = "/path/to/your/dataset.csv"

# Verify import
print(f"Dataset shape: {dataset.shape}")
print(f"Columns: {dataset.colnames}")
print(f"Species: {dataset.rownames[:5]}")  # First 5 species
```

## Step 3: Select Morphospace

```python
# Set morphospace type
setup = bpy.context.scene.traitblender_setup
setup.available_morphospaces = "CO_Raup"

print(f"Selected morphospace: {setup.available_morphospaces}")
```

## Step 4: Generate a Specimen

### 4.1 Select and Generate

```python
# Select a species from dataset
dataset = bpy.context.scene.traitblender_dataset
dataset.sample = "species1"  # Use actual name from your dataset

# Generate the 3D specimen
bpy.ops.traitblender.generate_morphospace_sample()

# Verify generation
if dataset.sample in bpy.data.objects:
    specimen = bpy.data.objects[dataset.sample]
    print(f"✓ Generated {dataset.sample}")
    print(f"  Location: {specimen.location}")
    print(f"  Table coords: {specimen.tb_coords}")
```

### 4.2 Position Specimen

```python
# Get the generated specimen
specimen = bpy.data.objects[dataset.sample]

# Position at table center (default)
specimen.tb_coords = (0.0, 0.0, 0.0)

# Or position elsewhere
specimen.tb_coords = (0.2, 0.0, 0.0)  # Move along table X axis
```

## Step 5: Configure Camera and Scene

### 5.1 Adjust Camera Settings

```python
# Access configuration
config = bpy.context.scene.traitblender_config

# Camera position (relative to table)
config.camera.location = (0.0, 0.0, 1.0)  # 1 meter above table center

# Camera rotation
config.camera.rotation = (0.0, 0.0, 0.0)

# Focal length
config.camera.focal_length = 60.0  # 60mm lens

# Resolution
config.camera.resolution_x = 1920
config.camera.resolution_y = 1920
config.camera.resolution_percentage = 100
```

### 5.2 Configure Lighting

```python
# Lamp position
config.lamp.location = (0.0, 0.0, 1.0)

# Lamp power
config.lamp.power = 10.0

# Lamp color
config.lamp.color = (1.0, 1.0, 1.0)  # White light
```

### 5.3 Set Background

```python
# World background
config.world.color = (0.0, 0.0, 0.0, 1.0)  # Black background
config.world.strength = 1.0
```

## Step 6: Configure Rendering

### 6.1 Set Render Engine

```python
# Use EEVEE for faster rendering
config.render.engine = "BLENDER_EEVEE_NEXT"

# Or Cycles for higher quality
# config.render.engine = "CYCLES"
```

### 6.2 Set Output Path

```python
# Output directory
config.output.output_directory = "/path/to/output/directory"
config.output.image_format = "PNG"
```

## Step 7: Render Image

### 7.1 Single Image

```python
# Set output filename
import os
output_dir = "/path/to/output"
species_name = dataset.sample
output_path = os.path.join(output_dir, f"{species_name}.png")

# Update output directory
config.output.output_directory = output_path

# Render
bpy.ops.traitblender.imaging_pipeline()
```

### 7.2 Batch Render Multiple Specimens

```python
import os

# Setup
output_dir = "/path/to/output"
os.makedirs(output_dir, exist_ok=True)

# Process each species
for species_name in dataset.rownames:
    print(f"Processing {species_name}...")
    
    # Select and generate
    dataset.sample = species_name
    bpy.ops.traitblender.generate_morphospace_sample()
    
    # Position
    specimen = bpy.data.objects[species_name]
    specimen.tb_coords = (0.0, 0.0, 0.0)
    
    # Render
    output_path = os.path.join(output_dir, f"{species_name}.png")
    config.output.output_directory = output_path
    bpy.ops.traitblender.imaging_pipeline()
    
    # Clean up
    bpy.data.objects.remove(specimen, do_unlink=True)
    
    print(f"✓ Rendered {species_name}")

print("Batch rendering complete!")
```

## Step 8: Add Data Augmentation (Optional)

### 8.1 Build Transform Pipeline

```python
# Get transforms config
transforms = config.transforms

# Clear any existing transforms
transforms.clear()

# Add transforms for variation
transforms.add_transform("world.color", "uniform", {"low": 0.0, "high": 0.1})
transforms.add_transform("camera.location", "normal", {"mu": 0, "sigma": 0.1, "n": 3})
transforms.add_transform("lamp.power", "gamma", {"alpha": 2.0, "beta": 1.0})

print(f"Pipeline has {len(transforms)} transforms")
```

### 8.2 Apply Transforms Before Rendering

```python
# Generate specimen
bpy.ops.traitblender.generate_morphospace_sample()

# Apply transforms for variation
transforms.run()

# Render with variation
bpy.ops.traitblender.imaging_pipeline()

# Undo if needed
transforms.undo()
```

## Complete Example Script

Here's a complete script that implements this tutorial:

```python
import bpy
import os

# Step 1: Setup
bpy.ops.traitblender.setup_scene()

# Step 2: Configure scene
config = bpy.context.scene.traitblender_config
config.camera.resolution_x = 1920
config.camera.resolution_y = 1920
config.camera.focal_length = 60.0
config.world.color = (0.0, 0.0, 0.0, 1.0)

# Step 3: Load dataset
dataset = bpy.context.scene.traitblender_dataset
dataset.filepath = "/path/to/your/dataset.csv"

# Step 4: Set morphospace
setup = bpy.context.scene.traitblender_setup
setup.available_morphospaces = "CO_Raup"

# Step 5: Setup output
output_dir = "/path/to/output"
os.makedirs(output_dir, exist_ok=True)

# Step 6: Process each species
for species_name in dataset.rownames:
    print(f"Processing {species_name}...")
    
    # Generate specimen
    dataset.sample = species_name
    bpy.ops.traitblender.generate_morphospace_sample()
    
    # Position on table
    specimen = bpy.data.objects[species_name]
    specimen.tb_coords = (0.0, 0.0, 0.0)
    
    # Render
    output_path = os.path.join(output_dir, f"{species_name}.png")
    config.output.output_directory = output_path
    bpy.ops.traitblender.imaging_pipeline()
    
    # Clean up
    bpy.data.objects.remove(specimen, do_unlink=True)

print("Tutorial complete!")
```

## Tips for Better Results

### Camera Positioning

- **Distance**: Adjust `camera.location.z` to frame your specimen properly
- **Angle**: Use `camera.rotation` to change viewing angle
- **Focal Length**: Longer focal lengths (85mm+) reduce perspective distortion

### Lighting

- **Power**: Start with 10.0 and adjust based on specimen size
- **Position**: Place lights to highlight specimen features
- **Color**: Slight color temperature variation can add realism

### Specimen Positioning

- **Table coordinates**: Always use `tb_coords` for consistent placement
- **Rotation**: Use `tb_rotation` for table-relative orientation
- **Multiple specimens**: Space them using different `tb_coords` values

## Common Issues and Solutions

### Specimen Not Visible

- Check that morphospace generation completed successfully
- Verify specimen is positioned above table: `specimen.tb_coords.z >= 0`
- Ensure camera is looking at the right location

### Dataset Import Fails

- Verify file format (CSV, TSV, or Excel)
- Check that species column is detected (should be first column)
- Ensure column names match morphospace parameter names

### Rendering Issues

- Check output directory exists and is writable
- Verify render engine is set correctly
- Ensure camera is active: `bpy.context.scene.camera = camera_object`

## Next Steps

Once you're comfortable with basic imaging:

1. **Explore Transforms**: Learn to add statistical variation ([Transform Documentation](../configuration/config-files.md#transforms))
2. **Custom Configurations**: Create and save YAML configs for different setups
3. **Batch Processing**: Process entire datasets programmatically
4. **Advanced Techniques**: Experiment with different morphospace parameters

For more information, see:
- [Quick Start API Guide](../getting-started/quick-start-api.md)
- [Configuration Files](../configuration/config-files.md)
- [API Reference](../api/)
