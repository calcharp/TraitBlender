import bpy
from ..register_config import register
from ...helpers import get_property, set_property

@register("camera")
class CameraConfig(bpy.types.PropertyGroup):
    location: bpy.props.FloatVectorProperty(
        name="Location",
        description="The location of the camera",
        default=(0.0, 0.0, 0.0),
        get=get_property("bpy.data.objects['Camera'].location"),
        set=set_property("bpy.data.objects['Camera'].location")
    )
    rotation: bpy.props.FloatVectorProperty(
        name="Rotation",
        description="The rotation of the camera",
        default=(0.0, 0.0, 0.0),
        get=get_property("bpy.data.objects['Camera'].rotation_euler"),
        set=set_property("bpy.data.objects['Camera'].rotation_euler")
    )
    camera_type: bpy.props.EnumProperty(
        name="Camera Type",
        description="The type of camera to use",
        items=[("PERSP", "Perspective", "A perspective camera"),
               ("ORTHO", "Orthographic", "An orthographic camera"),
               ("PANO", "Panoramic", "A panoramic camera")],
        default=0,
        get=get_property("bpy.data.cameras['Camera'].type", options=["PERSP", "ORTHO", "PANO"]),
        set=set_property("bpy.data.cameras['Camera'].type")
    )
    focal_length: bpy.props.FloatProperty(
        name="Focal Length",
        description="The focal length of the camera",
        default=60.0,
        min=0.0,
        get=get_property("bpy.data.cameras['Camera'].lens"),
        set=set_property("bpy.data.cameras['Camera'].lens")
    )
    shift_x: bpy.props.FloatProperty(
        name="Shift X",
        description="The shift of the camera on the x-axis",
        default=0.0,
        get=get_property("bpy.data.cameras['Camera'].shift_x"),
        set=set_property("bpy.data.cameras['Camera'].shift_x")
    )
    shift_y: bpy.props.FloatProperty(
        name="Shift Y",
        description="The shift of the camera on the y-axis",
        default=0.0,
        get=get_property("bpy.data.cameras['Camera'].shift_y"),
        set=set_property("bpy.data.cameras['Camera'].shift_y")
    )


    
