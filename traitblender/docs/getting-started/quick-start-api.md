# Quick Start Guide (API)

Learn how to use TraitBlender programmatically through Python scripts and Blender's API. This approach is ideal for batch processing, automation, and integration into larger workflows.

!!! note "GUI Alternative"
    This guide covers the Python API. If you prefer a graphical interface, see the [Quick Start (GUI)](./quick-start.md) guide.

## Prerequisites

Before starting, ensure you have:

- ✅ Blender 4.3.0+ installed
- ✅ TraitBlender add-on installed ([Installation Guide](./installation.md))
- ✅ Basic Python knowledge (helpful but not required)

## Basic API Usage

### 1. Enable TraitBlender in Script

```python
import bpy

# Enable TraitBlender add-on if not already enabled
bpy.ops.preferences.addon_enable(module="traitblender")

# Import TraitBlender modules
from traitblender.core import SceneAsset
from traitblender.operators import GenerateImageOperator
```

### 2. Load a Specimen

```python
# Clear existing scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Import a specimen model
specimen_path = "/path/to/your/specimen.obj"
bpy.ops.import_scene.obj(filepath=specimen_path)

# Get the imported object
specimen = bpy.context.selected_objects[0]
specimen.name = "specimen"
```

### 3. Apply Scene Configuration

```python
# Create a museum-style scene
scene_config = {
    "lighting": "museum_standard",
    "background": {"color": (1.0, 1.0, 1.0, 1.0)},  # White background
    "camera": {
        "view": "lateral",
        "distance": 5.0
    }
}

# Apply scene settings
scene_asset = SceneAsset(**scene_config)
scene_asset.apply()
```

### 4. Configure Rendering

```python
# Set render properties
scene = bpy.context.scene
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.filepath = "/path/to/output/specimen_image.png"

# Configure render engine for quality
scene.render.engine = 'CYCLES'
scene.cycles.samples = 128
```

### 5. Generate Image

```python
# Render the image
bpy.ops.render.render(write_still=True)

print("Image rendered successfully!")
```

## Complete Example Script

Here's a complete script that processes a specimen:

```python
import bpy
import os

def process_specimen(input_path, output_path):
    """
    Process a single specimen and generate museum-style image
    
    Args:
        input_path (str): Path to specimen model file
        output_path (str): Path for output image
    """
    
    # Clear scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Import specimen
    bpy.ops.import_scene.obj(filepath=input_path)
    specimen = bpy.context.selected_objects[0]
    
    # Center and scale specimen
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='BOUNDS')
    specimen.location = (0, 0, 0)
    
    # Setup camera
    bpy.ops.object.camera_add(location=(3, -3, 2))
    camera = bpy.context.object
    camera.rotation_euler = (1.1, 0, 0.785)
    
    # Setup lighting
    bpy.ops.object.light_add(type='SUN', location=(2, 2, 5))
    sun = bpy.context.object
    sun.data.energy = 3.0
    
    # Configure render settings
    scene = bpy.context.scene
    scene.camera = camera
    scene.render.resolution_x = 2048
    scene.render.resolution_y = 2048
    scene.render.filepath = output_path
    scene.render.image_settings.file_format = 'PNG'
    
    # Render
    bpy.ops.render.render(write_still=True)
    
    return True

# Example usage
if __name__ == "__main__":
    input_file = "/path/to/specimen.obj"
    output_file = "/path/to/output/specimen.png"
    
    process_specimen(input_file, output_file)
    print(f"Processed {input_file} -> {output_file}")
```

## Batch Processing Multiple Specimens

```python
import os
import glob

def batch_process_specimens(input_dir, output_dir):
    """
    Process all specimen files in a directory
    """
    # Supported file formats
    extensions = ['*.obj', '*.ply', '*.blend']
    
    for ext in extensions:
        pattern = os.path.join(input_dir, ext)
        files = glob.glob(pattern)
        
        for file_path in files:
            filename = os.path.basename(file_path)
            name, _ = os.path.splitext(filename)
            output_path = os.path.join(output_dir, f"{name}.png")
            
            print(f"Processing: {filename}")
            process_specimen(file_path, output_path)
            print(f"Completed: {output_path}")

# Batch process example
batch_process_specimens("/specimens/", "/output_images/")
```

## Running Scripts

### Method 1: Blender GUI Script Editor
1. Open Blender
2. Switch to **Scripting** workspace
3. Paste your script in the text editor
4. Click **Run Script**

### Method 2: Command Line
```bash
# Run Blender in background with script
blender --background --python your_script.py

# With additional arguments
blender --background --python process_specimens.py -- --input /data --output /results
```

### Method 3: Within Blender Python Console
```python
# In Blender's Python console
exec(open("/path/to/your_script.py").read())
```

## Advanced Features

### Custom Transforms
```python
from traitblender.transforms import MorphologicalTransform

# Apply custom morphological transform
transform = MorphologicalTransform(
    scale_factor=1.2,
    orientation="dorsal",
    standardize=True
)
transform.apply(specimen)
```

### Configuration Files
```python
import yaml

# Load configuration from YAML
with open("specimen_config.yaml", 'r') as f:
    config = yaml.safe_load(f)

# Apply configuration
for key, value in config['scene'].items():
    setattr(scene_asset, key, value)
```

## Next Steps

🎉 **Congratulations!** You can now use TraitBlender programmatically.

### Explore More:
- **[API Reference](../api/core.md)**: Complete API documentation
- **[CLI Usage](../cli/usage.md)**: Command-line batch processing
- **[Configuration Files](../configuration/config-files.md)**: YAML-based configurations

### Tips for API Usage:
- Always clear the scene before importing new specimens
- Use try/except blocks for robust error handling
- Save scene configurations for consistency across specimens
- Consider memory management for large batch operations

## Troubleshooting

Having issues with the API? Check our [troubleshooting guide](../troubleshooting/common-issues.md) for solutions to common problems.

---

**Estimated time**: 10-15 minutes to set up your first script  
**Skill level**: Intermediate  
**Output**: Automated specimen image generation pipeline

## Previous Step

Want to try the graphical interface first? Check out the **[Quick Start (GUI)](./quick-start.md)** guide. 