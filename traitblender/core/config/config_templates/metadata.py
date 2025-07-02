import bpy
from ..register_config import register, TraitBlenderConfig
from ...helpers import get_property, set_property


@register("metadata")
class MetadataConfig(TraitBlenderConfig):
    print_index = 7

    use_stamp_date: bpy.props.BoolProperty(
        name="Use Stamp Data",
        description="Whether to use stamp data",
        get=get_property("bpy.context.scene.render.use_stamp_date"),
        set=set_property("bpy.context.scene.render.use_stamp_date")
    )

    use_stamp_time: bpy.props.BoolProperty(
        name="Use Stamp Time",
        description="Whether to use stamp time",
        get=get_property("bpy.context.scene.render.use_stamp_time"),
        set=set_property("bpy.context.scene.render.use_stamp_time")
    )

    use_stamp_render_time: bpy.props.BoolProperty(
        name="Use Stamp Render Time",
        description="Whether to use stamp render time",
        get=get_property("bpy.context.scene.render.use_stamp_render_time"),
        set=set_property("bpy.context.scene.render.use_stamp_render_time")
    )

    use_stamp_frame: bpy.props.BoolProperty(
        name="Use Stamp Frame",
        description="Whether to use stamp frame",
        get=get_property("bpy.context.scene.render.use_stamp_frame"),
        set=set_property("bpy.context.scene.render.use_stamp_frame")
    )

    use_stamp_frame_range: bpy.props.BoolProperty(
        name="Use Stamp Frame Range",
        description="Whether to use stamp frame range",
        get=get_property("bpy.context.scene.render.use_stamp_frame_range"),
        set=set_property("bpy.context.scene.render.use_stamp_frame_range")
    )

    use_stamp_memory: bpy.props.BoolProperty(
        name="Use Stamp Memory",
        description="Whether to use stamp memory",
        get=get_property("bpy.context.scene.render.use_stamp_memory"),
        set=set_property("bpy.context.scene.render.use_stamp_memory")
    )

    use_stamp_hostname: bpy.props.BoolProperty(
        name="Use Stamp Hostname",
        description="Whether to use stamp hostname",
        get=get_property("bpy.context.scene.render.use_stamp_hostname"),
        set=set_property("bpy.context.scene.render.use_stamp_hostname")
    )

    use_stamp_camera: bpy.props.BoolProperty(
        name="Use Stamp Camera",
        description="Whether to use stamp camera",
        get=get_property("bpy.context.scene.render.use_stamp_camera"),
        set=set_property("bpy.context.scene.render.use_stamp_camera")
    )

    use_stamp_lens: bpy.props.BoolProperty(
        name="Use Stamp Lens",
        description="Whether to use stamp lens",
        get=get_property("bpy.context.scene.render.use_stamp_lens"),
        set=set_property("bpy.context.scene.render.use_stamp_lens")
    )

    use_stamp_scene: bpy.props.BoolProperty(
        name="Use Stamp Scene",
        description="Whether to use stamp scene",
        get=get_property("bpy.context.scene.render.use_stamp_scene"),
        set=set_property("bpy.context.scene.render.use_stamp_scene")
    )

    use_stamp_marker: bpy.props.BoolProperty(
        name="Use Stamp Marker",
        description="Whether to use stamp marker",
        get=get_property("bpy.context.scene.render.use_stamp_marker"),
        set=set_property("bpy.context.scene.render.use_stamp_marker")
    )

    use_stamp_filename: bpy.props.BoolProperty(
        name="Use Stamp Filename",
        description="Whether to use stamp filename",
        get=get_property("bpy.context.scene.render.use_stamp_filename"),
        set=set_property("bpy.context.scene.render.use_stamp_filename")
    )

    use_stamp_sequencer_strip: bpy.props.BoolProperty(
        name="Use Stamp Sequencer Strip",
        description="Whether to use stamp sequencer strip",
        get=get_property("bpy.context.scene.render.use_stamp_sequencer_strip"),
        set=set_property("bpy.context.scene.render.use_stamp_sequencer_strip")
    )

    use_stamp_note: bpy.props.BoolProperty(
        name="Use Stamp Note",
        description="Whether to use stamp note",
        get=get_property("bpy.context.scene.render.use_stamp_note"),
        set=set_property("bpy.context.scene.render.use_stamp_note")
    )

    stamp_note_text: bpy.props.StringProperty(
        name="Stamp Note Text",
        description="The text of the stamp note",
        default="",
        get=get_property("bpy.context.scene.render.stamp_note_text"),
        set=set_property("bpy.context.scene.render.stamp_note_text")
    )

    