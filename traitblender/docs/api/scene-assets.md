# Scene Assets API Reference

The positioning system provides a custom coordinate system relative to the museum table for consistent object placement.

## Table Coordinates System

TraitBlender uses a custom coordinate system (`tb_coords`) that positions objects relative to the table's top surface center. This ensures consistent placement regardless of table orientation or position.

### Table Coordinates Property

All Blender objects have a `tb_coords` property that provides table-relative positioning:

```python
# Get an object
obj = bpy.data.objects["MyObject"]

# Position relative to table center
obj.tb_coords = (0.0, 0.0, 0.0)  # Center of table
obj.tb_coords = (0.5, 0.0, 0.0)  # 0.5 units along table's X axis
obj.tb_coords = (0.0, 0.5, 0.1)  # Offset in X, Y, and Z

# Get current table coordinates
current_pos = obj.tb_coords
print(f"Table coordinates: {current_pos}")
```

### Table Rotation Property

Objects also have a `tb_rotation` property for table-relative rotation:

```python
# Rotate relative to table orientation
obj.tb_rotation = (0.0, 0.0, 0.0)  # Aligned with table
obj.tb_rotation = (0.0, 0.0, 1.57)  # 90 degrees around table's Z axis
```

## Coordinate Conversion Functions

### world_to_table_coords

Convert a world-space point to table coordinates.

```python
from core.positioning import world_to_table_coords
from mathutils import Vector

# Convert world position to table coordinates
world_point = Vector((1.0, 2.0, 3.0))
table_coords = world_to_table_coords(world_point)
print(f"Table coordinates: {table_coords}")
```

**Parameters:**
- `world_point` (Vector): World-space position
- `precision` (int, optional): Decimal places for rounding (default: 4)

**Returns:**
- `tuple[float, float, float]`: Table coordinates (x, y, z)

### get_table_top_center

Get the world-space center of the table's top face.

```python
from core.positioning import get_table_top_center

center = get_table_top_center()
print(f"Table center: {center}")
```

**Returns:**
- `Vector`: World-space position of table top center

### z_dist_to_lowest

Calculate the distance from an object's origin to its lowest vertex.

```python
from core.positioning import z_dist_to_lowest

obj = bpy.data.objects["MyObject"]
distance = z_dist_to_lowest(obj)
print(f"Distance to lowest point: {distance}")
```

**Parameters:**
- `obj` (bpy.types.Object): Blender object

**Returns:**
- `float`: Distance from origin to lowest vertex (0 for non-mesh objects)

## Usage Examples

### Positioning Specimens on Table

```python
import bpy

# Generate a specimen (from morphospace)
bpy.ops.traitblender.generate_morphospace_sample()

# Get the generated object
specimen = bpy.data.objects["species_name"]

# Position at table center
specimen.tb_coords = (0.0, 0.0, 0.0)

# Move to different position
specimen.tb_coords = (0.3, 0.0, 0.0)  # 0.3 units along table X axis
```

### Converting Between Coordinate Systems

```python
from core.positioning import world_to_table_coords, get_table_top_center
from mathutils import Vector

# Get table center in world space
table_center = get_table_top_center()

# Convert world position to table coordinates
world_pos = Vector((1.5, 2.0, 0.5))
table_pos = world_to_table_coords(world_pos)

# Use table coordinates to position object
obj = bpy.data.objects["MyObject"]
obj.tb_coords = table_pos
```

### Working with Multiple Objects

```python
# Position multiple specimens on table
specimens = ["specimen1", "specimen2", "specimen3"]
positions = [
    (-0.3, 0.0, 0.0),  # Left
    (0.0, 0.0, 0.0),   # Center
    (0.3, 0.0, 0.0),   # Right
]

for name, pos in zip(specimens, positions):
    if name in bpy.data.objects:
        obj = bpy.data.objects[name]
        obj.tb_coords = pos
```

## How Table Coordinates Work

The table coordinate system:

1. **Origin**: Center of the table's top face
2. **Axes**: Aligned with the table's local coordinate system
3. **Z-axis**: Normal to the table surface (upward)
4. **Automatic lift**: Accounts for object's lowest vertex to place on table surface

When you set `obj.tb_coords = (x, y, z)`:
- `x, y`: Position along table surface
- `z`: Height above/below table surface
- The object is automatically lifted so its bottom touches the table

## Integration with Morphospace Generation

When you generate a morphospace sample, it's automatically positioned using table coordinates:

```python
# Generate sample
bpy.ops.traitblender.generate_morphospace_sample()

# The specimen is automatically set to table center
specimen = bpy.data.objects[dataset.sample]
print(f"Initial position: {specimen.tb_coords}")  # (0.0, 0.0, 0.0)

# Adjust position
specimen.tb_coords = (0.2, 0.0, 0.0)  # Move along table X axis
```

## Best Practices

1. **Always use table coordinates** for positioning specimens - ensures consistency
2. **Use world coordinates** only when necessary for calculations
3. **Account for object geometry** - the system automatically handles bottom alignment
4. **Test positioning** before batch processing to ensure correct placement

## Error Handling

The table coordinate system requires the "Table" object to exist in the scene:

```python
try:
    obj.tb_coords = (0.0, 0.0, 0.0)
except RuntimeError as e:
    print(f"Error: Table object not found. Run bpy.ops.traitblender.setup_scene() first")
```

Always ensure the museum scene is loaded before using table coordinates.
