import bpy

# Mapping from string type names to Blender property types
PROPERTY_TYPE_MAP = {
    int: bpy.props.IntProperty,
    float: bpy.props.FloatProperty,
    str: bpy.props.StringProperty,
    bool: bpy.props.BoolProperty,
    list[int]: bpy.props.IntVectorProperty,
    list[float]: bpy.props.FloatVectorProperty,
    list[bool]: bpy.props.BoolVectorProperty,
    list[str]: bpy.props.CollectionProperty,
    list[list[float]]: bpy.types.PropertyGroup,  # Matrix group, handled specially
}

def get_bpy_prop_from_type_hint(type_hint):
    """
    Map a Python type hint to a Blender property type using PROPERTY_TYPE_MAP.
    For list[list[float]], returns PropertyGroup.
    """
    try:
        return PROPERTY_TYPE_MAP[type_hint]
    except KeyError:
        raise TypeError(f"No Blender property type mapping for type hint: {type_hint}") 