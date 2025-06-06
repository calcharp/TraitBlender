# Scene Assets API Reference

The Scene Assets module provides high-level interfaces for managing Blender objects with enhanced transformation capabilities, specifically designed for museum-style morphological visualizations.

## Overview

Scene Assets are the core building blocks of TraitBlender, providing object-oriented access to Blender objects with enhanced transform operations and origin management.

## Classes

### SceneAsset (Abstract Base Class)

Abstract base class for managing Blender objects with enhanced transformation capabilities.

```python
from traitblender.core.scene_assets import SceneAsset
```

#### Constructor

```python
def __init__(self, name: str)
```

**Parameters:**
- `name` (str): The name of the corresponding Blender object

#### Properties

##### object
```python
@property
def object(self) -> bpy.types.Object
```
Returns the Blender object with the same name as this asset.

**Raises:**
- `ValueError`: If no object with the specified name exists in the scene

##### location
```python
@property
def location(self) -> Vector

@location.setter
def location(self, value: Vector | tuple[float, float, float] | tuple[Vector | tuple[float, float, float], str])
```
Gets or sets the location of the object.

**Setter Parameters:**
- `value`: Can be:
  - `Vector` or `(x,y,z)` tuple (uses default origin_type="BOTTOM_CENTER")
  - `(Vector or (x,y,z) tuple, origin_type)` tuple to specify custom origin

**Example:**
```python
asset = GenericAsset("Suzanne")
asset.location = (0, 0, 5)  # Places at world origin + 5 units up
asset.location = ((1, 2, 3), "GEOMETRY_ORIGIN")  # Custom origin
```

##### rotation_euler
```python
@property
def rotation_euler(self) -> Euler

@rotation_euler.setter
def rotation_euler(self, value: Euler | tuple[float, float, float] | tuple[Euler | tuple[float, float, float], str])
```
Gets or sets the rotation of the object using Euler angles.

**Setter Parameters:**
- `value`: Can be:
  - `Euler` or `(x,y,z)` tuple (uses default origin_type="GEOMETRY_ORIGIN")
  - `(Euler or (x,y,z) tuple, origin_type)` tuple to specify custom origin

**Example:**
```python
import math
asset.rotation_euler = (0, 0, math.pi/4)  # 45 degrees around Z-axis
```

##### scale
```python
@property
def scale(self) -> Vector

@scale.setter
def scale(self, value: Vector | tuple[float, float, float] | tuple[Vector | tuple[float, float, float], str])
```
Gets or sets the scale of the object.

**Example:**
```python
asset.scale = (2, 2, 2)  # Doubles the size uniformly
```

##### dimensions
```python
@property
def dimensions(self) -> Vector

@dimensions.setter
def dimensions(self, value: Vector | tuple[float, float, float])
```
Gets or sets the dimensions (size) of the object.

#### Methods

##### origin_set
```python
def origin_set(self, type: str = "GEOMETRY_ORIGIN", center: str = "MEDIAN")
```
Set the object's origin with extended options beyond standard Blender functionality.

**Parameters:**
- `type` (str): Origin type. Options include:
  - `"GEOMETRY_ORIGIN"`: Use the geometry's origin (default)
  - `"BOTTOM_CENTER"`: Place at bottom center using actual mesh vertices
  - Standard Blender options: `"ORIGIN_GEOMETRY"`, `"ORIGIN_CURSOR"`, etc.
- `center` (str): Center type for Blender's origin_set (only used for standard Blender options)

---

### GenericAsset

A concrete implementation of SceneAsset that can be instantiated directly.

```python
from traitblender.core.scene_assets import GenericAsset

# Create an asset for an existing Blender object
asset = GenericAsset("Suzanne")
```

**Use Case:** General-purpose scene asset for any Blender object that needs enhanced transform capabilities.

---

### SurfaceAsset

A specialized SceneAsset that provides a surface interface for placing other objects. The surface is defined by the upper face of the object's bounding box with a -1 to 1 coordinate grid.

```python
from traitblender.core.scene_assets import SurfaceAsset

# Create a surface asset (typically for tables, platforms, etc.)
table = SurfaceAsset("Cube")
```

#### Additional Properties

##### surface
```python
@property
def surface(self) -> tuple[Vector, Vector, Vector, Vector]
```
Returns the four corners of the surface in world space, ordered as:
`[min_x,min_y, min_x,max_y, max_x,max_y, max_x,min_y]`

##### surface_normal
```python
@property
def surface_normal(self) -> Vector
```
Returns the normal vector of the surface in world space.

#### Additional Methods

##### surface_to_world
```python
def surface_to_world(self, coords: tuple[float, float]) -> Vector
```
Convert surface coordinates (-1 to 1) to world position.

**Parameters:**
- `coords` (tuple[float, float]): (x, y) coordinates in surface space, each from -1 to 1

**Returns:**
- `Vector`: World space position on the surface

**Raises:**
- `ValueError`: If coordinates are outside the -1 to 1 range

##### place
```python
def place(self, asset: SceneAsset, coords: tuple[float, float])
```
Place an asset on the surface at the given coordinates. The asset will be positioned with its bottom center at the specified point, rotated to align with the surface normal, and parented to this surface.

**Parameters:**
- `asset` (SceneAsset): The SceneAsset to place
- `coords` (tuple[float, float]): (x, y) coordinates in surface space, each from -1 to 1

## Usage Examples

### Basic Asset Manipulation
```python
from traitblender.core.scene_assets import GenericAsset
import math

# Create an asset for an existing object
specimen = GenericAsset("SpecimenMesh")

# Position and orient the specimen
specimen.location = (0, 0, 2)
specimen.rotation_euler = (0, 0, math.pi/6)  # 30 degrees
specimen.scale = (1.5, 1.5, 1.5)

# Set custom origin for precise placement
specimen.origin_set(type="BOTTOM_CENTER")
```

### Surface Placement
```python
from traitblender.core.scene_assets import SurfaceAsset, GenericAsset

# Create surface and objects
table = SurfaceAsset("TableMesh")
specimen1 = GenericAsset("Specimen1")
specimen2 = GenericAsset("Specimen2")

# Place specimens on the surface
table.place(specimen1, (-0.5, -0.5))  # Bottom-left quadrant
table.place(specimen2, (0.5, 0.5))    # Top-right quadrant

# Get surface properties
corners = table.surface
normal = table.surface_normal
world_pos = table.surface_to_world((0, 0))  # Center of surface
```

### Origin Management
```python
asset = GenericAsset("ComplexMesh")

# Different origin types for different use cases
asset.origin_set(type="BOTTOM_CENTER")     # For placing on surfaces
asset.origin_set(type="GEOMETRY_ORIGIN")   # For rotation around geometry center
asset.origin_set(type="ORIGIN_CURSOR")     # For manual cursor-based placement
```

## Error Handling

### Common Exceptions

- **ValueError**: Raised when:
  - Specified object name doesn't exist in the scene
  - Surface coordinates are outside the -1 to 1 range
  - Invalid parameter values are provided

### Best Practices

1. **Object Existence**: Always ensure the Blender object exists before creating a SceneAsset
2. **Origin Awareness**: Remember that transforms behave differently based on the current origin type
3. **Surface Coordinates**: Use the surface coordinate system (-1 to 1) for consistent placement
4. **Error Handling**: Wrap SceneAsset operations in try-catch blocks for robust code

```python
try:
    asset = GenericAsset("MyObject")
    asset.location = (0, 0, 5)
except ValueError as e:
    print(f"Error: {e}")
    # Handle missing object case
``` 