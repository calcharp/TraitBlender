import bpy
from ..register_config import register, TraitBlenderConfig
from ...helpers import get_property, set_property


@register("output")
class OutputConfig(TraitBlenderConfig):
    print_index = 6
    output_type: bpy.props.EnumProperty(
        name="Output Type",
        description="The type of material to use",
        items=[("image", "Image", "An image output"),
               ("video", "Video", "A video output")],
        default="image"
    )

    image_format: bpy.props.EnumProperty(
        name="Image Format",
        description="The format of the image",
        items=[("PNG", "PNG", "PNG"),
               ("JPEG", "JPEG", "JPEG")])
    
    output_directory: bpy.props.StringProperty(
        name="Base Output Path",
        description="The base path of the output",
        default="",
        subtype='DIR_PATH'
    )

    images_per_view: bpy.props.IntProperty(
        name="Images Per View",
        description="Number of images to generate per view per specimen",
        default=1,
        min=1
    )
