# Positioning System

---

## Overview

The Positioning System provides a table-centric coordinate system for precise specimen placement in museum-style scenes. Instead of working with world coordinates, specimens are positioned relative to a virtual table surface, with specialized origin calculations for morphological consistency.

**Key Features:**

- **Table Coordinates (`tb_location`)**: Position objects relative to table surface (0,0,0 = table center)
- **Table Rotation (`tb_rotation`)**: Rotate objects around their bottom-center pivot point
- **Custom Origins (`PLACEMENT_LOCAL_ORIGINS_TB`)**: Four origin calculation methods for morphological consistency
- **Automatic Z-Calculation**: Objects automatically placed on table surface
- **Coordinate Transformations**: Seamless conversion between world and table space

**Use Cases:**

- Position specimens consistently on museum table
- Rotate specimens around natural pivot points (base, not center)
- Compare specimens with aligned origins (geometric bounds, mean position, etc.)
- Apply transforms in table space, render in world space

---

## Architecture

### Component Overview

```
Positioning System
├── Table Coordinates (tb_location)
│   ├── Custom FloatVectorProperty (3D vector)
│   ├── Getter: world → table space
│   ├── Setter: table → world space
│   └── Auto Z-positioning on table
│
├── Table Rotation (tb_rotation)
│   ├── Custom FloatVectorProperty (Euler angles)
│   ├── Rotates around bottom-center pivot
│   ├── Getter/Setter with pivot transform
│   └── Preserves table position
│
├── Origin Calculations (PLACEMENT_LOCAL_ORIGINS_TB)
│   ├── OBJECT: Blender object origin
│   ├── GEOM_BOUNDS: Geometric bounding box center
│   ├── MEAN: Mean vertex position
│   └── MEDIAN: Median vertex position
│
└── Coordinate Utilities
    ├── get_table_top_center(): Find table center in world space
    ├── z_dist_to_lowest(): Distance from origin to lowest point
    └── world_to_tb_location(): Coordinate transformation
```

### Data Flow

```
1. User positions specimen in table space
   obj.tb_location = (0.5, 0.5, 0)  # X, Y, Z in table space
   ↓
2. Setter converts to world space
   table_center = get_table_top_center()
   world_pos = table_center + tb_location
   ↓
3. Auto-calculate Z (on table surface)
   z_offset = z_dist_to_lowest(obj, origin_type)
   world_pos.z += z_offset
   ↓
4. Apply to object
   obj.location = world_pos
   ↓
5. Getter converts back to table space (for display)
   tb_location = world_to_tb_location(obj.location)
```

---

## Table Coordinates (`tb_location`)

### Overview

`tb_location` is a custom `FloatVectorProperty` registered on `bpy.types.Object` that provides a table-centric coordinate system. Objects are positioned relative to the table surface rather than world origin.

**Convention:**
- **(0, 0, 0)**: Center of table surface
- **X-axis**: Left (-) to Right (+)
- **Y-axis**: Front (-) to Back (+)
- **Z-axis**: Below table (-) to Above table (+), but typically 0 (on table surface)

### Registration

Defined in `ui/properties/tb_location.py`:

```python
bpy.types.Object.tb_location = FloatVectorProperty(
    name="Table Coordinates",
    description="Position relative to table center (X, Y, Z in table space)",
    size=3,
    default=(0.0, 0.0, 0.0),
    subtype='TRANSLATION',
    unit='LENGTH',
    get=_get_tb_location,
    set=_set_tb_location
)
```

**Key attributes:**
- `size=3`: 3D vector (X, Y, Z)
- `subtype='TRANSLATION'`: UI displays as position
- `unit='LENGTH'`: Uses scene units (meters)
- `get/set`: Custom getters/setters for coordinate transformation

### The Getter: `get_tb_location()`

Converts object's world position to table space for display:

```python
def get_tb_location(self):
    """
    Convert object's world position to table coordinates.
    
    Returns:
        tuple: (x, y, z) in table space
    """
    try:
        # Get table center in world space
        table_center = get_table_top_center()
        
        # Convert world position to table-relative
        world_pos = self.location
        tb_x = world_pos.x - table_center.x
        tb_y = world_pos.y - table_center.y
        tb_z = world_pos.z - table_center.z
        
        return (tb_x, tb_y, tb_z)
    
    except Exception as e:
        warnings.warn(f"Error getting table coords: {e}")
        return (0.0, 0.0, 0.0)
```

**What it does:**
1. Find table center in world space
2. Subtract table center from object's world position
3. Return table-relative position

**When it's called:**
- When UI displays `tb_location` property
- When reading `obj.tb_location` in Python
- After object is moved (for UI update)

### The Setter: `set_tb_location()`

Converts table coordinates to world position and places object on table:

```python
def _set_tb_location(self, value):
    """
    Set object position from table coordinates.
    
    Args:
        value (tuple): (x, y, z) in table space
    """
    try:
        # Get table center in world space
        table_center = get_table_top_center()
        
        # Convert table coords to world space
        world_x = table_center.x + value[0]
        world_y = table_center.y + value[1]
        
        # Get orientation config for origin type
        config = bpy.context.scene.traitblender_config
        origin_type = config.orientations.object_location_origin
        
        # Calculate Z offset to place object on table
        z_offset = z_dist_to_lowest(self, origin_type)
        world_z = table_center.z + value[2] + z_offset
        
        # Apply world position
        self.location = (world_x, world_y, world_z)
    
    except Exception as e:
        warnings.warn(f"Error setting table coords: {e}")
```

**What it does:**
1. Get table center in world space
2. Add table coords to table center (X, Y)
3. Get origin type from config
4. Calculate Z offset using `z_dist_to_lowest()`
5. Set object's world position

**When it's called:**
- When user changes `tb_location` in UI
- When setting `obj.tb_location = (x, y, z)` in Python
- During specimen generation (initial placement)

### Z-Offset Calculation

The Z-offset ensures objects sit **on** the table, not intersecting it:

```python
# Without Z-offset:
obj.location.z = table_center.z + 0
# Result: Object center at table surface → half below table ✗

# With Z-offset:
z_offset = z_dist_to_lowest(obj, origin_type)
obj.location.z = table_center.z + 0 + z_offset
# Result: Object's bottom at table surface ✓
```

**Example:**
```python
# Object with height 2.0, origin at center
z_dist_to_lowest(obj, "OBJECT") → 1.0
# Object placed 1.0 units above table surface
# → Bottom edge at table.z, top edge at table.z + 2.0
```

---

## Table Rotation (`tb_rotation`)

### Overview

`tb_rotation` is a custom `FloatVectorProperty` that rotates objects around their **bottom-center** pivot point, not their object origin. This provides natural rotation for specimens (like spinning a shell on a table).

**Pivot Point:**
- **X/Y**: Object origin (center)
- **Z**: Lowest point of object (bottom)
- **Result**: Rotates around base, like a spinning top

### Registration

Defined in `ui/properties/table_rotations.py`:

```python
bpy.types.Object.tb_rotation = FloatVectorProperty(
    name="Table Rotation",
    description="Rotation around bottom-center pivot (Euler angles in radians)",
    size=3,
    default=(0.0, 0.0, 0.0),
    subtype='EULER',
    unit='ROTATION',
    get=get_tb_rotation,
    set=set_tb_rotation
)
```

**Key attributes:**
- `subtype='EULER'`: Euler angle rotation (XYZ)
- `unit='ROTATION'`: Radians (UI converts to degrees)
- `get/set`: Custom pivot-point handling

### The Getter: `get_tb_rotation()`

Returns current rotation (stored in custom property):

```python
def get_tb_rotation(self):
    """
    Get stored table rotation.
    
    Returns:
        tuple: (rx, ry, rz) Euler angles in radians
    """
    # Rotation stored in custom property to preserve it
    if "_tb_rotation" in self:
        return tuple(self["_tb_rotation"])
    else:
        return (0.0, 0.0, 0.0)
```

**Why custom property storage?**
- Object's actual `rotation_euler` is in world space
- We need to track rotation in table space separately
- Custom property preserves rotation across transforms

### The Setter: `set_tb_rotation()`

Rotates object around bottom-center pivot:

```python
def set_tb_rotation(self, value):
    """
    Rotate object around bottom-center pivot.
    
    Args:
        value (tuple): (rx, ry, rz) Euler angles in radians
    """
    import mathutils
    
    # Store rotation in custom property
    self["_tb_rotation"] = value
    
    # Get bottom-center pivot point
    pivot = self._get_bottom_center_pivot()
    
    # Convert Euler angles to rotation matrix
    rotation_matrix = mathutils.Euler(value, 'XYZ').to_matrix().to_4x4()
    
    # Create transformation matrix:
    # 1. Translate to origin (move pivot to world origin)
    to_origin = mathutils.Matrix.Translation(-pivot)
    
    # 2. Rotate
    # (rotation_matrix already created)
    
    # 3. Translate back (move pivot back to original position)
    from_origin = mathutils.Matrix.Translation(pivot)
    
    # Combine: from_origin @ rotation_matrix @ to_origin
    transform = from_origin @ rotation_matrix @ to_origin
    
    # Apply to object's matrix_world
    self.matrix_world = transform @ self.matrix_world
```

**What it does:**
1. Store rotation value in custom property
2. Calculate bottom-center pivot point
3. Create transformation matrix:
   - Translate pivot to world origin
   - Apply rotation
   - Translate pivot back
4. Apply transformation to object

**Transform Matrix Math:**
```
Final Transform = T(pivot) × R(angles) × T(-pivot)

Where:
  T(pivot)   = Translation matrix to move pivot back
  R(angles)  = Rotation matrix from Euler angles
  T(-pivot)  = Translation matrix to move pivot to origin
```

### Bottom-Center Pivot Calculation

```python
def _get_bottom_center_pivot(self):
    """
    Calculate bottom-center point of object.
    
    Returns:
        Vector: (x, y, z) of pivot in world space
    """
    import mathutils
    
    # Get object's origin (center in X/Y)
    pivot_x = self.location.x
    pivot_y = self.location.y
    
    # Get orientation config for origin type
    config = bpy.context.scene.traitblender_config
    origin_type = config.orientations.object_location_origin
    
    # Calculate Z distance to lowest point
    z_offset = z_dist_to_lowest(self, origin_type)
    
    # Bottom is current Z minus the offset
    pivot_z = self.location.z - z_offset
    
    return mathutils.Vector((pivot_x, pivot_y, pivot_z))
```

**Example:**
```python
# Object at (1, 2, 5), height 2.0, origin at center
pivot = _get_bottom_center_pivot()
# Returns (1, 2, 4)  ← X/Y from origin, Z at bottom

# Rotate 90° around Z-axis
obj.tb_rotation = (0, 0, math.radians(90))
# Object spins around point (1, 2, 4)
# Like a shell spinning on a table
```

---

## Origin Calculations

### Overview

The Positioning System supports four origin types for morphological consistency. Different origin types affect how specimens are aligned and compared.

**Dictionary:** `PLACEMENT_LOCAL_ORIGINS_TB` in `core/positioning/origins.py`

```python
PLACEMENT_LOCAL_ORIGINS_TB = {
    "OBJECT": _get_object_origin,
    "GEOM_BOUNDS": _get_geometry_bounds_origin,
    "MEAN": _get_mean_origin,
    "MEDIAN": _get_median_origin
}
```

**Configuration:**
```python
config = bpy.context.scene.traitblender_config
config.orientations.object_location_origin = "GEOM_BOUNDS"
```

### Origin Type: `OBJECT`

Uses Blender's object origin (the orange dot in viewport).

```python
def _get_object_origin(obj):
    """
    Get object's Blender origin.
    
    Returns:
        Vector: (0, 0, 0) in object local space
    """
    return mathutils.Vector((0.0, 0.0, 0.0))
```

**When to use:**
- Object origins already set correctly
- Custom origin placement (e.g., biological landmark)
- Simple objects with centered origins

**Characteristics:**
- Fast (no calculation)
- Depends on how object was created
- May not align morphologically similar specimens

**Example:**
```python
# Cylinder created with primitive_cylinder_add()
# Origin at geometric center
_get_object_origin() → (0, 0, 0) in local space
```

### Origin Type: `GEOM_BOUNDS`

Uses center of axis-aligned bounding box.

```python
def _get_geometry_bounds_origin(obj):
    """
    Calculate bounding box center.
    
    Returns:
        Vector: (x, y, z) center of bounding box in object local space
    """
    # Get bounding box corners (8 points)
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    
    # Find min/max in each axis
    min_x = min(corner.x for corner in bbox_corners)
    max_x = max(corner.x for corner in bbox_corners)
    min_y = min(corner.y for corner in bbox_corners)
    max_y = max(corner.y for corner in bbox_corners)
    min_z = min(corner.z for corner in bbox_corners)
    max_z = max(corner.z for corner in bbox_corners)
    
    # Calculate center
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    center_z = (min_z + max_z) / 2
    
    # Convert to object local space
    world_center = mathutils.Vector((center_x, center_y, center_z))
    local_center = obj.matrix_world.inverted() @ world_center
    
    return local_center
```

**When to use:**
- Simple convex shapes
- Quick alignment without vertex access
- Bounding box represents object well

**Characteristics:**
- Fast (only 8 corners)
- Axis-aligned (ignores rotation)
- Can be misleading for complex/concave shapes

**Example:**
```python
# L-shaped object:
#   ██
#   ██████
# Bounding box: rectangle enclosing entire shape
# Center: middle of rectangle (may be outside object) ✗
```

### Origin Type: `MEAN`

Uses arithmetic mean of all vertex positions (centroid).

```python
def _get_mean_origin(obj):
    """
    Calculate mean vertex position (centroid).
    
    Returns:
        Vector: (x, y, z) mean position in object local space
    """
    if obj.type != 'MESH':
        return _get_object_origin(obj)
    
    mesh = obj.data
    
    # Sum all vertex positions
    sum_x = sum_y = sum_z = 0.0
    num_verts = len(mesh.vertices)
    
    if num_verts == 0:
        return mathutils.Vector((0.0, 0.0, 0.0))
    
    for vert in mesh.vertices:
        sum_x += vert.co.x
        sum_y += vert.co.y
        sum_z += vert.co.z
    
    # Calculate mean
    mean_x = sum_x / num_verts
    mean_y = sum_y / num_verts
    mean_z = sum_z / num_verts
    
    return mathutils.Vector((mean_x, mean_y, mean_z))
```

**When to use:**
- Morphological consistency across specimens
- Objects with uniform vertex distribution
- Center-of-mass approximation (if uniform density)

**Characteristics:**
- Moderate speed (iterates all vertices)
- Robust for most shapes
- Sensitive to vertex density variation

**Example:**
```python
# Shell with 1000 vertices evenly distributed
# Mean = geometric centroid ✓

# Shell with dense apex (800 verts), sparse body (200 verts)
# Mean skewed toward apex ✗
```

### Origin Type: `MEDIAN`

Uses median vertex position in each axis.

```python
def _get_median_origin(obj):
    """
    Calculate median vertex position.
    
    Returns:
        Vector: (x, y, z) median position in object local space
    """
    if obj.type != 'MESH':
        return _get_object_origin(obj)
    
    mesh = obj.data
    num_verts = len(mesh.vertices)
    
    if num_verts == 0:
        return mathutils.Vector((0.0, 0.0, 0.0))
    
    # Collect vertex coordinates
    x_coords = [v.co.x for v in mesh.vertices]
    y_coords = [v.co.y for v in mesh.vertices]
    z_coords = [v.co.z for v in mesh.vertices]
    
    # Sort and find median
    x_coords.sort()
    y_coords.sort()
    z_coords.sort()
    
    # Median calculation
    mid = num_verts // 2
    if num_verts % 2 == 0:
        # Even number: average of two middle values
        median_x = (x_coords[mid - 1] + x_coords[mid]) / 2
        median_y = (y_coords[mid - 1] + y_coords[mid]) / 2
        median_z = (z_coords[mid - 1] + z_coords[mid]) / 2
    else:
        # Odd number: middle value
        median_x = x_coords[mid]
        median_y = y_coords[mid]
        median_z = z_coords[mid]
    
    return mathutils.Vector((median_x, median_y, median_z))
```

**When to use:**
- Non-uniform vertex distribution
- Outlier vertices (long appendages, spines)
- Robust center estimation

**Characteristics:**
- Slow (sorts all vertices)
- Resistant to outliers
- Independent in each axis

**Example:**
```python
# Shell with long spiny apex (few vertices far from body)
# Mean: Pulled toward apex
# Median: Center of main body mass ✓

# Vertices: [1, 2, 3, 100]
# Mean: 26.5 (pulled by outlier)
# Median: 2.5 (robust to outlier)
```

### Comparison Matrix

| Origin Type | Speed | Use Case | Pros | Cons |
|------------|-------|----------|------|------|
| `OBJECT` | ⚡⚡⚡ | Custom placement | Fast, predictable | Manual setup |
| `GEOM_BOUNDS` | ⚡⚡ | Simple shapes | Fast, no mesh access | Misleading for complex shapes |
| `MEAN` | ⚡ | Uniform density | Morphologically consistent | Slow, sensitive to density |
| `MEDIAN` | 🐌 | Non-uniform density | Outlier-resistant | Very slow, axis-independent |

**Recommendation:**
- **Default**: `MEAN` (best for most morphospaces)
- **Fast preview**: `GEOM_BOUNDS`
- **Publication**: `MEDIAN` (most robust)
- **Landmarks**: `OBJECT` (manual placement)

---

## Coordinate Transformation Utilities

### `get_table_top_center()`

Finds the center of the table surface in world space.

```python
def get_table_top_center():
    """
    Get world coordinates of table top center.
    
    Returns:
        Vector: (x, y, z) of table center in world space
        
    Raises:
        RuntimeError: If "Table" object not found in scene
    """
    import bpy
    import mathutils
    
    # Find table object
    table = bpy.data.objects.get("Table")
    if table is None:
        raise RuntimeError("Table object not found. Run setup_scene first.")
    
    # Get table's bounding box top center
    bbox = table.bound_box
    
    # Top face vertices (Z-max)
    top_verts = [v for v in bbox if v[2] == max(vert[2] for vert in bbox)]
    
    # Calculate center of top face
    center_local = mathutils.Vector((
        sum(v[0] for v in top_verts) / len(top_verts),
        sum(v[1] for v in top_verts) / len(top_verts),
        top_verts[0][2]  # Z-coordinate (all same)
    ))
    
    # Transform to world space
    center_world = table.matrix_world @ center_local
    
    return center_world
```

**Usage:**
```python
# Get table center
center = get_table_top_center()
print(f"Table at: {center}")

# Place object at table center
obj.location = center
obj.location.z += z_dist_to_lowest(obj, "MEAN")
```

### `world_to_tb_location()`

Converts world position to table coordinates.

```python
def world_to_tb_location(world_pos):
    """
    Convert world position to table coordinates.
    
    Args:
        world_pos (Vector): Position in world space
    
    Returns:
        Vector: Position in table space
    """
    table_center = get_table_top_center()
    
    return mathutils.Vector((
        world_pos.x - table_center.x,
        world_pos.y - table_center.y,
        world_pos.z - table_center.z
    ))
```

**Usage:**
```python
# Object in world space
obj.location = (10, 5, 3)

# Convert to table space
tb_location = world_to_tb_location(obj.location)
print(f"Table coords: {tb_location}")

# Can also use property
print(f"Same as: {obj.tb_location}")
```

### `z_dist_to_lowest()`

Calculates distance from object origin to lowest point.

```python
def z_dist_to_lowest(obj, origin_type="OBJECT"):
    """
    Calculate Z distance from origin to lowest vertex.
    
    Args:
        obj: Blender object
        origin_type: Origin calculation method
    
    Returns:
        float: Distance from origin to bottom (always positive)
    """
    if obj.type != 'MESH':
        return 0.0
    
    # Get origin function
    origin_func = PLACEMENT_LOCAL_ORIGINS_TB.get(origin_type, _get_object_origin)
    origin = origin_func(obj)
    
    # Find lowest vertex in local space
    mesh = obj.data
    if len(mesh.vertices) == 0:
        return 0.0
    
    lowest_z = min(v.co.z for v in mesh.vertices)
    
    # Distance from origin to lowest point
    distance = origin.z - lowest_z
    
    return distance
```

**Usage:**
```python
# Object with origin at center, height 2.0
z_offset = z_dist_to_lowest(obj, "OBJECT")
# Returns: 1.0 (half the height)

# Place on table
table_center = get_table_top_center()
obj.location.z = table_center.z + z_offset
# Object's bottom now at table surface
```

**Why it's needed:**
```python
# Without z_offset:
obj.location = table_center
# Result: Origin at table surface
#         Bottom half below table ✗

# With z_offset:
obj.location.z = table_center.z + z_dist_to_lowest(obj)
# Result: Bottom at table surface
#         Entire object above table ✓
```

