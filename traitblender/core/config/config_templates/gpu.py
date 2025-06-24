import bpy
from ..register_config import register

@register("gpu")
class GPUConfig(bpy.types.PropertyGroup):
    gpu_type: bpy.props.EnumProperty(
        name="GPU Type",
        description="The type of GPU to use",
        items=[("cpu", "CPU", "A CPU GPU"),
               ("gpu", "GPU", "A GPU")],
        default="gpu"
    )
