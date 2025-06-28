import bpy
from ..register_config import register
from ...helpers import get_property, set_property


@register("render")
class RenderConfig(bpy.types.PropertyGroup):
    
    engine: bpy.props.EnumProperty(
        name="Engine",
        description="The engine to use",    
        items=[("CYCLES", "Cycles", "Cycles"),
               ("BLENDER_EEVEE", "Eevee", "Eevee")],
        default=0,
        get=get_property("bpy.data.scenes['Scene'].render.engine"),
        set=set_property("bpy.data.scenes['Scene'].render.engine")
    )

    eevee_use_raytracing: bpy.props.BoolProperty(
        name="Use Raytracing",
        description="Whether to use raytracing",
        default=False,
        get=get_property("bpy.data.scenes['Scene'].render.eevee.use_raytracing"),
        set=set_property("bpy.data.scenes['Scene'].render.eevee.use_raytracing")
    )

    eevee_use_denoising: bpy.props.BoolProperty(
        name="Use Denoising",
        description="Whether to use denoising",
        default=False,
        get=get_property("bpy.data.scenes['Scene'].render.eevee.use_denoising"),
        set=set_property("bpy.data.scenes['Scene'].render.eevee.use_denoising")
    )

    cycles_device: bpy.props.EnumProperty(
        name="Device",
        description="The device to use",
        items=[("CPU", "CPU", "CPU"),
               ("GPU", "GPU", "GPU")],
        default=0,
        get=get_property("bpy.data.scenes['Scene'].cycles.device"),
        set=set_property("bpy.data.scenes['Scene'].cycles.device")
    )

    cycles_shading_system: bpy.props.EnumProperty(
        name="Shading System",
        description="The shading system to use",
        items=[("B", "B", "B"),
               ("C", "C", "C")],
        default=0,
        get=get_property("bpy.data.scenes['Scene'].cycles.shading_system"),
        set=set_property("bpy.data.scenes['Scene'].cycles.shading_system")
    )
    
    
