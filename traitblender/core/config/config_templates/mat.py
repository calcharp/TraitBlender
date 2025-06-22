import bpy
from ..register_config import register

@register("mat")
class MatConfig(bpy.types.PropertyGroup):
    mat_type: bpy.props.EnumProperty(
        name="Material Type",
        description="The type of material to use",
        items=[("standard", "Standard", "A standard material"),
               ("principled", "Principled", "A principled material")],
        default="standard"
    )
