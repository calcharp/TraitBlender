"""
Scene properties for the current morphospace sample (e.g. shell mesh structure).

Stored on the scene so they stay out of the object's Item tab and are updated when a new sample is generated.
"""

import bpy
from bpy.props import IntProperty, PointerProperty


class TRAITBLENDER_PG_sample_props(bpy.types.PropertyGroup):
    """Per-sample mesh structure (set by morphospace on generate). Not shown in object UI."""

    raup_num_rings: IntProperty(
        name="Rings",
        description="Number of rings in the shell mesh (set by morphospace)",
        default=0,
        min=0,
    )
    raup_points_per_ring: IntProperty(
        name="Points per ring",
        description="Vertices per ring (set by morphospace)",
        default=0,
        min=0,
    )


class TRAITBLENDER_PG_sample(bpy.types.PropertyGroup):
    """Container for current sample metadata (props updated when a new sample is generated)."""

    props: PointerProperty(type=TRAITBLENDER_PG_sample_props)
