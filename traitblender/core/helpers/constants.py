"""
Shared constants for TraitBlender core helpers.
"""

# Add-on package name (used for addon root and user data paths)
ADDON_PACKAGE = "bl_ext.user_default.traitblender"

# Config path: vector component names to index (x/y/z, r/g/b/a)
COMPONENT_TO_INDEX = {
    "x": 0, "y": 1, "z": 2,
    "r": 0, "g": 1, "b": 2, "a": 3,
}

# Valid Blender property types from bpy.props (for type checking)
VALID_PROPERTY_TYPES = {
    "BoolProperty",
    "BoolVectorProperty",
    "EnumProperty",
    "FloatProperty",
    "FloatVectorProperty",
    "IntProperty",
    "IntVectorProperty",
    "StringProperty",
}

# Supported texture types for material application
VALID_TEXTURES = {"DIFFUSE", "AO", "ROUGHNESS", "METALLIC", "NORMAL", "DISPLACEMENT"}
