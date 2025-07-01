import bpy
from ..register_config import register
from ...helpers import get_property, set_property

@register("camera")
class CameraConfig(bpy.types.PropertyGroup):
    location: bpy.props.FloatVectorProperty(
        name="Location",
        description="The location of the camera",
        default=(0.0, 0.0, 0.0),
        subtype='TRANSLATION',
        get=get_property("bpy.data.objects['Camera'].location", 
                        object_dependencies={"objects": ["Camera"]}),
        set=set_property("bpy.data.objects['Camera'].location", 
                        object_dependencies={"objects": ["Camera"]})
    )
    rotation: bpy.props.FloatVectorProperty(
        name="Rotation",
        description="The rotation of the camera",
        default=(0.0, 0.0, 0.0),
        subtype='EULER',
        get=get_property("bpy.data.objects['Camera'].rotation_euler", 
                        object_dependencies={"objects": ["Camera"]}),
        set=set_property("bpy.data.objects['Camera'].rotation_euler", 
                        object_dependencies={"objects": ["Camera"]})
    )
    camera_type: bpy.props.EnumProperty(
        name="Camera Type",
        description="The type of camera to use",
        items=[("PERSP", "Perspective", "A perspective camera"),
               ("ORTHO", "Orthographic", "An orthographic camera"),
               ("PANO", "Panoramic", "A panoramic camera")],
        default=0,
        get=get_property("bpy.data.cameras['Camera'].type", 
                        options=["PERSP", "ORTHO", "PANO"],
                        object_dependencies={"cameras": ["Camera"]}),
        set=set_property("bpy.data.cameras['Camera'].type", 
                        options=["PERSP", "ORTHO", "PANO"],
                        object_dependencies={"cameras": ["Camera"]})
    )
    focal_length: bpy.props.FloatProperty(
        name="Focal Length",
        description="The focal length of the camera",
        default=60.0,
        min=0.0,
        get=get_property("bpy.data.cameras['Camera'].lens", 
                        object_dependencies={"cameras": ["Camera"]}),
        set=set_property("bpy.data.cameras['Camera'].lens", 
                        object_dependencies={"cameras": ["Camera"]})
    )
    shift_x: bpy.props.FloatProperty(
        name="Shift X",
        description="The shift of the camera on the x-axis",
        default=0.0,
        get=get_property("bpy.data.cameras['Camera'].shift_x", 
                        object_dependencies={"cameras": ["Camera"]}),
        set=set_property("bpy.data.cameras['Camera'].shift_x", 
                        object_dependencies={"cameras": ["Camera"]})
    )
    shift_y: bpy.props.FloatProperty(
        name="Shift Y",
        description="The shift of the camera on the y-axis",
        default=0.0,
        get=get_property("bpy.data.cameras['Camera'].shift_y", 
                        object_dependencies={"cameras": ["Camera"]}),
        set=set_property("bpy.data.cameras['Camera'].shift_y", 
                        object_dependencies={"cameras": ["Camera"]})
    )
    lens_unit: bpy.props.EnumProperty(
        name="Lens Unit",
        description="Unit for camera lens",
        items=[('MILLIMETERS', "Millimeters", "Focal length in mm"),
               ('FOV', "Field of View", "Field of view in degrees")],
        get=get_property("bpy.data.cameras['Camera'].lens_unit", options=['MILLIMETERS', 'FOV'],
                         object_dependencies={'cameras': ['Camera']}),
        set=set_property("bpy.data.cameras['Camera'].lens_unit", options=['MILLIMETERS', 'FOV'],
                         object_dependencies={'cameras': ['Camera']})
    )


    
