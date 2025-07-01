import bpy
import warnings
import inspect
import mathutils


def _check_object_dependencies(object_dependencies):
    """Check if all required objects exist in the scene.
    
    Args:
        object_dependencies (dict): Dictionary mapping object types to lists of required names.
                                  Example: {"objects": ["Camera"], "cameras": ["Camera"], "worlds": ["World"]}
    
    Returns:
        bool: True if all dependencies exist, False otherwise
    """
    if not object_dependencies:
        return True
    
    for obj_type, names in object_dependencies.items():
        collection = getattr(bpy.data, obj_type, None)
        if collection is None:
            return False
        
        for name in names:
            if name not in collection:
                return False
    
    return True


def get_property(property_path: str, options: list = None, object_dependencies: dict = None):
    """Create a getter function for a Blender property.
    
    Args:
        property_path (str): The Blender property path (e.g., 
                           'bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value')
        options (list, optional): List of enum options for pattern matching. If provided, 
                                 the getter will return an int index instead of a string.
        object_dependencies (dict, optional): Dictionary mapping object types to lists of required names.
                                            If any dependency is missing, the getter returns None.
                                            Example: {"objects": ["Camera"], "cameras": ["Camera"]}
    
    Returns:
        function: A getter function that returns the value of the specified Blender property
        
    Raises:
        RuntimeError: If getting the value fails at runtime or if enum pattern matching fails
        
    Example:
        >>> getter = get_property('bpy.data.objects["Camera"].location', 
        ...                       object_dependencies={"objects": ["Camera"]})
        >>> value = getter(self)  # Returns None if Camera doesn't exist
        
        >>> getter = get_property('bpy.data.cameras["Camera"].type', 
        ...                       options=["PERSP", "ORTHO", "PANO"],
        ...                       object_dependencies={"cameras": ["Camera"]})
        >>> value = getter(self)  # Returns None if Camera doesn't exist
    """
    def get(self):
        def _auto_default():
            # Try to get the property value from the instance using the calling property name
            prop_val = None
            try:
                prop_name = inspect.currentframe().f_back.f_code.co_name
                prop_val = getattr(self, prop_name, None)
            except Exception:
                pass
            if isinstance(prop_val, mathutils.Vector):
                return tuple([0.0] * len(prop_val))
            return 0.0

        if not _check_object_dependencies(object_dependencies):
            val = _auto_default()
            warnings.warn(f"[TraitBlender] Missing required Blender objects for property: {property_path}\n\nYou may need to run bpy.ops.traitblender.setup_scene()", UserWarning)
            return val if options is None else 0
        try:
            value = eval(property_path)
            # If options are provided, treat this as an enum and return the index
            if options is not None:
                if value not in options:
                    raise RuntimeError(f"Enum value '{value}' not found in options list: {options}")
                return options.index(value)
            return value
        except Exception:
            val = _auto_default()
            warnings.warn(f"[TraitBlender] Error accessing property: {property_path}", UserWarning)
            return val if options is None else 0
    return get


def set_property(property_path: str, options: list = None, object_dependencies: dict = None):
    """Create a setter function for a Blender property.
    
    Args:
        property_path (str): The Blender property path (e.g., 
                           'bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value')
        options (list, optional): List of enum options for pattern matching. If provided, 
                                 the setter will convert integer indices to string values.
        object_dependencies (dict, optional): Dictionary mapping object types to lists of required names.
                                            If any dependency is missing, the setter does nothing.
                                            Example: {"objects": ["Camera"], "cameras": ["Camera"]}
    
    Returns:
        function: A setter function that sets the value of the specified Blender property
        
    Raises:
        RuntimeError: If setting the value fails at runtime or if enum conversion fails
        
    Example:
        >>> setter = set_property('bpy.data.objects["Camera"].location', 
        ...                       object_dependencies={"objects": ["Camera"]})
        >>> setter(self, (0, 0, 5))  # Does nothing if Camera doesn't exist
        
        >>> setter = set_property('bpy.data.cameras["Camera"].type', 
        ...                       options=["PERSP", "ORTHO", "PANO"],
        ...                       object_dependencies={"cameras": ["Camera"]})
        >>> setter(self, 1)  # Does nothing if Camera doesn't exist
    """
    def set(self, value):
        if not _check_object_dependencies(object_dependencies):
            return  # Silently do nothing if dependencies are missing
        
        try:
            # If options are provided, treat this as an enum and convert index to string
            if options is not None:
                if isinstance(value, int):
                    if value < 0 or value >= len(options):
                        raise RuntimeError(f"Enum index {value} out of range for options: {options}")
                    value = options[value]
                elif value not in options:
                    raise RuntimeError(f"Enum value '{value}' not found in options list: {options}")
            
            # Use exec with bpy and value in the namespace for complex Blender properties
            exec(f"{property_path} = value", {"bpy": bpy, "value": value})
        except Exception as e:
            import traceback
            warnings.warn(f"Error setting property '{property_path}' to value '{value}': {e}\nTraceback: {traceback.format_exc()}", UserWarning)
            raise RuntimeError(f"Failed to set value for property '{property_path}': {e}")
    return set
