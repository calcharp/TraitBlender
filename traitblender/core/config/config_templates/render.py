import bpy
from ..register_config import register

@register("render")
class RenderConfig(bpy.types.PropertyGroup):
    
    engine: bpy.props.EnumProperty(
        name="Engine",
        description="The engine to use",    
        items=[("CYCLES", "Cycles", "Cycles"),
               ("BLENDER_EEVEE", "Eevee", "Eevee")],
        default="CYCLES"
    )

    samples: bpy.props.IntProperty(
        name="Samples",
        description="The number of samples to use",
        default=16,
        min=1,
        max=1024
    )

    eevee_use_raytracing: bpy.props.BoolProperty(
        name="Use Raytracing",
        description="Whether to use raytracing",
        default=False
    )

    eevee_use_denoising: bpy.props.BoolProperty(
        name="Use Denoising",
        description="Whether to use denoising",
        default=False       
    )

    eevee_use_fast_gi: bpy.props.BoolProperty(
        name="Use Fast GI",
        description="Whether to use fast GI",
        default=False
    )

    cycles_device: bpy.props.EnumProperty(
        name="Device",
        description="The device to use",
        items=[("CPU", "CPU", "CPU"),
               ("GPU", "GPU", "GPU")],
        default="CPU"
    )

    cycless_shading_system: bpy.props.EnumProperty(
        name="Shading System",
        description="The shading system to use",
        items=[("B", "B", "B"),
               ("C", "C", "C")],
        default="B"
    )
    
    
