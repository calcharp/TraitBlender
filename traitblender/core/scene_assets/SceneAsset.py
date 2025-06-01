from abc import ABC, abstractmethod
import bpy
from mathutils import Vector, Euler
import math
import numpy as np

class SceneAsset(ABC): 
    """
    Abstract base class for managing Blender objects with enhanced transformation capabilities.
    
    SceneAsset provides a high-level interface for interacting with Blender objects, offering
    convenient properties for transformations (location, rotation, scale) with support for
    different origin types. This is particularly useful for museum-style morphological 
    visualizations where precise object placement and orientation are critical.
    
    Key Features:
    - Automatic object lookup by name in the Blender scene
    - Enhanced transform properties with origin-aware operations
    - Custom origin setting including 'BOTTOM_CENTER' for proper object placement
    - Type-safe property setters with flexible input formats
    - Preservation of original object origins during transformations
    
    Attributes:
        name (str): The name of the corresponding Blender object
        _current_origin_type (str): Tracks the current origin type for the object
    
    Subclasses:
        GenericAsset: General-purpose concrete implementation
        SurfaceAsset: Specialized for objects that serve as placement surfaces
    
    Example:
        asset = GenericAsset("Suzanne")
        asset.location = (0, 0, 5)  # Places at world origin + 5 units up
        asset.rotation_euler = (0, 0, math.pi/4)  # Rotates 45 degrees around Z-axis
        asset.scale = (2, 2, 2)  # Doubles the size uniformly
    """
    def __init__(self, name: str):
        self.name = name
        self._current_origin_type = "GEOMETRY_ORIGIN"  # Default Blender origin type

    @property
    def object(self):
        """Returns the Blender object with the same name as this asset"""
        obj = bpy.data.objects.get(self.name)
        if obj is None:
            raise ValueError(f"No object named '{self.name}' exists in the scene")
        return obj

    @property
    def location(self) -> Vector:
        """Returns the location of the object as a Vector"""
        return self.object.location

    @location.setter
    def location(self, value: Vector | tuple[float, float, float] | tuple[Vector | tuple[float, float, float], str]):
        """
        Sets the location of the object relative to specified origin
        
        Args:
            value: Can be:
                - Vector or (x,y,z) tuple (uses default origin_type="BOTTOM_CENTER")
                - (Vector or (x,y,z) tuple, origin_type) tuple to specify custom origin
        """
        # Handle (value, origin_type) tuple case
        if isinstance(value, tuple) and len(value) == 2 and isinstance(value[1], str):
            transform_value, origin_type = value
        else:
            transform_value = value
            origin_type = "BOTTOM_CENTER"
            
        # Convert to Vector if tuple
        if isinstance(transform_value, tuple):
            transform_value = Vector(transform_value)
            
        # Store original origin type
        original_origin = self._current_origin_type
        
        # Set to desired origin for transform
        self.origin_set(type=origin_type)
        
        # Apply transform
        self.object.location = transform_value
        
        # Restore original origin
        if original_origin != origin_type:
            self.origin_set(type=original_origin)

    @property
    def rotation_euler(self) -> Euler:
        """Returns the rotation of the object as Euler angles"""
        return self.object.rotation_euler

    @rotation_euler.setter
    def rotation_euler(self, value: Euler | tuple[float, float, float] | tuple[Euler | tuple[float, float, float], str]):
        """
        Sets the rotation of the object using Euler angles relative to specified origin
        
        Args:
            value: Can be:
                - Euler or (x,y,z) tuple (uses default origin_type="GEOMETRY_ORIGIN")
                - (Euler or (x,y,z) tuple, origin_type) tuple to specify custom origin
        """
        # Handle (value, origin_type) tuple case
        if isinstance(value, tuple) and len(value) == 2 and isinstance(value[1], str):
            transform_value, origin_type = value
        else:
            transform_value = value
            origin_type = "GEOMETRY_ORIGIN"
            
        # Convert to Euler if tuple
        if isinstance(transform_value, tuple):
            transform_value = Euler(transform_value)
            
        # Store original origin type
        original_origin = self._current_origin_type
        
        # Set to desired origin for transform
        self.origin_set(type=origin_type)
        
        # Apply transform
        self.object.rotation_euler = transform_value
        
        # Restore original origin
        if original_origin != origin_type:
            self.origin_set(type=original_origin)

    @property
    def scale(self) -> Vector:
        """Returns the scale of the object as a Vector"""
        return self.object.scale

    @scale.setter
    def scale(self, value: Vector | tuple[float, float, float] | tuple[Vector | tuple[float, float, float], str]):
        """
        Sets the scale of the object relative to specified origin
        
        Args:
            value: Can be:
                - Vector or (x,y,z) tuple (uses default origin_type="GEOMETRY_ORIGIN")
                - (Vector or (x,y,z) tuple, origin_type) tuple to specify custom origin
        """
        # Handle (value, origin_type) tuple case
        if isinstance(value, tuple) and len(value) == 2 and isinstance(value[1], str):
            transform_value, origin_type = value
        else:
            transform_value = value
            origin_type = "GEOMETRY_ORIGIN"
            
        # Convert to Vector if tuple
        if isinstance(transform_value, tuple):
            transform_value = Vector(transform_value)
            
        # Store original origin type
        original_origin = self._current_origin_type
        
        # Set to desired origin for transform
        self.origin_set(type=origin_type)
        
        # Apply transform
        self.object.scale = transform_value
        
        # Restore original origin
        if original_origin != origin_type:
            self.origin_set(type=original_origin)

    @property
    def dimensions(self) -> Vector:
        """Returns the dimensions (size) of the object as a Vector"""
        return self.object.dimensions

    @dimensions.setter
    def dimensions(self, value: Vector | tuple[float, float, float]):
        """Sets the dimensions (size) of the object"""
        if self.object:
            if isinstance(value, tuple):
                value = Vector(value)
            self.object.dimensions = value

    def origin_set(self, type: str = "GEOMETRY_ORIGIN", center: str = "MEDIAN"):
        """
        Set the object's origin. Extends Blender's origin_set with additional options.
        
        Args:
            type: Origin type. Can be:
                - "GEOMETRY_ORIGIN": Use the geometry's origin
                - "BOTTOM_CENTER": Place at bottom center using actual mesh vertices
                - Other standard Blender options like "ORIGIN_GEOMETRY", "ORIGIN_CURSOR", etc.
            center: Center type for Blender's origin_set (only used for standard Blender options)
        """
        if not self.object or not self.object.data or not isinstance(self.object.data, bpy.types.Mesh):
            return

        # Store current selection and active object
        current_selected = [obj for obj in bpy.context.selected_objects]
        current_active = bpy.context.active_object

        # Deselect all objects and select our target object
        bpy.ops.object.select_all(action='DESELECT')
        self.object.select_set(True)
        bpy.context.view_layer.objects.active = self.object

        if type == "BOTTOM_CENTER":
            # Get mesh data
            mesh = self.object.data
            
            # Get all vertex coordinates in local space (before world transform)
            local_verts = [vert.co for vert in mesh.vertices]
            
            # Find bounds in local space
            min_x = min(v.x for v in local_verts)
            max_x = max(v.x for v in local_verts)
            min_y = min(v.y for v in local_verts)
            max_y = max(v.y for v in local_verts)
            min_z = min(v.z for v in local_verts)  # This is the actual bottom
            
            # Calculate bottom center in local space
            bottom_center = Vector((
                (min_x + max_x) / 2,  # X center
                (min_y + max_y) / 2,  # Y center
                min_z                 # Bottom Z
            ))
            
            # Store current cursor location
            cursor_location = bpy.context.scene.cursor.location.copy()
            
            # Move cursor to bottom center in world space
            bpy.context.scene.cursor.location = self.object.matrix_world @ bottom_center
            
            # Ensure we're in object mode
            if bpy.context.active_object.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            
            # Set origin to cursor
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            
            # Restore cursor location
            bpy.context.scene.cursor.location = cursor_location
        else:
            # Use standard Blender origin setting
            bpy.ops.object.origin_set(type=type, center=center)

        # Update our tracked origin type
        self._current_origin_type = type

        # Restore previous selection and active object
        for obj in current_selected:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = current_active

class GenericAsset(SceneAsset):
    """A concrete implementation of SceneAsset that can be instantiated directly."""
    pass

class SurfaceAsset(SceneAsset):
    """
    A SceneAsset that provides a surface interface for placing other objects.
    The surface is defined by the upper square of the bounding box, with a -1 to 1 coordinate grid.
    """
    
    @property
    def surface(self) -> tuple[Vector, Vector, Vector, Vector]:
        """
        Returns the four corners of the surface in world space, ordered:
        [min_x,min_y, min_x,max_y, max_x,max_y, max_x,min_y]
        """
        if not self.object:
            raise ValueError(f"No object named '{self.name}' exists in the scene")
            
        # Get mesh data and world matrix
        mesh = self.object.data
        matrix_world = self.object.matrix_world
        
        # Get all vertex coordinates in world space
        world_verts = [matrix_world @ vert.co for vert in mesh.vertices]
        
        # Find bounds
        min_x = min(v.x for v in world_verts)
        max_x = max(v.x for v in world_verts)
        min_y = min(v.y for v in world_verts)
        max_y = max(v.y for v in world_verts)
        max_z = max(v.z for v in world_verts)  # We want the upper surface
        
        # Create the four corners in world space
        return (
            Vector((min_x, min_y, max_z)),  # Bottom left
            Vector((min_x, max_y, max_z)),  # Top left
            Vector((max_x, max_y, max_z)),  # Top right
            Vector((max_x, min_y, max_z)),  # Bottom right
        )
    
    @property
    def surface_normal(self) -> Vector:
        """Returns the normal vector of the surface in world space"""
        corners = self.surface
        edge1 = corners[1] - corners[0]  # Top left - Bottom left
        edge2 = corners[3] - corners[0]  # Bottom right - Bottom left
        normal = edge1.cross(edge2)
        return normal.normalized()
    
    def surface_to_world(self, coords: tuple[float, float]) -> Vector:
        """
        Convert surface coordinates (-1 to 1) to world position
        
        Args:
            coords: (x, y) coordinates in surface space, each from -1 to 1
        Returns:
            World space position on the surface
        """
        x, y = coords
        if not (-1 <= x <= 1 and -1 <= y <= 1):
            raise ValueError("Surface coordinates must be between -1 and 1")
            
        corners = self.surface
        
        # Convert from -1,1 space to 0,1 space
        x = (x + 1) / 2
        y = (y + 1) / 2
        
        # Bilinear interpolation between corners
        bottom = corners[0].lerp(corners[3], x)  # Interpolate along bottom edge
        top = corners[1].lerp(corners[2], x)     # Interpolate along top edge
        position = bottom.lerp(top, y)           # Interpolate between bottom and top
        
        return position
    
    def place(self, asset: SceneAsset, coords: tuple[float, float]):
        """
        Place an asset on the surface at the given coordinates.
        The asset will be positioned with its bottom center at the specified point,
        rotated to align with the surface normal, and parented to this surface.
        
        Args:
            asset: The SceneAsset to place
            coords: (x, y) coordinates in surface space, each from -1 to 1
        """
        # Ensure we're working with bottom center origin
        asset.origin_set(type="BOTTOM_CENTER")
        
        # Get world position and normal
        position = self.surface_to_world(coords)
        normal = self.surface_normal
        
        # Set location
        asset.location = position
        
        # Calculate rotation to align with normal
        # Get the object's current up vector in world space
        obj_matrix = asset.object.matrix_world
        current_up = obj_matrix.to_3x3() @ Vector((0, 0, 1))
        current_up.normalize()
        
        # Calculate rotation to align current up with surface normal
        rotation = current_up.rotation_difference(normal)
        
        # Apply the rotation in world space
        current_rot = asset.object.rotation_euler.copy()
        new_rot = (rotation.to_matrix().to_4x4() @ obj_matrix).to_euler()
        asset.rotation_euler = new_rot
        
        # Store current selection and active object
        current_selected = [obj for obj in bpy.context.selected_objects]
        current_active = bpy.context.active_object
        
        # Select both objects and make child active
        bpy.ops.object.select_all(action='DESELECT')
        asset.object.select_set(True)
        self.object.select_set(True)
        bpy.context.view_layer.objects.active = self.object
        
        # Parent with transforms preserved
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
        
        # Restore selection
        bpy.ops.object.select_all(action='DESELECT')
        for obj in current_selected:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = current_active




# Example of using SurfaceAsset
table = SurfaceAsset("Cube")  # The flat rectangular surface
suzanne = GenericAsset("Suzanne")  # The monkey head mesh

# Place Suzanne on the surface
table.place(suzanne, (0,0))  # Place Suzanne in the back left quadrant
