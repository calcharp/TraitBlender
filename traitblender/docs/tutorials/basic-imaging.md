# Basic Specimen Imaging Tutorial

This tutorial will guide you through creating your first museum-style specimen images using TraitBlender. By the end, you'll be able to import specimens, set up cameras, and generate high-quality images suitable for scientific documentation.

## Prerequisites

- TraitBlender installed and enabled in Blender 4.2+
- Basic familiarity with Blender interface
- A 3D specimen model (`.obj`, `.ply`, or `.blend` format)

## Tutorial Overview

We'll create a simple imaging setup to photograph a specimen from multiple angles, similar to museum documentation standards.

## Step 1: Prepare Your Scene

### 1.1 Open Blender and Clear Default Scene

```python
import bpy

# Clear default scene (optional)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
```

### 1.2 Import Your Specimen

1. **File > Import > [Your Format]** (e.g., Wavefront OBJ)
2. Navigate to your specimen file and import it
3. Your specimen should appear in the 3D viewport

Alternatively, using Python:
```python
# Import an OBJ file
bpy.ops.import_scene.obj(filepath="/path/to/your/specimen.obj")
```

## Step 2: Set Up TraitBlender Scene Assets

### 2.1 Create a Scene Asset for Your Specimen

```python
from traitblender.core.positioning import GenericAsset

# Create an asset for your imported specimen
# Replace "SpecimenName" with your actual object name
specimen = GenericAsset("SpecimenName")

# Set the origin to bottom center for proper placement
specimen.origin_set(type="BOTTOM_CENTER")
```

### 2.2 Create a Surface for Specimen Placement

```python
from traitblender.core.positioning import SurfaceAsset

# Add a plane as a base/table
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
bpy.context.active_object.name = "SpecimenTable"

# Create a surface asset
table = SurfaceAsset("SpecimenTable")
```

### 2.3 Place Specimen on Surface

```python
# Place the specimen at the center of the table
table.place(specimen, (0, 0))
```

## Step 3: Configure Lighting

### 3.1 Add Museum-Style Lighting

```python
# Add a key light (main light source)
bpy.ops.object.light_add(type='AREA', location=(2, -2, 3))
key_light = bpy.context.active_object
key_light.name = "KeyLight"
key_light.data.energy = 50
key_light.data.size = 2

# Add a fill light (softer secondary light)
bpy.ops.object.light_add(type='AREA', location=(-1, 1, 2))
fill_light = bpy.context.active_object
fill_light.name = "FillLight"
fill_light.data.energy = 20
fill_light.data.size = 3

# Add a rim light (for edge definition)
bpy.ops.object.light_add(type='SPOT', location=(0, 3, 1))
rim_light = bpy.context.active_object
rim_light.name = "RimLight"
rim_light.data.energy = 30
```

### 3.2 Set Up Environment

```python
# Set up world background
world = bpy.context.scene.world
world.use_nodes = True
bg_node = world.node_tree.nodes["Background"]
bg_node.inputs[0].default_value = (0.9, 0.9, 0.9, 1)  # Light gray background
bg_node.inputs[1].default_value = 0.5  # Strength
```

## Step 4: Set Up Cameras for Standard Views

### 4.1 Create Camera Positions

```python
import math

def create_camera_view(name, location, rotation):
    """Create a camera with specific position and rotation"""
    bpy.ops.object.camera_add(location=location, rotation=rotation)
    camera = bpy.context.active_object
    camera.name = name
    return camera

# Standard museum views
cameras = {
    "aperture": create_camera_view(
        "Camera_Aperture", 
        (0, 0, -3),  # Below specimen, looking up
        (0, 0, 0)
    ),
    "apex": create_camera_view(
        "Camera_Apex", 
        (0, 0, 3),   # Above specimen, looking down
        (math.pi, 0, 0)
    ),
    "lateral": create_camera_view(
        "Camera_Lateral", 
        (3, 0, 0),   # Side view
        (math.pi/2, 0, math.pi/2)
    ),
}
```

### 4.2 Configure Camera Settings

```python
for camera_name, camera in cameras.items():
    camera.data.lens = 50  # 50mm lens for natural perspective
    camera.data.clip_end = 100  # Extend render distance
    
    # Point camera at specimen
    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.target = specimen.object
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'
```

## Step 5: Configure Rendering Settings

### 5.1 Set Render Engine and Quality

```python
# Set rendering engine to Cycles for high quality
bpy.context.scene.render.engine = 'CYCLES'

# Configure quality settings
bpy.context.scene.cycles.samples = 128  # Good balance of quality/speed
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1920  # Square format for specimens

# Enable GPU rendering if available
bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
bpy.context.scene.cycles.device = 'GPU'
```

### 5.2 Set Output Format

```python
# Configure output settings
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGBA'
bpy.context.scene.render.filepath = "/path/to/output/directory/"
```

## Step 6: Render Images

### 6.1 Render Each View

```python
import os

output_dir = "/path/to/your/output/directory"
specimen_name = "MySpecimen"

for view_name, camera in cameras.items():
    # Set active camera
    bpy.context.scene.camera = camera
    
    # Set output filename
    filename = f"{specimen_name}_{view_name}.png"
    bpy.context.scene.render.filepath = os.path.join(output_dir, filename)
    
    # Render the image
    bpy.ops.render.render(write_still=True)
    
    print(f"Rendered {filename}")
```

### 6.2 Using TraitBlender Configuration (Alternative)

Create a configuration file `basic_imaging.yaml`:

```yaml
blender_preferences:
  use_online_access: False

rendering:
  render_engine: Cycles
  compute_device_type: CUDA
  samples: 128
  resolution_x: 1920
  resolution_y: 1920
  file_format: PNG

imaging:
  output_path: ./output/basic_tutorial
  images_per_specimen: 1
  images_per_view: 1
  views:
    - aperture
    - apex
    - lateral

transforms: []  # No transforms for basic documentation
```

Then run:
```python
from traitblender.core import ConfigLoader, ImageRenderer

config = ConfigLoader.from_file("basic_imaging.yaml")
renderer = ImageRenderer(config)
renderer.render_specimen(specimen)
```

## Step 7: Review Results

Your output directory should now contain:
- `MySpecimen_aperture.png` - Bottom view showing aperture
- `MySpecimen_apex.png` - Top view showing apex  
- `MySpecimen_lateral.png` - Side profile view

## Tips for Better Results

### Lighting Optimization

1. **Adjust light positions** based on your specimen's features
2. **Use 3-point lighting** (key, fill, rim) for professional results
3. **Soften shadows** by increasing light size values
4. **Balance light intensities** to avoid overexposure

### Camera Positioning

1. **Frame your specimen** to fill ~70% of the image
2. **Use orthographic projection** for technical documentation
3. **Maintain consistent distances** across views
4. **Include a scale reference** if needed

### Rendering Quality

1. **Start with low samples** (64) for testing
2. **Increase samples** (256+) for final images
3. **Use denoising** for cleaner results with fewer samples
4. **Consider render time vs. quality** tradeoffs

## Common Issues and Solutions

### Specimen Too Dark
- Increase light energy values
- Add more light sources
- Check material properties (may be too dark)

### Noisy Renders
- Increase sample count
- Enable denoising in render properties
- Improve lighting setup

### Camera Not Focused on Specimen
- Check Track-To constraints
- Manually adjust camera positions
- Ensure specimen is at world origin

## Next Steps

Once you're comfortable with basic imaging:

1. Try the [Advanced Lighting Tutorial](./lighting.md)
2. Learn about [Custom Transforms](./custom-transforms.md)
3. Explore [Morphospace Visualization](./morphospace.md)
4. Set up [Batch Processing](../cli/batch-processing.md) for multiple specimens

## Complete Example Script

Here's a complete script that implements this tutorial:

```python
import bpy
import math
import os
from traitblender.core.positioning import GenericAsset

def setup_basic_specimen_imaging(specimen_path, output_dir):
    # Clear scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Import specimen
    bpy.ops.import_scene.obj(filepath=specimen_path)
    specimen_obj = bpy.context.selected_objects[0]
    specimen_obj.name = "Specimen"
    
    # Create specimen asset
    specimen = GenericAsset("Specimen")
    specimen.origin_set(type="BOTTOM_CENTER")
    
    # Create table
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
    bpy.context.active_object.name = "Table"
    table = SurfaceAsset("Table")
    
    # Place specimen
    table.place(specimen, (0, 0))
    
    # Set up lighting
    bpy.ops.object.light_add(type='AREA', location=(2, -2, 3))
    key_light = bpy.context.active_object
    key_light.data.energy = 50
    key_light.data.size = 2
    
    # Set up cameras and render
    cameras = {
        "aperture": (0, 0, -3, 0, 0, 0),
        "apex": (0, 0, 3, math.pi, 0, 0),
        "lateral": (3, 0, 0, math.pi/2, 0, math.pi/2)
    }
    
    # Configure rendering
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 128
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1920
    
    # Render each view
    for view_name, (x, y, z, rx, ry, rz) in cameras.items():
        bpy.ops.object.camera_add(location=(x, y, z), rotation=(rx, ry, rz))
        camera = bpy.context.active_object
        bpy.context.scene.camera = camera
        
        filename = f"specimen_{view_name}.png"
        bpy.context.scene.render.filepath = os.path.join(output_dir, filename)
        bpy.ops.render.render(write_still=True)
        
        bpy.data.objects.remove(camera)  # Clean up
    
    print("Basic imaging complete!")

# Usage
setup_basic_specimen_imaging(
    "/path/to/specimen.obj", 
    "/path/to/output/directory"
)
```

This tutorial provides a solid foundation for specimen imaging with TraitBlender. Practice with different specimens and lighting setups to develop your skills! 