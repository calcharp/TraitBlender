import bpy
from bpy.props import StringProperty, EnumProperty
from ...core.morphospaces import list_morphospaces, get_morphospace_display_name


class TraitBlenderSetupProperties(bpy.types.PropertyGroup):
    """Property group for TraitBlender setup configuration."""
    
    config_file: StringProperty(
        name="Config File",
        description="Path to YAML configuration file",
        default="",
        subtype='FILE_PATH'
    )
    
    available_morphospaces: EnumProperty(
        name="Available Morphospaces",
        description="List of available morphospace modules",
        items=lambda self, context: self._get_morphospace_items(),
        default=0
    )
    
    def _get_morphospace_items(self):
        """Get available morphospaces for the enum. Identifier = NAME from module (or folder if no NAME)."""
        items = []
        try:
            morphospaces = list_morphospaces()
            for folder_name in morphospaces:
                identifier = get_morphospace_display_name(folder_name)
                items.append((identifier, identifier, f"Morphospace: {identifier}"))
        except Exception as e:
            print(f"Error getting morphospace items: {e}")
        return items