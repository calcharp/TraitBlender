import bpy
from bpy.props import StringProperty, EnumProperty
from ...core.morphospaces import list_morphospaces


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
        """Get available morphospaces for the enum."""
        items = []
        try:
            morphospaces = list_morphospaces()
            for name in morphospaces:
                # Use the literal folder name for both value and display
                items.append((name, name, f"Morphospace: {name}"))
        except Exception as e:
            print(f"Error getting morphospace items: {e}")
        return items 