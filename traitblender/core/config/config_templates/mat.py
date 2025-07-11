import bpy
from ..register_config import register, TraitBlenderConfig
from ...helpers import get_property, set_property
@register("mat")
class MatConfig(TraitBlenderConfig):
    print_index = 4

    location: bpy.props.FloatVectorProperty(
        name="Mat Location",
        description="The location of the Mat",
        subtype='TRANSLATION',
        get=get_property("bpy.data.objects['Mat'].location",
                        object_dependencies={"objects": ["Mat"]}),
        set=set_property("bpy.data.objects['Mat'].location",
                        object_dependencies={"objects": ["Mat"]})
    )
    # Normalized table coordinates (clamped with min/max)
    location_table: bpy.props.FloatVectorProperty(
        name="Mat Location (Table-Normalized)",
        description="Mat location in normalized table coordinates (-1 to 1 on X/Y, always Z=0)",
        subtype='TRANSLATION',
        size=3,
        get=get_property("bpy.data.objects['Mat'].table_coords_norm", object_dependencies={"objects": ["Mat", "Table"]}),
        set=set_property("bpy.data.objects['Mat'].table_coords_norm", object_dependencies={"objects": ["Mat", "Table"]})
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
        get=get_property("bpy.data.Mats['mat_material'].node_tree.nodes['Principled BSDF'].inputs[0].default_value",
                        object_dependencies={"Mats": ["mat_material"]}),
        set=set_property("bpy.data.Mats['mat_material'].node_tree.nodes['Principled BSDF'].inputs[0].default_value",
                        object_dependencies={"Mats": ["mat_material"]})
    )
    roughness: bpy.props.FloatProperty(
        name="Mat Roughness",
        description="The roughness of the Mat",
        default=1.0,
        min=0.0,
        max=1.0,
        get=get_property("bpy.data.Mats['mat_material'].node_tree.nodes['Principled BSDF'].inputs[2].default_value",
                        object_dependencies={"Mats": ["mat_Mat"]}),
        set=set_property("bpy.data.Mats['mat_material'].node_tree.nodes['Principled BSDF'].inputs[2].default_value",
                        object_dependencies={"Mats": ["mat_material"]})
    )
