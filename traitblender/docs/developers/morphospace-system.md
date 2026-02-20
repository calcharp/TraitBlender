# Morphospace System

For mathematical morphospace concepts, see: [Theoretical Morphology](https://en.wikipedia.org/wiki/Theoretical_morphology)

---

## Overview

The Morphospace System provides a pluggable architecture for generating 3D specimens from mathematical models. Morphospaces are self-contained Python modules that convert trait parameters into Blender geometry, enabling researchers to create diverse specimen collections from morphological datasets.

**Key Features:**

- **Pluggable Architecture**: Drop morphospace modules into `assets/morphospace_modules/` - auto-discovered
- **Dataset Integration**: Automatic parameter mapping from dataset columns to morphospace functions
- **Standard Interface**: All morphospaces follow the same `sample()` → `to_blender()` pattern
- **Isolated Modules**: Each morphospace is self-contained with its own dependencies and logic
- **Dynamic Loading**: Morphospaces loaded on-demand using `importlib`

**Use Cases:**

- Generate 3D specimens from morphological measurements
- Create synthetic specimen libraries for computer vision training
- Visualize theoretical morphospaces
- Compare specimens across morphological parameter space

---

## Architecture

### Component Overview

```
Morphospace System
├── Discovery (list_morphospaces)
│   └── Scans assets/morphospace_modules/ for valid modules
│
├── Module Structure
│   ├── __init__.py (contains sample() function)
│   └── morphospace/ (mathematical model + Blender conversion)
│
├── Loading (generate_morphospace_sample_op)
│   ├── importlib dynamic loading
│   ├── Extract sample() function
│   └── Inspect function signature
│
├── Parameter Mapping
│   ├── Get dataset row for selected sample
│   ├── Convert column names (lowercase, spaces→underscores)
│   └── Map to function parameters
│
└── Geometry Generation
    ├── Call sample() with parameters
    ├── Returns morphospace sample object
    └── Call to_blender() to create Blender mesh
```

### Data Flow

```
1. User selects morphospace
   setup.available_morphospaces = "Shell (Default)"
   ↓
2. User selects dataset sample
   dataset.sample = "SpeciesName"
   ↓
3. User triggers generation
   bpy.ops.traitblender.generate_morphospace_sample()
   ↓
4. Operator loads morphospace module
   importlib → get sample() function
   ↓
5. Get dataset row
   row_data = dataset.loc(sample_name)
   ↓
6. Map parameters
   Column names → function parameter names
   {"Growth Rate": 0.5} → {"growth_rate": 0.5}
   ↓
7. Call sample() function
   sample_obj = sample(name="SpeciesName", growth_rate=0.5, ...)
   ↓
8. Generate Blender geometry
   sample_obj.to_blender()
   ↓
9. Position on table
   obj.tb_location = (0, 0, 0)
   obj.tb_rotation = (0, 0, 0)
```

---

## Morphospace Module Structure

### Required Directory Structure

```
assets/morphospace_modules/
└── MyMorphospace/                    # Module name (folder)
    ├── __init__.py                   # Required: Contains sample() function
    └── morphospace/                  # Mathematical model + Blender conversion
        ├── __init__.py
        ├── my_morphospace.py        # Model implementation
        └── my_morphospace_sample.py  # Sample class with to_blender()
```

**Minimum requirement:** `__init__.py` with `sample()` function

**Recommended structure:** Separate model and conversion logic for maintainability

### The `__init__.py` File

Must contain a `sample()` function as the entry point:

```python
# assets/morphospace_modules/MyMorphospace/__init__.py

from .morphospace import MyMorphospace_MORPHOSPACE, MyMorphospace_MORPHOSPACE_SAMPLE

def sample(name="Specimen", param1=1.0, param2=2.0, param3=0.5):
    """
    Generate a specimen from the morphospace.
    
    Args:
        name (str): Name for the generated specimen
        param1 (float): Description of param1
        param2 (float): Description of param2
        param3 (float): Description of param3
    
    Returns:
        MyMorphospace_MORPHOSPACE_SAMPLE: Sample object with to_blender() method
    """
    morphospace = MyMorphospace_MORPHOSPACE()
    return morphospace.generate_sample(
        name=name,
        param1=param1,
        param2=param2,
        param3=param3
    )

__all__ = ['sample']
```

**Key requirements:**

- ✅ Function named `sample`
- ✅ First parameter named `name` (receives species/specimen name)
- ✅ Default values for all parameters (morphospace can be called with no dataset)
- ✅ Returns object with `to_blender()` method
- ✅ Docstring explaining parameters

### Required: `ORIENTATIONS` Dictionary

Morphospaces **must** export an `ORIENTATIONS` dict with at least a callable `"Default"` entry. Morphospaces without it are not listed. Each function receives `(sample_obj)` and modifies the object in place (e.g., rotating so the specimen faces the camera).

```python
def _orient_default(sample_obj):
    """Center on table, rotate so aperture face is orthogonal to table Y axis."""
    sample_obj.tb_location = (0.0, 0.0, 0.0)
    # ... compute aperture plane from vertex group, rotate to align ...

ORIENTATIONS = {
    "Default": _orient_default,
}
```

These appear in the Orientations panel dropdown and are applied automatically in the Imaging Pipeline.

---

## The `sample()` Function Interface

### Function Signature

```python
def sample(name: str = "Specimen", **params) -> MorphospaceSampleObject:
    """Generate specimen from morphospace parameters."""
    pass
```

**Requirements:**

1. **First parameter must be `name`**
   - Receives species/specimen identifier from dataset
   - Used to name the generated Blender object

2. **All parameters must have defaults**
   - Enables testing without dataset
   - Provides fallback values

3. **Parameter names must match dataset columns** (after conversion)
   - Dataset: "Growth Rate" → `growth_rate`
   - Dataset: "aperture_size" → `aperture_size`
   - Dataset: "D Parameter" → `d_parameter`

4. **Return object with `to_blender()` method**
   - Must create Blender geometry when called
   - Object becomes available as `bpy.data.objects[name]`

### Example: Simple Morphospace

```python
def sample(name="Shape", radius=1.0, height=2.0, segments=32):
    """
    Generate a simple cylinder morphospace specimen.
    
    Args:
        name: Specimen name
        radius: Cylinder radius
        height: Cylinder height
        segments: Number of segments
    
    Returns:
        SimpleSample object
    """
    return SimpleSample(name, radius, height, segments)
```

### Example: Complex Morphospace (Shell Default)

```python
def sample(name="Shell", b=0.1, d=4, z=0, a=1, phi=0, psi=0,
           c_depth=0, c_n=0, n_depth=0, n=0, t=10, time_step=1/30,
           points_in_circle=40, eps=0.8, h_0=0.1, length=0.015):
    """
    Generate shell using Shell morphospace.
    
    Args:
        name: Specimen name
        b: Growth rate
        d: Distance from axis
        z: Vertical translation
        a: Aperture shape parameter
        phi, psi: Rotation angles
        c_depth, c_n: Axial rib parameters
        n_depth, n: Spiral rib parameters
        t: Shell length (time parameter)
        time_step: Time discretization
        points_in_circle: Aperture resolution
        eps, h_0: Thickness parameters
        length: Final shell length in meters
    
    Returns:
        ShellMorphospaceSample object
    """
    morphospace = ShellMorphospace()
    return morphospace.generate_sample(
        name=name, b=b, d=d, z=z, a=a, phi=phi, psi=psi,
        c_depth=c_depth, c_n=c_n, n_depth=n_depth, n=n, 
        t=t, time_step=time_step, points_in_circle=points_in_circle,
        eps=eps, h_0=h_0, length=length
    )
```

---

## The Morphospace Sample Class

### Required Method: `to_blender()`

Sample objects must implement `to_blender()` to create Blender geometry:

```python
class MyMorphospaceSample:
    def __init__(self, name, data):
        self.name = name
        self.data = data  # Vertex/face data or other geometry info
    
    def to_blender(self):
        """
        Create Blender mesh object from morphospace data.
        
        Must:
        - Create mesh with bpy.data.meshes.new()
        - Create object with bpy.data.objects.new()
        - Link to scene collection
        - Set object name to self.name
        - Update scene
        """
        # Create mesh
        mesh = bpy.data.meshes.new(name=self.name)
        
        # Generate geometry (vertices, edges, faces)
        vertices = self._calculate_vertices()
        faces = self._calculate_faces()
        
        # Build mesh
        mesh.from_pydata(vertices, [], faces)
        mesh.update()
        
        # Create object
        obj = bpy.data.objects.new(self.name, mesh)
        
        # Link to scene
        bpy.context.collection.objects.link(obj)
        
        # Optional: Set origin, smooth shading, etc.
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME')
        bpy.ops.object.shade_smooth()
        
        # Update scene
        bpy.context.view_layer.update()
```

**Requirements:**

- ✅ Create mesh data structure
- ✅ Create Blender object with `self.name`
- ✅ Link to scene collection
- ✅ Update view layer
- ⚠️ Don't raise exceptions (handle errors gracefully)

### Example: Simple Cylinder

```python
class SimpleCylinderSample:
    def __init__(self, name, radius, height, segments):
        self.name = name
        self.radius = radius
        self.height = height
        self.segments = segments
    
    def to_blender(self):
        # Use Blender's primitive creation
        bpy.ops.mesh.primitive_cylinder_add(
            radius=self.radius,
            depth=self.height,
            vertices=self.segments,
            location=(0, 0, 0)
        )
        
        # Rename to specimen name
        obj = bpy.context.active_object
        obj.name = self.name
        
        # Update scene
        bpy.context.view_layer.update()
```

### Example: Complex Mesh (Shell Default)

The Shell (Default) morphospace generates shells with inner/outer surfaces and aperture:

```python
class ShellMorphospaceSample:
    def __init__(self, name, data):
        self.name = name
        self.data = data  # Contains: outer_surface, inner_surface, aperture
    
    def to_blender(self):
        # Create outer surface mesh
        outer_mesh = self._create_surface_mesh("outer_surface", self.data["outer_surface"])
        outer_obj = bpy.data.objects.new("outer_surface", outer_mesh)
        bpy.context.collection.objects.link(outer_obj)
        
        # Create inner surface mesh
        inner_mesh = self._create_surface_mesh("inner_surface", self.data["inner_surface"])
        inner_obj = bpy.data.objects.new("inner_surface", inner_mesh)
        bpy.context.collection.objects.link(inner_obj)
        
        # Create aperture mesh
        aperture_mesh = self._create_aperture_mesh(self.data["aperture"])
        aperture_obj = bpy.data.objects.new(f"{self.name}_aperture", aperture_mesh)
        bpy.context.collection.objects.link(aperture_obj)
        
        # Join all parts
        bpy.ops.object.select_all(action='DESELECT')
        outer_obj.select_set(True)
        inner_obj.select_set(True)
        aperture_obj.select_set(True)
        bpy.context.view_layer.objects.active = outer_obj
        bpy.ops.object.join()
        
        # Rename to specimen name
        final_obj = bpy.context.active_object
        final_obj.name = self.name
        
        # Set origin and smooth shading
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME')
        bpy.ops.object.shade_smooth()
        
        bpy.context.view_layer.update()
```

---

## Discovery and Loading

### Discovery: `list_morphospaces()`

Scans `assets/morphospace_modules/` for valid modules in `core/morphospaces/list_morphospaces.py`:

```python
def list_morphospaces():
    """
    List all available morphospaces by scanning the directory.
    
    Returns:
        list: Sorted list of morphospace names (folder names)
    """
    morphospace_modules_path = get_asset_path("morphospace_modules")
    
    if not os.path.exists(morphospace_modules_path):
        return []
    
    morphospaces = []
    try:
        for item in os.listdir(morphospace_modules_path):
            item_path = os.path.join(morphospace_modules_path, item)
            # Check if it's a directory with __init__.py
            if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, "__init__.py")):
                morphospaces.append(item)
    except Exception as e:
        print(f"Error listing morphospaces: {e}")
        return []
    
    return sorted(morphospaces)
```

**Discovery criteria:**
- ✅ Directory in `assets/morphospace_modules/`
- ✅ Contains `__init__.py` file
- ❌ Hidden directories (starting with `.` or `_`)

### Loading: Dynamic Import

Morphospace modules are loaded on-demand in `ui/operators/generate_morphospace_sample_op.py`:

```python
# Get morphospace name from UI
morphospace_name = setup.available_morphospaces

# Build path to module
morphospace_modules_path = get_asset_path("morphospace_modules")
morphospace_path = os.path.join(morphospace_modules_path, morphospace_name)

# Create module spec
spec = importlib.util.spec_from_file_location(
    morphospace_name,
    os.path.join(morphospace_path, "__init__.py"),
    submodule_search_locations=[morphospace_path]
)

# Load module
morphospace_module = importlib.util.module_from_spec(spec)
sys.modules[morphospace_name] = morphospace_module
spec.loader.exec_module(morphospace_module)

# Extract sample function
sample_func = getattr(morphospace_module, 'sample')
```

**Error handling:**
```python
try:
    sample_func = getattr(morphospace_module, 'sample')
except AttributeError:
    self.report({'ERROR'}, f"Morphospace '{morphospace_name}' has no 'sample' function")
    return {'CANCELLED'}
```

---

## Parameter Mapping

### Column Name Conversion

Dataset column names are converted to match Python parameter naming:

```python
# Conversion rules:
1. Lowercase
2. Spaces → underscores

# Examples:
"Growth Rate"     → "growth_rate"
"D Parameter"     → "d_parameter"
"aperture_size"   → "aperture_size"  (no change)
"SHELL LENGTH"    → "shell_length"
"phi"             → "phi"             (no change)
```

### Mapping Process

```python
# 1. Get function signature
sig = inspect.signature(sample_func)
valid_params = set(sig.parameters.keys()) - {'name'}

# 2. Get dataset row
selected_sample_name = dataset.sample
row_data = dataset.loc(selected_sample_name)

# 3. Map parameters
params = {}
for column_name, value in row_data.items():
    # Convert column name
    param_name = column_name.lower().replace(' ', '_')
    
    # Check if parameter exists in function
    if param_name in valid_params:
        params[param_name] = value

# 4. Call function
sample_obj = sample_func(name=selected_sample_name, **params)
```

### Handling Missing Parameters

**Function has parameter not in dataset:**
```python
def sample(name="Shell", param1=1.0, param2=2.0):
    pass

# Dataset only has: ["species", "param1"]
# Missing: param2

# Result: Uses default value from function signature
sample(name="Species1", param1=0.5)  # param2=2.0 (default)
```

**Dataset has column not in function:**
```python
def sample(name="Shell", param1=1.0):
    pass

# Dataset has: ["species", "param1", "param2", "extra_column"]
# Extra: param2, extra_column

# Result: Extra columns ignored
sample(name="Species1", param1=0.5)  # param2 and extra_column ignored
```

---

## Creating a New Morphospace

### Step-by-Step Guide

**1. Create module directory:**

```bash
cd assets/morphospace_modules/
mkdir MyMorphospace
cd MyMorphospace
```

**2. Create `__init__.py` with `sample()` function:**

```python
# assets/morphospace_modules/MyMorphospace/__init__.py

def sample(name="Specimen", length=1.0, width=1.0, height=1.0):
    """
    Generate a box specimen.
    
    Args:
        name: Specimen identifier
        length: Box length
        width: Box width  
        height: Box height
    
    Returns:
        BoxSample object with to_blender() method
    """
    return BoxSample(name, length, width, height)


class BoxSample:
    """Simple box morphospace sample."""
    
    def __init__(self, name, length, width, height):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
    
    def to_blender(self):
        """Create box mesh in Blender."""
        import bpy
        
        # Create box
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            location=(0, 0, 0)
        )
        
        # Scale to dimensions
        obj = bpy.context.active_object
        obj.scale = (self.length, self.width, self.height)
        
        # Apply scale
        bpy.ops.object.transform_apply(scale=True)
        
        # Rename
        obj.name = self.name
        
        # Update scene
        bpy.context.view_layer.update()


__all__ = ['sample']
```

**3. Test in Blender:**

```python
# In Blender console
from assets.morphospace_modules.MyMorphospace import sample

# Test without dataset
sample_obj = sample(name="TestBox", length=2.0, width=1.0, height=0.5)
sample_obj.to_blender()

# Should create a box named "TestBox" in the scene
```

**4. Create test dataset:**

```csv
species,length,width,height
Box1,1.0,1.0,1.0
Box2,2.0,1.5,0.8
Box3,0.5,0.5,2.0
```

**5. Use in TraitBlender:**

```python
# Load museum scene
bpy.ops.traitblender.setup_scene()

# Import dataset
dataset = bpy.context.scene.traitblender_dataset
dataset.filepath = "/path/to/boxes.csv"

# Select morphospace (should appear in dropdown)
setup = bpy.context.scene.traitblender_setup
setup.available_morphospaces = "MyMorphospace"

# Generate specimen
dataset.sample = "Box1"
bpy.ops.traitblender.generate_morphospace_sample()

# Should create box with dimensions from dataset
```

### Recommended Structure (Advanced)

For complex morphospaces, separate concerns:

```
MyMorphospace/
├── __init__.py                   # Entry point with sample()
└── morphospace/
    ├── __init__.py               # Exports MORPHOSPACE and MORPHOSPACE_SAMPLE
    ├── my_morphospace.py         # Mathematical model
    └── my_morphospace_sample.py  # Blender conversion
```

**`__init__.py`:**
```python
from .morphospace import MyMORPHOSPACE, MyMORPHOSPACE_SAMPLE

def sample(name="Specimen", **params):
    morphospace = MyMORPHOSPACE()
    return morphospace.generate_sample(name=name, **params)

__all__ = ['sample']
```

**`morphospace/my_morphospace.py`:**
```python
class MyMORPHOSPACE:
    """Mathematical morphospace model."""
    
    def __init__(self):
        pass
    
    def generate_sample(self, name, param1, param2, ...):
        """
        Generate specimen data from parameters.
        
        Returns:
            MyMORPHOSPACE_SAMPLE object
        """
        # Calculate geometry data
        data = self._calculate_geometry(param1, param2, ...)
        
        return MyMORPHOSPACE_SAMPLE(name=name, data=data)
    
    def _calculate_geometry(self, param1, param2, ...):
        """Mathematical model implementation."""
        # Complex calculations here
        return geometry_data
```

**`morphospace/my_morphospace_sample.py`:**
```python
import bpy

class MyMORPHOSPACE_SAMPLE:
    """Blender conversion for morphospace samples."""
    
    def __init__(self, name, data):
        self.name = name
        self.data = data
    
    def to_blender(self):
        """Create Blender mesh from geometry data."""
        # Convert self.data to Blender mesh
        pass
```

