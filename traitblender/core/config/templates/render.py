import bpy
from .. import config_subsection_register, TraitBlenderConfig
from ...helpers import get_property, set_property
from ...helpers.render_engine_compat import render_engine_enum_items, render_engine_options


_RENDER_ENGINE_OPTS = render_engine_options()
_RENDER_ENGINE_ITEMS = tuple(render_engine_enum_items())


@config_subsection_register("render")
class RenderConfig(TraitBlenderConfig):
    print_index = 5

    def from_dict(self, data_dict):
        if not isinstance(data_dict, dict):
            return
        from ...helpers.render_engine_compat import normalize_render_engine_value

        data = dict(data_dict)
        if "engine" in data:
            data["engine"] = normalize_render_engine_value(data["engine"])
        super().from_dict(data)

    engine: bpy.props.EnumProperty(
        name="Engine",
        description="The engine to use",
        items=_RENDER_ENGINE_ITEMS,
        get=get_property(
            "bpy.context.scene.render.engine",
            options=_RENDER_ENGINE_OPTS,
        ),
        set=set_property(
            "bpy.context.scene.render.engine",
            options=_RENDER_ENGINE_OPTS,
        ),
    )

    eevee_use_raytracing: bpy.props.BoolProperty(
        name="Use Raytracing",
        description="Whether to use raytracing",
        default=False,
        get=get_property("bpy.context.scene.eevee.use_raytracing"),
        set=set_property("bpy.context.scene.eevee.use_raytracing")
    )

