import bpy
from ..register_config import register, TraitBlenderConfig
from ...helpers import get_property, set_property

@register("camera")
class CameraConfig(TraitBlenderConfig):
    print_index = 2
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
    # Normalized table coordinates
    location_table: bpy.props.FloatVectorProperty(
        name="Location (Table-Normalized)",
        description="Camera location in normalized table coordinates (-1 to 1 on X/Y, meters on Z)",
        default=(0.0, 0.0, 0.0),
        subtype='TRANSLATION',
        get=get_property("bpy.data.objects['Camera'].table_coords_norm", object_dependencies={"objects": ["Camera", "Table"]}),
        set=set_property("bpy.data.objects['Camera'].table_coords_norm", object_dependencies={"objects": ["Camera", "Table"]})
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
    resolution_x: bpy.props.IntProperty(
        name="Resolution X",
        description="The resolution of the render",
        get=get_property("bpy.context.scene.render.resolution_x"),
        set=set_property("bpy.context.scene.render.resolution_x")
    )
    resolution_y: bpy.props.IntProperty(
        name="Resolution Y",
        description="The resolution of the render",
        get=get_property("bpy.context.scene.render.resolution_y"),
        set=set_property("bpy.context.scene.render.resolution_y")
    )
    resolution_percentage: bpy.props.IntProperty(
        name="Resolution Percentage",
        description="The resolution of the render",
        min=0,
        max=100,
        get=get_property("bpy.context.scene.render.resolution_percentage"),
        set=set_property("bpy.context.scene.render.resolution_percentage")
    )
    aspect_x: bpy.props.FloatProperty(
        name="Aspect X",
        description="The aspect of the render",
        get=get_property("bpy.context.scene.render.pixel_aspect_x"),
        set=set_property("bpy.context.scene.render.pixel_aspect_x")
    )
    aspect_y: bpy.props.FloatProperty(
        name="Aspect Y",
        description="The aspect of the render",
        get=get_property("bpy.context.scene.render.pixel_aspect_y"),
        set=set_property("bpy.context.scene.render.pixel_aspect_y")
    )
    shift_x: bpy.props.FloatProperty(
        name="Shift X",
        description="The shift of the camera on the x-axis",
        get=get_property("bpy.data.cameras['Camera'].shift_x", 
                        object_dependencies={"cameras": ["Camera"]}),
        set=set_property("bpy.data.cameras['Camera'].shift_x", 
                        object_dependencies={"cameras": ["Camera"]})
    )
    shift_y: bpy.props.FloatProperty(
        name="Shift Y",
        description="The shift of the camera on the y-axis",
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



    
