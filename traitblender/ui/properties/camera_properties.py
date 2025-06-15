import bpy

def update_camera_type(self, context):
    try:
        cam = bpy.data.objects["Camera"].data
        cam.type = self.tb_camera_type
    except Exception:
        pass

def update_lens(self, context):
    try:
        cam = bpy.data.objects["Camera"].data
        cam.lens = self.tb_lens
    except Exception:
        pass

def update_lens_unit(self, context):
    try:
        cam = bpy.data.objects["Camera"].data
        cam.lens_unit = self.tb_lens_unit
    except Exception:
        pass

def update_shift_x(self, context):
    try:
        cam = bpy.data.objects["Camera"].data
        cam.shift_x = self.tb_shift_x
    except Exception:
        pass

def update_shift_y(self, context):
    try:
        cam = bpy.data.objects["Camera"].data
        cam.shift_y = self.tb_shift_y
    except Exception:
        pass

def update_clip_start(self, context):
    try:
        cam = bpy.data.objects["Camera"].data
        cam.clip_start = self.tb_clip_start
    except Exception:
        pass

def update_clip_end(self, context):
    try:
        cam = bpy.data.objects["Camera"].data
        cam.clip_end = self.tb_clip_end
    except Exception:
        pass

def update_sensor_fit(self, context):
    try:
        cam = bpy.data.objects["Camera"].data
        cam.sensor_fit = self.tb_sensor_fit
    except Exception:
        pass

def update_sensor_width(self, context):
    try:
        cam = bpy.data.objects["Camera"].data
        cam.sensor_width = self.tb_sensor_width
    except Exception:
        pass

def register_camera_properties():
    bpy.types.WindowManager.tb_camera_type = bpy.props.EnumProperty(
        name="Camera Type",
        items=[
            ('PERSP', "Perspective", "Perspective camera"),
            ('ORTHO', "Orthographic", "Orthographic camera"),
            ('PANO', "Panoramic", "Panoramic camera"),
        ],
        default='PERSP',
        update=update_camera_type
    )
    bpy.types.WindowManager.tb_lens = bpy.props.FloatProperty(
        name="Focal Length", default=50.0, min=1.0, update=update_lens
    )
    bpy.types.WindowManager.tb_lens_unit = bpy.props.EnumProperty(
        name="Lens Unit",
        items=[
            ('MILLIMETERS', "Millimeters", "Focal length in millimeters"),
            ('FOV', "Field of View", "Field of view in degrees"),
        ],
        default='MILLIMETERS',
        update=update_lens_unit
    )
    bpy.types.WindowManager.tb_shift_x = bpy.props.FloatProperty(
        name="Shift X", default=0.0, update=update_shift_x
    )
    bpy.types.WindowManager.tb_shift_y = bpy.props.FloatProperty(
        name="Shift Y", default=0.0, update=update_shift_y
    )
    bpy.types.WindowManager.tb_clip_start = bpy.props.FloatProperty(
        name="Clip Start", default=0.1, min=0.001, update=update_clip_start
    )
    bpy.types.WindowManager.tb_clip_end = bpy.props.FloatProperty(
        name="Clip End", default=1000.0, min=0.001, update=update_clip_end
    )
    bpy.types.WindowManager.tb_sensor_fit = bpy.props.EnumProperty(
        name="Sensor Fit",
        items=[
            ('AUTO', "Auto", "Automatic sensor fit"),
            ('HORIZONTAL', "Horizontal", "Fit to horizontal"),
            ('VERTICAL', "Vertical", "Fit to vertical"),
        ],
        default='AUTO',
        update=update_sensor_fit
    )
    bpy.types.WindowManager.tb_sensor_width = bpy.props.FloatProperty(
        name="Sensor Width", default=36.0, min=0.1, update=update_sensor_width
    )
    bpy.types.WindowManager.tb_render_filename = bpy.props.StringProperty(
        name="Filename", default=""
    )
    bpy.types.WindowManager.tb_render_extension = bpy.props.StringProperty(
        name="Extension", default="png"
    )

def unregister_camera_properties():
    del bpy.types.WindowManager.tb_camera_type
    del bpy.types.WindowManager.tb_lens
    del bpy.types.WindowManager.tb_lens_unit
    del bpy.types.WindowManager.tb_shift_x
    del bpy.types.WindowManager.tb_shift_y
    del bpy.types.WindowManager.tb_clip_start
    del bpy.types.WindowManager.tb_clip_end
    del bpy.types.WindowManager.tb_sensor_fit
    del bpy.types.WindowManager.tb_sensor_width
    del bpy.types.WindowManager.tb_render_filename
    del bpy.types.WindowManager.tb_render_extension 