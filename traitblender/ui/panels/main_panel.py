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
        row = layout.row(align=True)
        row.operator("traitblender.setup_scene", text="Setup Museum Scene") 