import bpy
from ..register_config import register, TraitBlenderConfig
from ...helpers import get_property, set_property
@register("mat")
class MatConfig(TraitBlenderConfig):
    print_index = 4

    # Table coordinates in meters
    location: bpy.props.FloatVectorProperty(
        name="Mat Location (Relative to Table Surface)",
        description="Mat location in table coordinates (origin at table top center, Z is table normal) in meters",
        subtype='TRANSLATION',
        size=3,
            get=get_property("bpy.data.objects['Mat'].location", object_dependencies={"objects": ["Mat"]}),
    set=set_property("bpy.data.objects['Mat'].location", object_dependencies={"objects": ["Mat"]})
    )
    rotation: bpy.props.FloatVectorProperty(
        name="Mat Rotation",
        description="The rotation of the Mat",
        subtype='EULER',
        get=get_property("bpy.data.objects['Mat'].rotation_euler",
                        object_dependencies={"objects": ["Mat"]}),
        set=set_property("bpy.data.objects['Mat'].rotation_euler",
                        object_dependencies={"objects": ["Mat"]})
    )
    scale: bpy.props.FloatVectorProperty(
        name="Mat Scale",
        description="The scale of the Mat",
        subtype='XYZ',
        get=get_property("bpy.data.objects['Mat'].scale",
                        object_dependencies={"objects": ["Mat"]}),
        set=set_property("bpy.data.objects['Mat'].scale",
                        object_dependencies={"objects": ["Mat"]})
    )
    color: bpy.props.FloatVectorProperty(
        name="Mat Color",
        description="The color of the Mat",
        default=(0.0, 0.0, 0.0, 1.0),
        min=0.0,
        max=1.0,
        size=4,
        subtype='COLOR',
        get=get_property("bpy.data.materials['mat_material'].node_tree.nodes['Principled BSDF'].inputs[0].default_value",
                        object_dependencies={"objects": ["Mat"],
                                             "materials": ["mat_material"]}),
        set=set_property("bpy.data.materials['mat_material'].node_tree.nodes['Principled BSDF'].inputs[0].default_value",
                        object_dependencies={"objects": ["Mat"],
                                             "materials": ["mat_material"]})
    )
    roughness: bpy.props.FloatProperty(
        name="Mat Roughness",
        description="The roughness of the Mat",
        default=1.0,
        min=0.0,
        max=1.0,
        get=get_property("bpy.data.materials['mat_material'].node_tree.nodes['Principled BSDF'].inputs[2].default_value",
                        object_dependencies={"objects": ["Mat"],
                                             "materials": ["mat_material"]}),
        set=set_property("bpy.data.materials['mat_material'].node_tree.nodes['Principled BSDF'].inputs[2].default_value",
                        object_dependencies={"objects": ["Mat"],
                                             "materials": ["mat_material"]})
    )
