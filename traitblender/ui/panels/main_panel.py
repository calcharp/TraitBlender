import bpy
from bpy.types import Panel

def register_panel_properties():
    bpy.types.WindowManager.tb_config_path = bpy.props.StringProperty(
        name="Config File",
        description="Path to the YAML configuration file",
        subtype='FILE_PATH',
        default="",
        update=auto_load_config
    )

def unregister_panel_properties():
    del bpy.types.WindowManager.tb_config_path

def auto_load_config(self, context):
    if self.tb_config_path:
        try:
            from ..operators.register_config_operator import register_config
            register_config(self.tb_config_path)
        except Exception as e:
            self.tb_config_path = ""  # Optionally clear on error
            self.report({'ERROR'}, str(e))

class TRAITBLENDER_PT_main_panel(Panel):
    bl_label = "TraitBlender"
    bl_idname = "TRAITBLENDER_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TraitBlender'

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout
        # Config file selector row
        row = layout.row(align=True)
        row.prop(wm, "tb_config_path", text="", icon='FILE_FOLDER')
        # Only the setup scene button in the next row
        row = layout.row(align=True)
        row.operator("traitblender.setup_scene", text="Setup Museum Scene") 