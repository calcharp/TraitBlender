import bpy
from bpy.props import StringProperty, EnumProperty, BoolProperty
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
        default=0,
        update=lambda self, context: self._on_morphospace_change(context),
    )

    # Internal state for morphospace switching confirmation
    prev_morphospace: StringProperty(default="", options={'HIDDEN'})
    pending_morphospace: StringProperty(default="", options={'HIDDEN'})
    suppress_morphospace_update: BoolProperty(default=False, options={'HIDDEN'})
    
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

    def _on_morphospace_change(self, context):
        """
        Confirm morphospace switch because it invalidates the current dataset columns.
        - On Yes: switch + clear dataset (filepath/csv) so default dataset regenerates.
        - On No: keep previous morphospace selection.
        """
        if self.suppress_morphospace_update:
            return

        new_value = self.available_morphospaces

        # First time initialization: accept current selection as previous
        if not self.prev_morphospace:
            self.prev_morphospace = new_value
            return

        if new_value == self.prev_morphospace:
            return

        # Headless / batch: no windows for popup_menu; apply switch without confirmation.
        if getattr(bpy.app, "background", False):
            self.prev_morphospace = new_value
            self.pending_morphospace = ""
            return

        # Stash the user's requested morphospace, revert selection immediately, then show popup.
        self.pending_morphospace = new_value
        self.suppress_morphospace_update = True
        try:
            self.available_morphospaces = self.prev_morphospace
        finally:
            self.suppress_morphospace_update = False

        try:
            bpy.ops.traitblender.morphospace_switch_popup('INVOKE_DEFAULT')
        except Exception as e:
            # If popup fails for any reason, fall back to switching without confirmation.
            print(f"TraitBlender: Failed to show morphospace switch confirmation popup: {e}")
            self.pending_morphospace = ""