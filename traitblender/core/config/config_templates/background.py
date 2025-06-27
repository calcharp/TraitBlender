import bpy
from ..register_config import register
from ...helpers import get_property, set_property

@register("background")
class BackgroundConfig(bpy.types.PropertyGroup):
    color: bpy.props.FloatVectorProperty(
        name="Background Color",
        description="The color of the background",
        default=(0.0, 0.0, 0.0, 1.0),
        min=0.0,
        max=1.0,
        size=4,
        get=get_property('bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value'),
        set=set_property('bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value')
    )
    strength: bpy.props.FloatProperty(
        name="Strength",
        description="Strength of the emitted light.",
        default=1.0,
        min=0.0,
        get=get_property('bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value'),
        set=set_property('bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value')
    )