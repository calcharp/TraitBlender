import bpy
from bpy.props import StringProperty


class TraitBlenderSetupProperties(bpy.types.PropertyGroup):
    """Property group for TraitBlender setup configuration."""
    
    config_file: StringProperty(
        name="Config File",
        description="Path to YAML configuration file",
        default="",
        subtype='FILE_PATH'
    ) 