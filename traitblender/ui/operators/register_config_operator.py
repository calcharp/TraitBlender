import bpy
from bpy.types import Operator
from bpy.props import StringProperty
from ...core.config.register_config import register_config

class TRAITBLENDER_OT_register_config(Operator):
    bl_idname = "traitblender.register_config"
    bl_label = "Register Config"
    bl_description = "Load a YAML config file and update TraitBlender settings"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: StringProperty(
        name="Config File",
        description="Path to the YAML configuration file",
        subtype='FILE_PATH',
    )

    def execute(self, context):
        try:
            register_config(self.filepath)
            self.report({'INFO'}, f"Config loaded: {self.filepath}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'} 