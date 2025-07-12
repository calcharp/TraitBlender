import bpy
from ..register_config import register, TraitBlenderConfig
from ...helpers import get_property, set_property

@register("lamp")
class LampConfig(TraitBlenderConfig):
    print_index = 3

    # Table coordinates in meters
    location: bpy.props.FloatVectorProperty(
        name="Lamp Location (Relative to Table Surface)",
        description="Lamp location in table coordinates (origin at table top center, Z is table normal) in meters",
        default=(0.0, 0.0, 0.0),
        subtype='TRANSLATION',
            get=get_property("bpy.data.objects['Lamp'].location", object_dependencies={"objects": ["Lamp"]}),
    set=set_property("bpy.data.objects['Lamp'].location", object_dependencies={"objects": ["Lamp"]})
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
        default=(1.0, 1.0, 1.0),
        min=0.0,
        max=1.0,
        size=3,
        subtype='COLOR',
        get=get_property('bpy.data.lights["Lamp"].color',
                        object_dependencies={"lights": ["Lamp"]}),
        set=set_property('bpy.data.lights["Lamp"].color',
                        object_dependencies={"lights": ["Lamp"]})
    )

    power: bpy.props.FloatProperty(
        name="Lamp Power",
        description="The power of the lamp",
        min=0.0,
        get=get_property("bpy.data.lights['Lamp'].energy",
                        object_dependencies={"lights": ["Lamp"]}),
        set=set_property("bpy.data.lights['Lamp'].energy",
                        object_dependencies={"lights": ["Lamp"]})
    )

    use_soft_falloff: bpy.props.BoolProperty(
        name="Lamp Soft Falloff",
        description="Whether the lamp uses a soft falloff",
        get=get_property("bpy.data.lights['Lamp'].use_soft_falloff",
                        object_dependencies={"lights": ["Lamp"]}),
        set=set_property("bpy.data.lights['Lamp'].use_soft_falloff",
                        object_dependencies={"lights": ["Lamp"]})
    )

    beam_size: bpy.props.FloatProperty(
        name="Lamp Beam Size",
        description="The size of the lamp's beam",
        min=0.0,
        max=10.0,
        get=get_property("bpy.data.lights['Lamp'].spot_size",
                        object_dependencies={"lights": ["Lamp"]}),
        set=set_property("bpy.data.lights['Lamp'].spot_size",
                        object_dependencies={"lights": ["Lamp"]})
    )

    beam_blend: bpy.props.FloatProperty(
        name="Lamp Beam Blend",
        description="The blend of the lamp's beam",
        min=0.0,
        get=get_property("bpy.data.lights['Lamp'].spot_blend",
                        object_dependencies={"lights": ["Lamp"]}),  
        set=set_property("bpy.data.lights['Lamp'].spot_blend",
                        object_dependencies={"lights": ["Lamp"]})
    )

    shadow: bpy.props.BoolProperty(
        name="Lamp Shadow",
        description="Whether the lamp casts shadows",
        get=get_property("bpy.data.lights['Lamp'].use_shadow",
                        object_dependencies={"lights": ["Lamp"]}),
        set=set_property("bpy.data.lights['Lamp'].use_shadow",
                        object_dependencies={"lights": ["Lamp"]})
    )

    diffuse: bpy.props.FloatProperty(
        name="Lamp Diffuse",
        description="The diffuse of the lamp",
        min=0.0,
        get=get_property("bpy.data.lights['Lamp'].diffuse_factor",
                        object_dependencies={"lights": ["Lamp"]}),
        set=set_property("bpy.data.lights['Lamp'].diffuse_factor",
                        object_dependencies={"lights": ["Lamp"]})
    )


    