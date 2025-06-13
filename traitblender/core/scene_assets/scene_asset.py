from abc import ABC, abstractmethod
import bpy
from mathutils import Vector, Euler
import math
import numpy as np
from ..helpers.object_validator import ObjectNotFoundError, check_object_exists

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
        check_object_exists(self.name)
        obj = bpy.data.objects.get(self.name)
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
            
        # If we're already at the desired origin, just set location directly
        if self._current_origin_type == origin_type:
            self.object.location = transform_value
            return
            
        # Store original origin type and current world location
        original_origin = self._current_origin_type
        
        # Set to desired origin for transform
        self.origin_set(type=origin_type)
        
        # Apply transform
        self.object.location = transform_value
        
        # Restore original origin
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
        
        Raises:
            ObjectNotFoundError: If the object doesn't exist or is not a mesh
        """
        check_object_exists(self.name)
        if not self.object or not self.object.data or not isinstance(self.object.data, bpy.types.Mesh):
            raise ObjectNotFoundError(f"Object '{self.name}' is not a valid mesh object for origin setting")
        
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


# Dictionary mapping asset names to their corresponding asset types
ASSET_TYPES = {
    "GenericAsset": GenericAsset
}

