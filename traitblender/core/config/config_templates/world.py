import bpy
from ..register_config import register, TraitBlenderConfig
from ...helpers import get_property, set_property

@register("world")
class WorldConfig(TraitBlenderConfig):
    print_index = 1
    
    color: bpy.props.FloatVectorProperty(
        name="World Color",
        description="The color of the world",
        default=(0.0, 0.0, 0.0, 1.0),
        min=0.0,
        max=1.0,
        size=4,
        subtype='COLOR',
        get=get_property('bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value',
                        object_dependencies={"worlds": ["World"]}),
        set=set_property('bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value',
                        object_dependencies={"worlds": ["World"]})
    )
    strength: bpy.props.FloatProperty(
        name="Strength",
        description="Strength of the emitted light.",
        default=1.0,
        min=0.0,
        get=get_property('bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value',
                        object_dependencies={"worlds": ["World"]}),
        set=set_property('bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value',
                        object_dependencies={"worlds": ["World"]})
    )