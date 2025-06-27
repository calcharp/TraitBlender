import bpy


def get_property(property_path: str):
    """Create a getter function for a Blender property.
    
    Args:
        property_path (str): The Blender property path (e.g., 
                           'bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value')
    
    Returns:
        function: A getter function that returns the value of the specified Blender property
        
    Raises:
        RuntimeError: If getting the value fails at runtime
        
    Example:
        >>> getter = get_property('bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value')
        >>> value = getter(self)  # Returns the current value of the property
    """
    def get(self):
        try:
            return eval(property_path)
        except Exception as e:
            raise RuntimeError(f"Failed to get value from property '{property_path}': {e}")
    return get


def set_property(property_path: str):
    """Create a setter function for a Blender property.
    
    Args:
        property_path (str): The Blender property path (e.g., 
                           'bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value')
    
    Returns:
        function: A setter function that sets the value of the specified Blender property
        
    Raises:
        RuntimeError: If setting the value fails at runtime
        
    Example:
        >>> setter = set_property('bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value')
        >>> setter(self, (1.0, 0.5, 0.2, 1.0))  # Sets the property to a new color value
    """
    def set(self, value):
        try:
            # Use exec with bpy and value in the namespace for complex Blender properties
            exec(f"{property_path} = value", {"bpy": bpy, "value": value})
        except Exception as e:
            raise RuntimeError(f"Failed to set value for property '{property_path}': {e}")
    return set
