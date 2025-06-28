import bpy
from ..register_config import register
from ...helpers import get_property, set_property


@register("output")
class OutputConfig(bpy.types.PropertyGroup):
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