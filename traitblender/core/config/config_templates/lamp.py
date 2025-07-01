import bpy
from ..register_config import register
from ...helpers import get_property, set_property


@register("lamp")
class LampConfig(bpy.types.PropertyGroup):

    location: bpy.props.FloatVectorProperty(
        name="Lamp Location",
        description="The location of the lamp",
        get=get_property("bpy.data.objects['Lamp'].location",
                        object_dependencies={"objects": ["Lamp"]}),
        set=set_property("bpy.data.objects['Lamp'].location",
                        object_dependencies={"objects": ["Lamp"]})
    )

    rotation: bpy.props.FloatVectorProperty(
        name="Lamp Rotation",
        description="The rotation of the lamp",
        get=get_property("bpy.data.objects['Lamp'].rotation_euler",
                        object_dependencies={"objects": ["Lamp"]}),
        set=set_property("bpy.data.objects['Lamp'].rotation_euler",
                        object_dependencies={"objects": ["Lamp"]})
    )

    scale: bpy.props.FloatVectorProperty(
        name="Lamp Scale",
        description="The scale of the lamp",
        get=get_property("bpy.data.objects['Lamp'].scale",
                        object_dependencies={"objects": ["Lamp"]}),
        set=set_property("bpy.data.objects['Lamp'].scale",
                        object_dependencies={"objects": ["Lamp"]})
    )

    color: bpy.props.FloatVectorProperty(
        name="Lamp Color",
        description="The color of the lamp",
        min=0.0,
        max=1.0,
        size=4,
        subtype='COLOR',
        get=get_property("bpy.data.lights['Spot'].color",
                        object_dependencies={"lights": ["Spot"]}),
        set=set_property("bpy.data.lights['Spot'].color",
                        object_dependencies={"lights": ["Spot"]})
    )
    power: bpy.props.FloatProperty(
        name="Lamp Power",
        description="The power of the lamp",
        min=0.0,
        get=get_property("bpy.data.lights['Spot'].energy",
                        object_dependencies={"lights": ["Spot"]}),
        set=set_property("bpy.data.lights['Spot'].energy",
                        object_dependencies={"lights": ["Spot"]})
    )

    use_soft_falloff: bpy.props.BoolProperty(
        name="Lamp Soft Falloff",
        description="Whether the lamp uses a soft falloff",
        get=get_property("bpy.data.lights['Spot'].use_soft_falloff",
                        object_dependencies={"lights": ["Spot"]}),
        set=set_property("bpy.data.lights['Spot'].use_soft_falloff",
                        object_dependencies={"lights": ["Spot"]})
    )

    beam_size: bpy.props.FloatProperty(
        name="Lamp Beam Size",
        description="The size of the lamp's beam",
        min=0.0,
        max=10.0,
        get=get_property("bpy.data.lights['Spot'].spot_size",
                        object_dependencies={"lights": ["Spot"]}),
        set=set_property("bpy.data.lights['Spot'].spot_size",
                        object_dependencies={"lights": ["Spot"]})
    )

    beam_blend: bpy.props.FloatProperty(
        name="Lamp Beam Blend",
        description="The blend of the lamp's beam",
        min=0.0,
        get=get_property("bpy.data.lights['Spot'].spot_blend",
                        object_dependencies={"lights": ["Spot"]}),  
        set=set_property("bpy.data.lights['Spot'].spot_blend",
                        object_dependencies={"lights": ["Spot"]})
    )

    shadow: bpy.props.BoolProperty(
        name="Lamp Shadow",
        description="Whether the lamp casts shadows",
        get=get_property("bpy.data.lights['Spot'].use_shadow",
                        object_dependencies={"lights": ["Spot"]}),
        set=set_property("bpy.data.lights['Spot'].use_shadow",
                        object_dependencies={"lights": ["Spot"]})
    )
    