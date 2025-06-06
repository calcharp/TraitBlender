# Configuration Files

TraitBlender uses YAML configuration files to define rendering pipelines, transforms, and output settings. This allows for reproducible, automated generation of museum-style morphological images.

## Configuration File Structure

Configuration files are organized into several main sections:

### Basic Structure

```yaml
blender_preferences:
  use_online_access: True

morphospace: 
  name: ContrerasMorphospace
  path: /path/to/morphospace/data

dataset:
  # Dataset configuration

rendering:
  render_engine: Cycles
  compute_device_type: CUDA 

imaging:
  output_path: /path/to/output/directory
  images_per_specimen: 1
  images_per_view: 1
  views:
    - bottom
    - apex
    - aperture

transforms:
  - GaussianCameraRotation:
      mu: 0
      sigma: 0.1
  - GaussianSpecimenRotation:
      mu: 0
      sigma: 0.1
  # Additional transforms...
```

## Configuration Sections

### blender_preferences

Controls Blender-specific settings that affect rendering behavior.

```yaml
blender_preferences:
  use_online_access: True  # Allow Blender to access online resources
```

**Options:**
- `use_online_access` (boolean): Whether Blender can access online resources for textures, etc.

### morphospace

Defines the morphospace to be used for specimen visualization.

```yaml
morphospace: 
  name: ContrerasMorphospace      # Unique identifier for the morphospace
  path: /path/to/morphospace/data # Path to morphospace data files
```

**Required Fields:**
- `name` (string): Name/identifier for the morphospace
- `path` (string): File system path to the morphospace data

### dataset

Configuration for the dataset containing specimen information.

```yaml
dataset:
  path: /path/to/dataset.csv
  specimen_column: specimen_id
  trait_columns:
    - trait1
    - trait2
    - trait3
```

**Fields:**
- `path` (string): Path to the dataset file
- `specimen_column` (string): Column name containing specimen identifiers
- `trait_columns` (list): List of trait columns to include in analysis

### rendering

Controls the Blender rendering engine and performance settings.

```yaml
rendering:
  render_engine: Cycles           # Rendering engine (Cycles/Eevee)
  compute_device_type: CUDA       # GPU acceleration type
  samples: 128                    # Number of render samples
  resolution_x: 1920              # Output width in pixels
  resolution_y: 1080              # Output height in pixels
  file_format: PNG                # Output file format
```

**Options:**
- `render_engine`: 
  - `Cycles`: Ray-tracing engine for photorealistic results
  - `Eevee`: Real-time engine for faster rendering
- `compute_device_type`:
  - `CUDA`: NVIDIA GPU acceleration
  - `OPENCL`: OpenCL GPU acceleration
  - `CPU`: CPU-only rendering
- `samples` (integer): Render quality (higher = better quality, slower)
- `resolution_x/y` (integer): Output image dimensions
- `file_format`: `PNG`, `JPEG`, `TIFF`, `EXR`

### imaging

Defines output settings and camera views for specimen imaging.

```yaml
imaging:
  output_path: /path/to/output/directory
  images_per_specimen: 3          # Number of images per specimen
  images_per_view: 1              # Number of images per camera view
  views:                          # List of camera views
    - bottom                      # Bottom view (aperture)
    - apex                        # Top view (apex)
    - aperture                    # Aperture view
    - lateral                     # Side view
    - oblique                     # Angled view
```

**Standard Views:**
- `bottom`: Bottom-up view showing aperture
- `apex`: Top-down view showing apex
- `aperture`: Direct aperture view
- `lateral`: Side profile view
- `oblique`: 45-degree angled view

### transforms

List of transformations to apply during rendering for data augmentation and variation.

```yaml
transforms:
  - GaussianCameraRotation:       # Random camera rotation
      mu: 0                       # Mean rotation (radians)
      sigma: 0.1                  # Standard deviation
      
  - GaussianSpecimenRotation:     # Random specimen rotation
      mu: 0
      sigma: 0.1
      
  - GaussianSpecimenTranslation:  # Random specimen position
      mu: 0
      sigma: 0.1
      
  - RandomizeWorldColor:          # Random background color
      # No parameters needed
      
  - RandomLampPlacement:          # Random light positioning
      # No parameters needed
      
  - GaussianLampRotation:         # Random light rotation
      mu: 0
      sigma: 0.1
      
  - GaussianLampTranslation:      # Random light position
      mu: 0
      sigma: 0.1
```

## Example Configurations

### Basic Museum Documentation

```yaml
blender_preferences:
  use_online_access: False

morphospace: 
  name: MuseumCollection2024
  path: ./data/morphospaces/museum_collection.json

dataset:
  path: ./data/specimens.csv
  specimen_column: catalog_number
  trait_columns:
    - length_mm
    - width_mm
    - height_mm

rendering:
  render_engine: Cycles
  compute_device_type: CUDA
  samples: 256
  resolution_x: 2048
  resolution_y: 2048
  file_format: PNG

imaging:
  output_path: ./output/museum_docs
  images_per_specimen: 1
  images_per_view: 1
  views:
    - bottom
    - apex
    - lateral

transforms: []  # No transforms for documentation
```

### Research Data Augmentation

```yaml
blender_preferences:
  use_online_access: True

morphospace: 
  name: ResearchDataset
  path: ./data/morphospaces/research_data.json

dataset:
  path: ./data/research_specimens.csv
  specimen_column: specimen_id
  trait_columns:
    - pc1
    - pc2
    - pc3

rendering:
  render_engine: Cycles
  compute_device_type: CUDA
  samples: 128
  resolution_x: 1024
  resolution_y: 1024
  file_format: PNG

imaging:
  output_path: ./output/research_augmented
  images_per_specimen: 10
  images_per_view: 2
  views:
    - bottom
    - apex
    - aperture
    - lateral
    - oblique

transforms:
  - GaussianCameraRotation:
      mu: 0
      sigma: 0.05
  - GaussianSpecimenRotation:
      mu: 0
      sigma: 0.1
  - GaussianSpecimenTranslation:
      mu: 0
      sigma: 0.05
  - RandomizeWorldColor: {}
  - RandomLampPlacement: {}
  - GaussianLampRotation:
      mu: 0
      sigma: 0.2
```

## Using Configuration Files

### Command Line

```bash
# Run with a specific configuration
traitblender --config ./configs/museum_documentation.yaml

# Override specific settings
traitblender --config ./configs/base.yaml --output-path ./custom_output
```

### Python API

```python
from traitblender.core import ConfigLoader

# Load configuration
config = ConfigLoader.from_file("./configs/research.yaml")

# Access configuration sections
render_settings = config.rendering
imaging_settings = config.imaging

# Override settings programmatically
config.imaging.output_path = "./new_output_path"
```

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
│   ├── morphospaces/
│   └── specimens.csv
└── output/
```

### Configuration Tips

1. **Start with Base Config**: Create a base configuration and extend it for specific use cases
2. **Document Transforms**: Comment your transform parameters for reproducibility
3. **Version Control**: Keep configuration files in version control
4. **Validation**: Test configurations with small datasets first
5. **Performance**: Balance quality (samples) with rendering time for your use case

### Common Patterns

**High Quality Documentation:**
- High samples (256+)
- High resolution (2048x2048+)
- No transforms
- Standard views only

**Research Data Augmentation:**
- Moderate samples (128)
- Multiple views and variations
- Gaussian transforms for variation
- Multiple images per specimen

**Quick Testing:**
- Low samples (32-64)
- Lower resolution (512x512)
- Single view
- Minimal transforms 