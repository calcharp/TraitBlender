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

    resolution_x: bpy.props.IntProperty(
        name="Resolution X",
        description="The resolution of the render",
        get=get_property("bpy.context.scene.render.resolution_x"),
        set=set_property("bpy.context.scene.render.resolution_x")
    )
    
    resolution_y: bpy.props.IntProperty(
        name="Resolution Y",
        description="The resolution of the render",
        get=get_property("bpy.context.scene.render.resolution_y"),
        set=set_property("bpy.context.scene.render.resolution_y")
    )

    resolution_percentage: bpy.props.IntProperty(
        name="Resolution Percentage",
        description="The resolution of the render",
        get=get_property("bpy.context.scene.render.resolution_percentage"),
        set=set_property("bpy.context.scene.render.resolution_percentage")
    )

    aspect_x: bpy.props.IntProperty(
        name="Aspect X",
        description="The aspect of the render",
        get=get_property("bpy.context.scene.render.pixel_aspect_x"),
        set=set_property("bpy.context.scene.render.pixel_aspect_x")
    )

    aspect_y: bpy.props.IntProperty(
        name="Aspect Y",
        description="The aspect of the render",
        get=get_property("bpy.context.scene.render.pixel_aspect_y"),
        set=set_property("bpy.context.scene.render.pixel_aspect_y")
    )
