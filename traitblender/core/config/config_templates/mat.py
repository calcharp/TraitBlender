import bpy
from ..register_config import register
from ...helpers import get_property, set_property


@register("mat")
class MatConfig(bpy.types.PropertyGroup):
    color: bpy.props.FloatVectorProperty(
        name="Material Color",
        description="The color of the material",
        default=(0.0, 0.0, 0.0, 1.0),
        min=0.0,
        max=1.0,
        size=4,
        subtype='COLOR',
        get=get_property("bpy.data.materials['mat_material'].node_tree.nodes['Principled BSDF'].inputs[0].default_value",
                        object_dependencies={"materials": ["mat_material"]}),
        set=set_property("bpy.data.materials['mat_material'].node_tree.nodes['Principled BSDF'].inputs[0].default_value",
                        object_dependencies={"materials": ["mat_material"]})
    )
