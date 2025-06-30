import bpy


def get_property(property_path: str, options: list = None):
    """Create a getter function for a Blender property.
    
    Args:
        property_path (str): The Blender property path (e.g., 
                           'bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value')
        options (list, optional): List of enum options for pattern matching. If provided, 
                                 the getter will return an int index instead of a string.
    
    Returns:
        function: A getter function that returns the value of the specified Blender property
        
    Raises:
        RuntimeError: If getting the value fails at runtime or if enum pattern matching fails
        
    Example:
        >>> getter = get_property('bpy.data.cameras["Camera"].type')
        >>> value = getter(self)  # Returns the current value of the property
        
        >>> getter = get_property('bpy.data.cameras["Camera"].type', 
        ...                       options=["PERSP", "ORTHO", "PANO"])
        >>> value = getter(self)  # Returns the int index (0, 1, or 2)
    """
    def get(self):
        try:
            value = eval(property_path)
            
            # If options are provided, treat this as an enum and return the index
            if options is not None:
                if value not in options:
                    raise RuntimeError(f"Enum value '{value}' not found in options list: {options}")
                return options.index(value)
            
            return value
        except Exception as e:
            import traceback
            print(f"Error getting property '{property_path}': {e}")
            print(f"Traceback: {traceback.format_exc()}")
            raise RuntimeError(f"Failed to get value from property '{property_path}': {e}")
    return get


def set_property(property_path: str, options: list = None):
    """Create a setter function for a Blender property.
    
    Args:
        property_path (str): The Blender property path (e.g., 
                           'bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value')
        options (list, optional): List of enum options for pattern matching. If provided, 
                                 the setter will convert integer indices to string values.
    
    Returns:
        function: A setter function that sets the value of the specified Blender property
        
    Raises:
        RuntimeError: If setting the value fails at runtime or if enum conversion fails
        
    Example:
        >>> setter = set_property('bpy.data.cameras["Camera"].type')
        >>> setter(self, "PERSP")  # Sets the property to a string value
        
        >>> setter = set_property('bpy.data.cameras["Camera"].type', 
        ...                       options=["PERSP", "ORTHO", "PANO"])
        >>> setter(self, 1)  # Converts 1 to "ORTHO" and sets the property
    """
    def set(self, value):
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
            print(f"Error setting property '{property_path}' to value '{value}': {e}")
            print(f"Traceback: {traceback.format_exc()}")
            raise RuntimeError(f"Failed to set value for property '{property_path}': {e}")
    return set
