import bpy
from bpy.types import Panel


class TRAITBLENDER_PT_main_panel(Panel):
    bl_label = "TraitBlender"
    bl_idname = "TRAITBLENDER_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TraitBlender'

    def draw(self, context):
        layout = self.layout
        
        # Setup Museum Scene button
        row = layout.row(align=True)
        row.operator("traitblender.setup_scene", text="Setup Museum Scene")
        
        # Configuration section
        layout.separator()
        
        # Config file path row
        row = layout.row(align=True)
        row.prop(context.scene.traitblender_setup, "config_file", text="Config File")
        
        # Configure and Show Configuration buttons row
        row = layout.row(align=True)
        row.operator("traitblender.configure_scene", text="Configure Scene")
        row.operator("traitblender.show_configuration", text="Show Configuration")
        
        # Export Config button row
        row = layout.row(align=True)
        row.operator("traitblender.export_config", text="Export Config as YAML") 