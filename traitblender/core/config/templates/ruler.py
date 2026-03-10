import bpy
from .. import config_subsection_register, TraitBlenderConfig
from ...helpers import get_property, set_property


def _get_ruler_hide(self):
    obj = bpy.data.objects.get("Ruler")
    if obj is None:
        return False
    return obj.hide_viewport


def _set_ruler_hide(self, value):
    obj = bpy.data.objects.get("Ruler")
    if obj is not None:
        obj.hide_viewport = value
        obj.hide_render = value


@config_subsection_register("ruler")
class RulerConfig(TraitBlenderConfig):
    """Config for the Ruler object (tb_location, tb_rotation, hide)."""

    # Table coordinates in meters; default slightly in front of table center
    tb_location: bpy.props.FloatVectorProperty(
        name="Ruler Location",
        description="Ruler location relative to Table top center (meters)",
        subtype='TRANSLATION',
        size=3,
        default=(0.0, -0.1, 0.0),
        get=get_property(
            "bpy.data.objects['Ruler'].tb_location",
            object_dependencies={"objects": ["Ruler"]},
            default=(0.0, -0.1, 0.0),
        ),
        set=set_property("bpy.data.objects['Ruler'].tb_location", object_dependencies={"objects": ["Ruler"]}),
    )
    tb_rotation: bpy.props.FloatVectorProperty(
        name="Ruler Rotation",
        description="Ruler rotation (Euler)",
        subtype='EULER',
        default=(0.0, 0.0, 0.0),
        get=get_property(
            "bpy.data.objects['Ruler'].tb_rotation",
            object_dependencies={"objects": ["Ruler"]},
            default=(0.0, 0.0, 0.0),
        ),
        set=set_property("bpy.data.objects['Ruler'].tb_rotation", object_dependencies={"objects": ["Ruler"]}),
    )
    hide: bpy.props.BoolProperty(
        name="Hide Ruler",
        description="Hide the Ruler in the viewport and in renders",
        default=False,
        get=_get_ruler_hide,
        set=_set_ruler_hide,
    )
