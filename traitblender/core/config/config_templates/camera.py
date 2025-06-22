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
    