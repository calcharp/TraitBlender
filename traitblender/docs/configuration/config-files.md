# Configuration Files

TraitBlender uses YAML configuration files to define scene settings, transforms, and output options. This allows for reproducible, automated generation of museum-style morphological images.

## Configuration File Structure

Configuration files are organized into several main sections that correspond to different aspects of the scene. The structure matches the `traitblender_config` PropertyGroup in Blender.

### Basic Structure

```yaml
---
world:
  color: [0.0, 0.0, 0.0, 1.0]
  strength: 1.0
camera:
  location: [0.0, 0.0, 1.0]
  rotation: [0.0, 0.0, 0.0]
  focal_length: 60.0
  resolution_x: 1080
  resolution_y: 1080
  resolution_percentage: 100
lamp:
  location: [0.0, 0.0, 1.0]
  power: 10.0
  color: [1.0, 1.0, 1.0]
mat:
  color: [0.0, 0.0, 0.0, 1.0]
  location: [0.0, 0.0, 0.59]
render:
  engine: BLENDER_EEVEE_NEXT
output:
  output_directory: ""
  image_format: PNG
transforms:
  []
```

## Configuration Sections

### world

Controls the world/background settings.

```yaml
world:
  color: [0.0, 0.0, 0.0, 1.0]  # RGBA background color
  strength: 1.0                 # Background light strength
```

**Fields:**
- `color` (list[float, float, float, float]): RGBA color values (0.0-1.0)
- `strength` (float): Intensity of background lighting

### camera

Camera position, rotation, and rendering settings.

```yaml
camera:
  location: [0.0, 0.0, 1.0]           # Camera position (table coordinates)
  rotation: [0.0, 0.0, 0.0]          # Camera rotation (Euler angles)
  focal_length: 60.0                 # Focal length in mm
  camera_type: PERSP                 # PERSP, ORTHO, or PANO
  resolution_x: 1920                 # Render width
  resolution_y: 1080                 # Render height
  resolution_percentage: 100          # Render resolution percentage
  aspect_x: 1.0                      # Pixel aspect ratio X
  aspect_y: 1.0                      # Pixel aspect ratio Y
  shift_x: 0.0                       # Camera shift X
  shift_y: 0.0                       # Camera shift Y
  lens_unit: MILLIMETERS             # MILLIMETERS or FOV
```

**Fields:**
- `location` (list[float, float, float]): Position relative to table center (in meters)
- `rotation` (list[float, float, float]): Euler rotation angles
- `focal_length` (float): Camera lens focal length
- `camera_type` (string): `PERSP`, `ORTHO`, or `PANO`
- `resolution_x/y` (int): Output image dimensions
- `resolution_percentage` (int): Render resolution percentage (0-100)

### lamp

Lighting configuration.

```yaml
lamp:
  location: [0.0, 0.0, 1.0]      # Light position (table coordinates)
  rotation: [0.0, 0.0, 0.0]      # Light rotation
  power: 10.0                    # Light power/energy
  color: [1.0, 1.0, 1.0]         # RGB light color
  scale: [1.0, 1.0, 1.0]         # Light scale
  shadow: true                    # Enable shadows
  beam_size: 1.0                  # Beam size (for area lights)
  beam_blend: 0.0                 # Beam blend
  diffuse: 1.0                    # Diffuse light contribution
  use_soft_falloff: true          # Use soft falloff
```

### mat

Specimen mat/background surface settings.

```yaml
mat:
  color: [0.0, 0.0, 0.0, 1.0]    # Mat color (RGBA)
  location: [0.0, 0.0, 0.59]      # Mat position
  rotation: [0.0, 0.0, 0.0]       # Mat rotation
  scale: [0.125, 0.125, 1.0]      # Mat scale
  roughness: 0.0                  # Material roughness
```

### render

Render engine settings.

```yaml
render:
  engine: BLENDER_EEVEE_NEXT      # BLENDER_EEVEE_NEXT or CYCLES
  eevee_use_raytracing: false     # Enable Eevee ray tracing
```

### output

Output file settings.

```yaml
output:
  output_directory: ""            # Output directory path
  image_format: PNG               # PNG, JPEG, TIFF, etc.
  output_type: image              # Output type
  images_per_view: 1              # Images per camera view
```

### metadata

Information to include in rendered images.

```yaml
metadata:
  use_stamp_camera: true          # Include camera info
  use_stamp_date: true            # Include date
  use_stamp_filename: true        # Include filename
  use_stamp_frame: true           # Include frame number
  use_stamp_render_time: true     # Include render time
  use_stamp_scene: true           # Include scene name
  use_stamp_time: true            # Include time
  stamp_note_text: ""             # Custom note text
  # Additional stamp options available
```

### orientations

Orientation function to apply to specimens (defined by each morphospace).

```yaml
orientations:
  orientation: NONE  # Or morphospace-specific: Default, Aperture Up, etc.
```

### transforms

Transform pipeline for data augmentation. This is a list of transform definitions.

```yaml
transforms:
  - property_path: world.color
    sampler_name: uniform
    params:
      low: 0.0
      high: 1.0
  - property_path: camera.location
    sampler_name: normal
    params:
      mu: 0
      sigma: 0.5
      n: 3
  - property_path: world.strength
    sampler_name: beta
    params:
      a: 2
      b: 5
```

**Transform Structure:**
- `property_path` (string): Relative path to config property (e.g., "world.color", "camera.location")
- `sampler_name` (string): Statistical distribution to use
- `params` (dict): Parameters for the sampler function

**Available Samplers:**

| Sampler | Parameters | Description |
|---------|-----------|-------------|
| `uniform` | `low`, `high` | Uniform distribution |
| `normal` | `mu`, `sigma`, optional `n` | Normal (Gaussian) distribution |
| `beta` | `a`, `b` | Beta distribution |
| `gamma` | `alpha`, `beta` | Gamma distribution |
| `dirichlet` | `alphas` (list) | Dirichlet distribution (for color vectors) |
| `multivariate_normal` | `mu` (list), `cov` (list of lists) | Multivariate normal distribution |
| `poisson` | `lam` | Poisson distribution |
| `exponential` | `lambd` | Exponential distribution |
| `cauchy` | `x0`, `gamma` | Cauchy distribution |
| `discrete_uniform` | `low`, `high` (integers) | Discrete uniform distribution |

## Example Configurations

### Basic Museum Documentation

```yaml
---
world:
  color: [0.0, 0.0, 0.0, 1.0]
  strength: 1.0
camera:
  location: [0.0, 0.0, 1.0]
  rotation: [0.0, 0.0, 0.0]
  focal_length: 60.0
  resolution_x: 2048
  resolution_y: 2048
  resolution_percentage: 100
lamp:
  location: [0.0, 0.0, 1.0]
  power: 10.0
  color: [1.0, 1.0, 1.0]
render:
  engine: BLENDER_EEVEE_NEXT
output:
  output_directory: "./output/museum_docs"
  image_format: PNG
transforms: []  # No transforms for documentation
```

### Research Data Augmentation

```yaml
---
world:
  color: [0.0, 0.0, 0.0, 1.0]
  strength: 1.0
camera:
  location: [0.0, 0.0, 1.0]
  rotation: [0.0, 0.0, 0.0]
  focal_length: 50.0
  resolution_x: 1024
  resolution_y: 1024
  resolution_percentage: 100
lamp:
  location: [0.0, 0.0, 1.0]
  power: 10.0
  color: [1.0, 1.0, 1.0]
render:
  engine: BLENDER_EEVEE_NEXT
output:
  output_directory: "./output/research_augmented"
  image_format: PNG
transforms:
  - property_path: world.color
    sampler_name: dirichlet
    params:
      alphas: [1.0, 1.0, 1.0, 1.0]
  - property_path: camera.location
    sampler_name: normal
    params:
      mu: 0
      sigma: 0.2
      n: 3
  - property_path: lamp.power
    sampler_name: gamma
    params:
      alpha: 3.0
      beta: 2.0
```

## Using Configuration Files

### In Blender GUI

1. In the **Museum Setup** panel, enter the path to your YAML file in the **Config File** field
2. Click **Configure Scene** to load the configuration
3. The configuration will be applied to the current scene

### Python API

```python
import bpy
import yaml

# Load configuration from YAML file
with open("my_config.yaml", 'r') as f:
    config_data = yaml.safe_load(f)

# Apply to scene
bpy.context.scene.traitblender_config.from_dict(config_data)

# Export current configuration
config_dict = bpy.context.scene.traitblender_config.to_dict()
with open("exported_config.yaml", 'w') as f:
    yaml.dump(config_dict, f)

# View configuration as YAML string
config_yaml = str(bpy.context.scene.traitblender_config)
print(config_yaml)
```

### Exporting Configuration

You can export the current configuration from the GUI:
1. Go to the **Configuration** panel
2. Click **Export Config as YAML**
3. Save the file for reuse

## Property Paths

When defining transforms, use relative property paths that match the configuration structure:

- `world.color` - World background color
- `world.strength` - World background strength
- `camera.location` - Camera position (3D vector)
- `camera.rotation` - Camera rotation (3D vector)
- `camera.focal_length` - Camera focal length
- `camera.resolution_x` - Render width
- `camera.resolution_y` - Render height
- `lamp.location` - Light position
- `lamp.power` - Light power
- `lamp.color` - Light color (3D vector)
- `mat.color` - Mat color
- `mat.location` - Mat position

## Best Practices

### File Organization

```
project/
├── configs/
│   ├── base.yaml              # Base configuration
│   ├── museum_docs.yaml       # Museum documentation
│   ├── research_augment.yaml  # Research with augmentation
│   └── quick_test.yaml        # Fast testing configuration
├── data/
│   └── specimens.csv
└── output/
```

### Configuration Tips

1. **Start with Base Config**: Create a base configuration and extend it for specific use cases
2. **Document Transforms**: Comment your transform parameters for reproducibility
3. **Version Control**: Keep configuration files in version control
4. **Validation**: Test configurations with small datasets first
5. **Performance**: Balance quality (resolution) with rendering time for your use case

### Common Patterns

**High Quality Documentation:**
- High resolution (2048x2048+)
- No transforms
- Standard camera settings

**Research Data Augmentation:**
- Moderate resolution (1024x1024)
- Multiple transforms for variation
- Statistical sampling on multiple properties

**Quick Testing:**
- Lower resolution (512x512)
- Minimal transforms
- Fast render engine (EEVEE)

## Transform Examples

### Color Variation

```yaml
transforms:
  - property_path: world.color
    sampler_name: dirichlet
    params:
      alphas: [0.8, 0.8, 0.8, 1.0]  # Slight color variation
```

### Camera Movement

```yaml
transforms:
  - property_path: camera.location
    sampler_name: multivariate_normal
    params:
      mu: [0, 0, 0]
      cov: [[0.1, 0, 0], [0, 0.1, 0], [0, 0, 0.05]]  # Small position variation
```

### Lighting Variation

```yaml
transforms:
  - property_path: lamp.power
    sampler_name: gamma
    params:
      alpha: 3.0
      beta: 2.0
  - property_path: lamp.color
    sampler_name: dirichlet
    params:
      alphas: [1.0, 1.0, 1.0]  # Slight color temperature variation
```
