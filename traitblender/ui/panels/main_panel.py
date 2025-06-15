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
        row = box.row(align=True)
        row.prop(wm, "tb_camera_type", text="")
        row.operator("traitblender.set_camera_type", text="Apply").camera_type = wm.tb_camera_type

        # Lens Settings
        box = layout.box()
        box.label(text="Lens Settings")
        row = box.row(align=True)
        row.prop(wm, "tb_lens", text="Focal Length")
        row.operator("traitblender.set_camera_lens", text="Apply").lens = wm.tb_lens
        row = box.row(align=True)
        row.prop(wm, "tb_lens_unit", text="Unit")
        row.operator("traitblender.set_camera_lens_unit", text="Apply").lens_unit = wm.tb_lens_unit

        # Shift Settings
        box = layout.box()
        box.label(text="Shift")
        row = box.row(align=True)
        row.prop(wm, "tb_shift_x", text="X")
        row.prop(wm, "tb_shift_y", text="Y")
        op = row.operator("traitblender.set_camera_shift", text="Apply")
        op.shift_x = wm.tb_shift_x
        op.shift_y = wm.tb_shift_y

        # Clipping Settings
        box = layout.box()
        box.label(text="Clipping")
        row = box.row(align=True)
        row.prop(wm, "tb_clip_start", text="Start")
        row.prop(wm, "tb_clip_end", text="End")
        op = row.operator("traitblender.set_camera_clip", text="Apply")
        op.clip_start = wm.tb_clip_start
        op.clip_end = wm.tb_clip_end

        # Sensor Settings
        box = layout.box()
        box.label(text="Sensor")
        row = box.row(align=True)
        row.prop(wm, "tb_sensor_fit", text="Fit")
        row.prop(wm, "tb_sensor_width", text="Width")
        op = row.operator("traitblender.set_camera_sensor", text="Apply")
        op.sensor_fit = wm.tb_sensor_fit
        op.sensor_width = wm.tb_sensor_width

        # Render Button
        box = layout.box()
        box.label(text="Render")
        row = box.row(align=True)
        row.prop(wm, "tb_render_filename", text="Filename")
        row.prop(wm, "tb_render_extension", text="Extension")
        op = row.operator("traitblender.camera_render", text="Render")
        op.filename = wm.tb_render_filename
        op.extension = wm.tb_render_extension

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