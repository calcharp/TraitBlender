import bpy

def register_camera_properties():
    bpy.types.WindowManager.tb_camera_type = bpy.props.EnumProperty(
        name="Camera Type",
        items=[
            ('PERSP', "Perspective", "Perspective camera"),
            ('ORTHO', "Orthographic", "Orthographic camera"),
            ('PANO', "Panoramic", "Panoramic camera"),
        ],
        default='PERSP'
    )
    bpy.types.WindowManager.tb_lens = bpy.props.FloatProperty(
        name="Focal Length", default=50.0, min=1.0
    )
    bpy.types.WindowManager.tb_lens_unit = bpy.props.EnumProperty(
        name="Lens Unit",
        items=[
            ('MILLIMETERS', "Millimeters", "Focal length in millimeters"),
            ('FOV', "Field of View", "Field of view in degrees"),
        ],
        default='MILLIMETERS'
    )
    bpy.types.WindowManager.tb_shift_x = bpy.props.FloatProperty(
        name="Shift X", default=0.0
    )
    bpy.types.WindowManager.tb_shift_y = bpy.props.FloatProperty(
        name="Shift Y", default=0.0
    )
    bpy.types.WindowManager.tb_clip_start = bpy.props.FloatProperty(
        name="Clip Start", default=0.1, min=0.001
    )
    bpy.types.WindowManager.tb_clip_end = bpy.props.FloatProperty(
        name="Clip End", default=1000.0, min=0.001
    )
    bpy.types.WindowManager.tb_sensor_fit = bpy.props.EnumProperty(
        name="Sensor Fit",
        items=[
            ('AUTO', "Auto", "Automatic sensor fit"),
            ('HORIZONTAL', "Horizontal", "Fit to horizontal"),
            ('VERTICAL', "Vertical", "Fit to vertical"),
        ],
        default='AUTO'
    )
    bpy.types.WindowManager.tb_sensor_width = bpy.props.FloatProperty(
        name="Sensor Width", default=36.0, min=0.1
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