import bpy
from ..register_config import register

@register("background")
class BackgroundConfig(bpy.types.PropertyGroup):
    background_color: bpy.props.FloatVectorProperty(
        name="Background Color",
        description="The color of the background",
        default=(0.0, 0.0, 0.0, 0.0),
        min=0.0,
        max=1.0,
        size=4,
        get=lambda self: bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value,
        set=lambda self, value: setattr(bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0], "default_value", value)
    )