# Asset Management

---

## Overview

The Asset Management system provides path resolution, directory initialization, and resource management for TraitBlender's assets (morphospaces, configs, materials, textures, scenes). It handles both bundled assets and user-specific data directories.

**Key Features:**

- **Path Resolution (`get_asset_path`)**: Locate bundled assets relative to add-on root
- **User Directories (`init_user_dirs`)**: Create/manage user-specific data directories
- **Material Management (`apply_material`)**: Apply materials and textures to objects
- **Cross-Platform**: Works on Windows, macOS, Linux
- **Flexible Structure**: Supports both development and installed add-on layouts

**Use Cases:**

- Load morphospace modules from `assets/morphospace_modules/`
- Load default config from `assets/configs/default.yaml`
- Import museum scene from `assets/scenes/museum_scene.blend`
- Create user config directory in `~/.config/traitblender/`
- Apply materials/textures to specimens

---

## Architecture

### Component Overview

```
Asset Management
├── Path Resolution
│   ├── get_asset_path() - Find bundled assets
│   ├── Handles development vs installed layouts
│   └── Supports nested paths
│
├── Directory Structure
│   ├── assets/ (bundled with add-on)
│   │   ├── configs/
│   │   ├── morphospace_modules/
│   │   ├── scenes/
│   │   ├── materials/
│   │   └── textures/
│   │
│   └── User data (created by init_user_dirs)
│       └── ~/.config/traitblender/
│           ├── configs/
│           ├── exports/
│           └── logs/
│
├── Material Management
│   ├── apply_material() - Apply material to object
│   ├── _create_textured_material() - Create material with textures
│   └── set_textures() - Apply texture images
│
└── Initialization
    ├── init_user_dirs() - Create user directories
    └── Called on add-on registration
```

### Data Flow

```
1. Add-on loads
   __init__.py → init_user_dirs()
   ↓
2. Create user directories
   ~/.config/traitblender/configs/
   ~/.config/traitblender/exports/
   ~/.config/traitblender/logs/
   ↓
3. User requests asset (e.g., load config)
   config_path = get_asset_path("configs", "default.yaml")
   ↓
4. Resolve path
   Add-on root: /path/to/traitblender/
   Asset subpath: assets/configs/default.yaml
   Full path: /path/to/traitblender/assets/configs/default.yaml
   ↓
5. Return path
   → Load YAML from resolved path
```

---

## Path Resolution

### `get_asset_path()`

Resolves paths to bundled assets relative to add-on root.

**Location:** `core/helpers/addon_helpers.py`

```python
def get_asset_path(*path_parts):
    """
    Get absolute path to asset bundled with the add-on.
    
    Args:
        *path_parts: Path components relative to assets/ directory
    
    Returns:
        str: Absolute path to asset
    
    Examples:
        get_asset_path("configs", "default.yaml")
        → /path/to/traitblender/assets/configs/default.yaml
        
        get_asset_path("morphospace_modules")
        → /path/to/traitblender/assets/morphospace_modules/
        
        get_asset_path("scenes", "museum_scene.blend")
        → /path/to/traitblender/assets/scenes/museum_scene.blend
    """
    import os
    
    # Get add-on root directory
    # Uses get_addon_root() from addon_helpers
    addon_root = get_addon_root()
    
    # Build path: addon_root/assets/path_parts
    asset_path = os.path.join(addon_root, "assets", *path_parts)
    
    # Normalize path (resolve .. and .)
    asset_path = os.path.normpath(asset_path)
    
    return asset_path
```

**Key characteristics:**
- Returns absolute path (not relative)
- Does NOT check if file exists (caller's responsibility)
- Works with development and installed add-on layouts
- Handles nested paths via `*path_parts`

### Usage Examples

**Load default config:**
```python
from core.helpers import get_asset_path
import yaml

config_path = get_asset_path("configs", "default.yaml")
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)
```

**List morphospaces:**
```python
morphospace_dir = get_asset_path("morphospace_modules")
morphospaces = [d for d in os.listdir(morphospace_dir) 
                if os.path.isdir(os.path.join(morphospace_dir, d))]
```

**Load museum scene:**
```python
scene_path = get_asset_path("scenes", "museum_scene.blend")

# Append objects from scene
with bpy.data.libraries.load(scene_path) as (data_from, data_to):
    data_to.objects = data_from.objects
```

**Get texture path:**
```python
texture_path = get_asset_path("textures", "wood_grain.jpg")
# Use with apply_material() or set_textures()
```

### Path Components

**Valid path parts:**
```python
# Single component
get_asset_path("configs")
→ .../assets/configs/

# Multiple components
get_asset_path("morphospace_modules", "Shell", "__init__.py")
→ .../assets/morphospace_modules/Shell/__init__.py

# Deeply nested
get_asset_path("materials", "specimens", "shell_material.blend")
→ .../assets/materials/specimens/shell_material.blend
```

**Invalid usage:**
```python
# ✗ Don't include "assets" in path_parts (automatically added)
get_asset_path("assets", "configs", "default.yaml")  # Wrong

# ✓ Correct
get_asset_path("configs", "default.yaml")  # Right

# ✗ Don't use absolute paths
get_asset_path("/home/user/config.yaml")  # Wrong

# ✓ Use for bundled assets only
get_asset_path("configs", "default.yaml")  # Right
```

---

## Directory Structure

### Bundled Assets (`assets/`)

Located in add-on installation directory:

```
TraitBlender/
└── assets/
    ├── configs/
    │   └── default.yaml           # Default configuration
    │
    ├── morphospace_modules/
    │   ├── Shell/
    │   │   ├── __init__.py
    │   │   └── morphospace/
    │   │       ├── shell_morphospace.py
    │   │       └── shell_morphospace_sample.py
    │   └── [other morphospaces]/
    │
    ├── scenes/
    │   └── museum_scene.blend     # Museum table/camera/lamp setup
    │
    ├── materials/
    │   └── [material .blend files]
    │
    └── textures/
        └── [texture images]
```

**Access bundled assets:**
```python
get_asset_path("configs", "default.yaml")
get_asset_path("morphospace_modules", "Shell")
get_asset_path("scenes", "museum_scene.blend")
```

### User Data Directories

Created in user's home directory:

**Linux/macOS:**
```
~/.config/traitblender/
├── configs/      # User configuration files
├── exports/      # Exported renders, configs
└── logs/         # Log files (future use)
```

**Windows:**
```
C:\Users\<username>\AppData\Roaming\traitblender\
├── configs\
├── exports\
└── logs\
```

**Creation:**
```python
# Called during add-on registration
init_user_dirs()

# Creates directories if they don't exist
# Safe to call multiple times (idempotent)
```

**Getting user directories:**
```python
import os

# User config directory
user_config_dir = os.path.expanduser("~/.config/traitblender/configs")

# Cross-platform (recommended)
import platform
if platform.system() == "Windows":
    user_dir = os.path.expanduser("~/AppData/Roaming/traitblender")
else:
    user_dir = os.path.expanduser("~/.config/traitblender")
```

---

## User Directory Initialization

### `init_user_dirs()`

Creates user data directories on add-on first run.

**Location:** `core/helpers/addon_helpers.py`

```python
def init_user_dirs():
    """
    Initialize user-specific TraitBlender directories.
    
    Creates:
        Linux/macOS: ~/.config/traitblender/{configs,exports,logs}
        Windows: %APPDATA%/traitblender/{configs,exports,logs}
    
    Safe to call multiple times (idempotent).
    """
    import os
    import platform
    
    # Determine base user directory
    if platform.system() == "Windows":
        base_dir = os.path.expanduser("~/AppData/Roaming/traitblender")
    else:
        base_dir = os.path.expanduser("~/.config/traitblender")
    
    # Subdirectories to create
    subdirs = ["configs", "exports", "logs"]
    
    # Create directories
    for subdir in subdirs:
        dir_path = os.path.join(base_dir, subdir)
        try:
            os.makedirs(dir_path, exist_ok=True)
            print(f"TraitBlender: Created directory {dir_path}")
        except OSError as e:
            print(f"TraitBlender: Failed to create {dir_path}: {e}")
    
    return base_dir
```

**When it's called:**
```python
# In __init__.py (add-on registration)
def register():
    # ... register classes ...
    
    # Initialize user directories
    init_user_dirs()
    
    # ... configure TraitBlender ...
```

**Safe to call multiple times:**
```python
# First call: Creates directories
init_user_dirs()
# Output: "Created directory /home/user/.config/traitblender/configs"

# Second call: Directories exist, no-op
init_user_dirs()
# Output: (nothing, os.makedirs with exist_ok=True)
```

### Use Cases for User Directories

**Save user configs:**
```python
import os
import yaml

# Get user config directory
user_config_dir = os.path.expanduser("~/.config/traitblender/configs")

# Save config
config_path = os.path.join(user_config_dir, "my_config.yaml")
with open(config_path, 'w') as f:
    yaml.dump(config_data, f)
```

**Export renders:**
```python
# Get export directory
export_dir = os.path.expanduser("~/.config/traitblender/exports")

# Save render
render_path = os.path.join(export_dir, "render_001.png")
bpy.context.scene.render.filepath = render_path
bpy.ops.render.render(write_still=True)
```

**Log errors:**
```python
import datetime

log_dir = os.path.expanduser("~/.config/traitblender/logs")
log_path = os.path.join(log_dir, f"traitblender_{datetime.date.today()}.log")

with open(log_path, 'a') as f:
    f.write(f"{datetime.datetime.now()}: Error occurred\n")
```

---

## Material Management

### `apply_material()`

Applies material to Blender object, optionally with textures.

**Location:** `core/helpers/material_helpers.py`

```python
def apply_material(obj, material_name, textures=None):
    """
    Apply material to object, optionally with textures.
    
    Args:
        obj: Blender object to apply material to
        material_name (str): Name of material to create/use
        textures (dict, optional): Texture configuration
            {
                'base_color': 'path/to/texture.jpg',
                'roughness': 'path/to/roughness.jpg',
                'normal': 'path/to/normal.jpg',
                'metallic': 'path/to/metallic.jpg'
            }
    
    Returns:
        bpy.types.Material: The applied material
    
    Examples:
        # Simple material (no textures)
        apply_material(obj, "SimpleMaterial")
        
        # Material with textures
        apply_material(obj, "WoodMaterial", {
            'base_color': get_asset_path("textures", "wood_color.jpg"),
            'roughness': get_asset_path("textures", "wood_rough.jpg")
        })
    """
    import bpy
    
    # Get or create material
    mat = bpy.data.materials.get(material_name)
    if mat is None:
        mat = bpy.data.materials.new(name=material_name)
        mat.use_nodes = True
    
    # Clear existing material slots
    obj.data.materials.clear()
    
    # Apply material
    obj.data.materials.append(mat)
    
    # Apply textures if provided
    if textures:
        set_textures(mat, textures)
    
    return mat
```

### `set_textures()`

Applies texture images to material node tree.

```python
def set_textures(material, textures):
    """
    Apply textures to material's node tree.
    
    Args:
        material: Blender material with node tree
        textures (dict): Texture paths by type
            {
                'base_color': path,
                'roughness': path,
                'normal': path,
                'metallic': path
            }
    
    Creates:
        - Image Texture nodes for each texture
        - Connects to Principled BSDF shader
        - Normal Map node for normal textures
    """
    import bpy
    
    if not material.use_nodes:
        material.use_nodes = True
    
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    # Get Principled BSDF (or create)
    bsdf = nodes.get("Principled BSDF")
    if bsdf is None:
        bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    
    # Apply each texture
    x_offset = -300
    y_offset = 0
    
    for tex_type, tex_path in textures.items():
        if not os.path.exists(tex_path):
            print(f"Warning: Texture not found: {tex_path}")
            continue
        
        # Create Image Texture node
        tex_node = nodes.new(type="ShaderNodeTexImage")
        tex_node.image = bpy.data.images.load(tex_path)
        tex_node.location = (x_offset, y_offset)
        y_offset -= 300
        
        # Connect to BSDF
        if tex_type == 'base_color':
            links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])
        
        elif tex_type == 'roughness':
            links.new(tex_node.outputs['Color'], bsdf.inputs['Roughness'])
        
        elif tex_type == 'metallic':
            links.new(tex_node.outputs['Color'], bsdf.inputs['Metallic'])
        
        elif tex_type == 'normal':
            # Normal maps require Normal Map node
            normal_map = nodes.new(type="ShaderNodeNormalMap")
            normal_map.location = (x_offset + 200, y_offset)
            links.new(tex_node.outputs['Color'], normal_map.inputs['Color'])
            links.new(normal_map.outputs['Normal'], bsdf.inputs['Normal'])
```

### Usage Examples

**Simple colored material:**
```python
from core.helpers import apply_material

# Create object
bpy.ops.mesh.primitive_uv_sphere_add()
obj = bpy.context.active_object

# Apply simple material
mat = apply_material(obj, "SpecimenMaterial")

# Set color
bsdf = mat.node_tree.nodes.get("Principled BSDF")
bsdf.inputs['Base Color'].default_value = (0.8, 0.6, 0.4, 1.0)  # Beige
bsdf.inputs['Roughness'].default_value = 0.5
```

**Textured material:**
```python
from core.helpers import apply_material, get_asset_path

# Get texture paths
textures = {
    'base_color': get_asset_path("textures", "shell_color.jpg"),
    'roughness': get_asset_path("textures", "shell_rough.jpg"),
    'normal': get_asset_path("textures", "shell_normal.jpg")
}

# Apply material with textures
apply_material(obj, "ShellMaterial", textures=textures)
```

**Material from config:**
```python
# In setup_scene_operator.py
config = context.scene.traitblender_config
mat_config = config.mat

# Get or create mat object
mat = bpy.data.objects.get("Mat")

# Apply material
mat_material = apply_material(mat, "MuseumMat")

# Configure from config
bsdf = mat_material.node_tree.nodes.get("Principled BSDF")
bsdf.inputs['Base Color'].default_value = (*mat_config.color, 1.0)
bsdf.inputs['Roughness'].default_value = mat_config.roughness
```
