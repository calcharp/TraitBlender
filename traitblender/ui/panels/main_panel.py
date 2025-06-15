import bpy
from bpy.types import Panel

class TRAITBLENDER_PT_camera_panel(Panel):
    """Camera settings panel for TraitBlender"""
    bl_label = "Camera"
    bl_idname = "TRAITBLENDER_PT_camera_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TraitBlender'
    bl_parent_id = "TRAITBLENDER_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout

        # Camera Type
        box = layout.box()
        box.label(text="Camera Type")
        box.prop(wm, "tb_camera_type", text="")

        # Lens Settings
        box = layout.box()
        box.label(text="Lens Settings")
        box.prop(wm, "tb_lens", text="Focal Length")
        box.prop(wm, "tb_lens_unit", text="Unit")

        # Shift Settings
        box = layout.box()
        box.label(text="Shift")
        box.prop(wm, "tb_shift_x", text="X")
        box.prop(wm, "tb_shift_y", text="Y")

        # Clipping Settings
        box = layout.box()
        box.label(text="Clipping")
        box.prop(wm, "tb_clip_start", text="Start")
        box.prop(wm, "tb_clip_end", text="End")

        # Sensor Settings
        box = layout.box()
        box.label(text="Sensor")
        box.prop(wm, "tb_sensor_fit", text="Fit")
        box.prop(wm, "tb_sensor_width", text="Width")

        # Render Button
        box = layout.box()
        box.label(text="Render")
        box.prop(wm, "tb_render_filename", text="Filename")
        box.prop(wm, "tb_render_extension", text="Extension")
        box.operator("traitblender.camera_render", text="Render")

class TRAITBLENDER_PT_main_panel(Panel):
    bl_label = "TraitBlender"
    bl_idname = "TRAITBLENDER_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TraitBlender'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("traitblender.setup_scene", text="Setup Museum Scene") 