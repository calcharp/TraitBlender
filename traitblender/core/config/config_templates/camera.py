import bpy
from ..register_config import register

@register("camera")
class CameraConfig(bpy.types.PropertyGroup):
    camera_type: bpy.props.EnumProperty(
        name="Camera Type",
        description="The type of camera to use",
        items=[("perspective", "Perspective", "A perspective camera"),
               ("orthographic", "Orthographic", "An orthographic camera")],
        default="perspective"
    )
    focal_length: bpy.props.FloatProperty(
        name="Focal Length",
        description="The focal length of the camera",
        default=60.0,
        min=0.0
    )

    shift_x: bpy.props.FloatProperty(
        name="Shift X",
        description="The shift of the camera on the x-axis",
        default=0.0
    )
    shift_y: bpy.props.FloatProperty(
        name="Shift Y",
        description="The shift of the camera on the y-axis",
        default=0.0
    )

    use_dof: bpy.props.BoolProperty(
        name="Use DOF",
        description="Whether to use depth of field",
        default=False
    )

    focus_distance: bpy.props.FloatProperty(
        name="Focus Distance",
        description="The distance to the focus point",
        default=10.0,
        min=0.0
    )

    sensor_fit: bpy.props.EnumProperty(
        name="Sensor Fit",
        description="The fit of the sensor",
        items=[("auto", "Auto", "Auto"),
               ("horizontal", "Horizontal", "Horizontal"),
               ("vertical", "Vertical", "Vertical")],
        default="auto"
    )

    sensor_width: bpy.props.FloatProperty(
        name="Sensor Width",
        description="The width of the sensor",
        default=36.0,
        min=0.0
    )
    
    
