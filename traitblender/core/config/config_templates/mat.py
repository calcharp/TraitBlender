import bpy
from ..register_config import register, TraitBlenderConfig
from ...helpers import get_property, set_property


@register("mat")
class MatConfig(TraitBlenderConfig):
    print_index = 4

    location: bpy.props.FloatVectorProperty(
        name="Material Location",
        description="The location of the material",
        subtype='TRANSLATION',
        get=get_property("bpy.data.objects['Mat'].location",
                        object_dependencies={"objects": ["Mat"]}),
        set=set_property("bpy.data.objects['Mat'].location",
                        object_dependencies={"objects": ["Mat"]})
    )

    rotation: bpy.props.FloatVectorProperty(
        name="Material Rotation",
        description="The rotation of the material",
        subtype='EULER',
        get=get_property("bpy.data.objects['Mat'].rotation_euler",
                        object_dependencies={"objects": ["Mat"]}),
        set=set_property("bpy.data.objects['Mat'].rotation_euler",
                        object_dependencies={"objects": ["Mat"]})
    )

    scale: bpy.props.FloatVectorProperty(
        name="Material Scale",
        description="The scale of the material",
        subtype='XYZ',
        get=get_property("bpy.data.objects['Mat'].scale",
                        object_dependencies={"objects": ["Mat"]}),
        set=set_property("bpy.data.objects['Mat'].scale",
                        object_dependencies={"objects": ["Mat"]})
    )

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
