# Imaging System

For Blender rendering documentation, see: [Blender Python API - Rendering](https://docs.blender.org/api/current/bpy.ops.render.html)

---

## Overview

The Imaging System orchestrates the final step of the TraitBlender workflow: rendering museum-quality images of specimens. It coordinates specimen generation, transform application, and image output to create training datasets for computer vision models.

**Key Features:**

- **Batch Rendering**: Process entire datasets automatically
- **Transform Integration**: Apply statistical variations per specimen
- **Output Management**: Organize rendered images with metadata
- **Progress Tracking**: Monitor rendering progress across large datasets
- **Format Support**: PNG, JPEG, OpenEXR, and other Blender-supported formats

---

## Architecture

### Imaging Pipeline Flow

```
1. Load Dataset
   ↓
2. For each specimen:
   ↓
3. Generate morphospace sample
   ↓
4. Apply transforms (optional)
   ↓
5. Position specimen
   ↓
6. Render from camera view
   ↓
7. Save with metadata
   ↓
8. Undo transforms
   ↓
9. Clean up specimen
   ↓
10. Next specimen
```

---

## Current State

!!! warning "Under Development"
    The Imaging System is currently under development. The basic rendering functionality works, but the automated pipeline operator (`TRAITBLENDER_OT_imaging_pipeline`) needs implementation.

### What Works

- ✅ Manual rendering via Blender's render operators
- ✅ Output configuration (format, directory, resolution)
- ✅ Metadata stamping
- ✅ Single specimen rendering

### What's Coming

- ⚠️ Automated batch rendering pipeline
- ⚠️ Progress tracking and cancellation
- ⚠️ Multi-view rendering (multiple camera angles)
- ⚠️ Render queue management
- ⚠️ Error handling and recovery

---

## Manual Rendering Workflow

Until the automated pipeline is complete, you can render specimens programmatically:

### Single Specimen

```python
import bpy

# Setup
config = bpy.context.scene.traitblender_config
dataset = bpy.context.scene.traitblender_dataset
setup = bpy.context.scene.traitblender_setup

# Configure output
config.output.output_directory = "C:/renders/shells/"
config.output.image_format = "PNG"

# Generate specimen
dataset.sample = "Shell_001"
bpy.ops.traitblender.generate_morphospace_sample()

# Render
bpy.context.scene.render.filepath = f"{config.output.output_directory}Shell_001.png"
bpy.ops.render.render(write_still=True)
```

### Batch Rendering

```python
import bpy
import os

config = bpy.context.scene.traitblender_config
dataset = bpy.context.scene.traitblender_dataset
setup = bpy.context.scene.traitblender_setup

# Configure output
output_dir = "C:/renders/shells/"
os.makedirs(output_dir, exist_ok=True)
config.output.output_directory = output_dir
config.output.image_format = "PNG"

# Render all specimens
for specimen_name in dataset.rownames:
    print(f"Rendering {specimen_name}...")
    
    # Generate specimen
    dataset.sample = specimen_name
    bpy.ops.traitblender.generate_morphospace_sample()
    
    # Set output path
    output_path = os.path.join(output_dir, f"{specimen_name}.png")
    bpy.context.scene.render.filepath = output_path
    
    # Render
    bpy.ops.render.render(write_still=True)
    
    # Clean up
    obj = bpy.data.objects.get(specimen_name)
    if obj:
        bpy.data.objects.remove(obj, do_unlink=True)
    
    print(f"✓ {specimen_name} rendered to {output_path}")

print(f"Batch rendering complete! {len(dataset.rownames)} specimens rendered.")
```

### With Transform Pipeline

```python
import bpy
import os

config = bpy.context.scene.traitblender_config
dataset = bpy.context.scene.traitblender_dataset

# Configure transforms for variation
transforms = config.transforms
transforms.clear()
transforms.add_transform("world.color", "dirichlet", {"alphas": [0.3, 0.3, 0.3, 1]})
transforms.add_transform("lamp.power", "gamma", {"alpha": 2, "beta": 5})
transforms.add_transform("camera.location", "normal", {"mu": 0, "sigma": 0.05, "n": 3})

# Configure output
output_dir = "C:/renders/shells_varied/"
os.makedirs(output_dir, exist_ok=True)

# Render multiple variations per specimen
images_per_specimen = 5

for specimen_name in dataset.rownames:
    print(f"Rendering {specimen_name} ({images_per_specimen} variations)...")
    
    # Generate specimen once
    dataset.sample = specimen_name
    bpy.ops.traitblender.generate_morphospace_sample()
    
    # Render multiple variations
    for i in range(images_per_specimen):
        # Apply transforms
        transforms.run()
        
        # Set output path
        output_path = os.path.join(output_dir, f"{specimen_name}_var{i:03d}.png")
        bpy.context.scene.render.filepath = output_path
        
        # Render
        bpy.ops.render.render(write_still=True)
        
        # Undo transforms for next variation
        transforms.undo()
        
        print(f"  ✓ Variation {i+1}/{images_per_specimen}")
    
    # Clean up specimen
    obj = bpy.data.objects.get(specimen_name)
    if obj:
        bpy.data.objects.remove(obj, do_unlink=True)
    
    print(f"✓ {specimen_name} complete ({images_per_specimen} images)")

total_images = len(dataset.rownames) * images_per_specimen
print(f"Batch rendering complete! {total_images} images rendered.")
```

---

## Output Configuration

Configure rendering output in the Configuration panel → Output section:

### Output Properties

**`output_directory`** - Directory path where images will be saved. Can be absolute or relative.

**`image_format`** - Output image format:
- `PNG` - Lossless compression, supports transparency
- `JPEG` - Lossy compression, smaller file size
- `OPEN_EXR` - HDR format for post-processing
- `TIFF` - High-quality, uncompressed

**`output_type`** - Output type:
- `image` - Single image per render
- `video` - Animation/video output (for future multi-frame rendering)

**`images_per_view`** - Number of images to render per view (for future multi-view support)

---

## Metadata Configuration

Configure image metadata in the Configuration panel → Metadata section:

### Metadata Stamps

Blender can embed metadata in rendered images. Enable/disable stamps:

- **Camera Name** (`use_stamp_camera`) - Include camera name
- **Date** (`use_stamp_date`) - Include render date
- **Filename** (`use_stamp_filename`) - Include output filename
- **Frame** (`use_stamp_frame`) - Include frame number
- **Render Time** (`use_stamp_render_time`) - Include render duration
- **Scene Name** (`use_stamp_scene`) - Include scene name
- **Custom Note** (`use_stamp_note`) - Include custom text (`stamp_note_text`)

### Example Metadata

When metadata stamps are enabled, the rendered image will include text overlay:

```
Camera: Camera | Date: 2025-01-21 | File: Shell_001.png
Scene: Scene | Time: 00:02.34 | Shell morphospace specimen
```

---

## Render Settings

Configure render engine and quality in the Configuration panel → Render section:

### Render Engine

**`engine`** - Blender render engine:
- `BLENDER_EEVEE_NEXT` - Real-time rendering (fast, good for previews and large datasets)
- `CYCLES` - Ray-traced rendering (slow, photorealistic)
- `BLENDER_WORKBENCH` - Viewport rendering (very fast, lower quality)

**`eevee_use_raytracing`** - Enable ray tracing in EEVEE (better reflections/shadows, slower)

### Resolution

Resolution is configured in the Camera section:
- `resolution_x` - Image width in pixels
- `resolution_y` - Image height in pixels
- `resolution_percentage` - Scale factor (50% = half resolution, faster renders)

---

## Planned Features

### Automated Pipeline Operator

The `TRAITBLENDER_OT_imaging_pipeline` operator (currently a stub in `ui/operators/imaging_pipeline_operator.py`) will provide:

**Features:**
- Start/stop/pause rendering
- Progress bar with ETA
- Error recovery (skip failed specimens)
- Render queue management
- Log file generation

**Usage:**
```python
# In GUI: Click "Run Imaging Pipeline" button
# In API:
bpy.ops.traitblender.imaging_pipeline()
```

### Multi-View Rendering

Render specimens from multiple camera angles automatically:

```python
config.output.images_per_view = 3  # Front, side, top views

# System will:
# 1. Position camera at front view
# 2. Render → specimen_front.png
# 3. Rotate camera 90°
# 4. Render → specimen_side.png
# 5. Position camera top-down
# 6. Render → specimen_top.png
```

### Render Profiles

Save/load complete rendering configurations:

```python
# Save current settings
bpy.ops.traitblender.save_render_profile(name="high_quality")

# Load profile
bpy.ops.traitblender.load_render_profile(name="high_quality")
```

---

## Performance Optimization

### Tips for Faster Rendering

**1. Use EEVEE instead of Cycles**
```python
config.render.engine = "BLENDER_EEVEE_NEXT"
config.render.eevee_use_raytracing = False
```

**2. Reduce resolution for testing**
```python
config.camera.resolution_percentage = 50  # Render at 50% resolution
```

**3. Disable metadata stamps**
```python
config.metadata.use_stamp_camera = False
config.metadata.use_stamp_date = False
# ... disable others
```

**4. Use PNG compression**
```python
config.output.image_format = "PNG"
bpy.context.scene.render.image_settings.compression = 15  # 0-100, higher = smaller files
```

**5. Render in background mode**
```bash
blender --background scene.blend --python render_script.py
```

---

## Troubleshooting

### Common Issues

**Problem: Renders are blank/black**
- Check camera position (`config.camera.location`)
- Verify lamp power (`config.lamp.power`)
- Ensure specimen is positioned on table (`obj.tb_location`)

**Problem: Renders are slow**
- Switch to EEVEE engine
- Reduce resolution percentage
- Disable ray tracing
- Lower specimen geometry complexity

**Problem: Out of memory errors**
- Reduce resolution
- Clean up unused specimens between renders
- Render in smaller batches

**Problem: Transform pipeline errors**
- Verify transform parameters are valid
- Check property paths exist
- Test transforms on single specimen first

---

## Implementation Status

Current implementation in `ui/operators/imaging_pipeline_operator.py`:

```python
class TRAITBLENDER_OT_imaging_pipeline(Operator):
    """Iterate through the dataset and update the sample value on a timer"""
    bl_idname = "traitblender.imaging_pipeline"
    bl_label = "Run Imaging Pipeline"
    
    def modal(self, context, event):
        pass  # TODO: Implement modal operator
    
    def execute(self, context):
        pass  # TODO: Implement batch rendering
    
    def cancel(self, context):
        pass  # TODO: Implement cleanup
```

**To implement:**
1. Modal operator with timer for progress updates
2. Iterator over dataset rows
3. Specimen generation + transform application
4. Render with proper output paths
5. Progress tracking and cancellation
6. Error handling and logging

---

## See Also

- [Configuration System](./configuration-system.md) - Output and render settings
- [Transform Pipeline](./transform-pipeline.md) - Applying variations
- [Dataset Management](./dataset-management.md) - Working with specimen data

