import bpy
from ..register_config import register
from ...helpers import get_property, set_property


@register("render")
class RenderConfig(bpy.types.PropertyGroup):
    
    engine: bpy.props.EnumProperty(
        name="Engine",
        description="The engine to use",    
        items=[("CYCLES", "Cycles", "Cycles"),
               ("BLENDER_EEVEE_NEXT", "Eevee", "Eevee"),
               ("BLENDER_WORKBENCH", "Workbench", "Workbench")],
        get=get_property("bpy.context.scene.render.engine", options=["CYCLES", "BLENDER_EEVEE_NEXT", "BLENDER_WORKBENCH"]),
        set=set_property("bpy.context.scene.render.engine", options=["CYCLES", "BLENDER_EEVEE_NEXT", "BLENDER_WORKBENCH"])
    )

    eevee_use_raytracing: bpy.props.BoolProperty(
        name="Use Raytracing",
        description="Whether to use raytracing",
        default=False,
        get=get_property("bpy.context.scene.eevee.use_raytracing"),
        set=set_property("bpy.context.scene.eevee.use_raytracing")
    )

