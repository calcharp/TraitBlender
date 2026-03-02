"""
Scene properties for the current morphospace sample (e.g. shell mesh structure).

Stored on the scene so they stay out of the object's Item tab and are updated when a new sample is generated.
"""

import bpy
from bpy.props import FloatVectorProperty, IntProperty, PointerProperty


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

    # Rest state (updated when a new sample is created); used to reset before applying an orientation.
    rest_origin: FloatVectorProperty(
        name="Rest origin",
        description="World position of the sample origin when the sample was created",
        size=3,
        subtype='TRANSLATION',
        default=(0.0, 0.0, 0.0),
    )
    rest_rotation: FloatVectorProperty(
        name="Rest rotation",
        description="Rotation of the sample when it was created (Euler)",
        size=3,
        subtype='EULER',
        default=(0.0, 0.0, 0.0),
    )
    last_baked_rotation: FloatVectorProperty(
        name="Last baked rotation",
        description="Rotation that was last baked into the mesh (so it can be undone when resetting)",
        size=3,
        subtype='EULER',
        default=(0.0, 0.0, 0.0),
    )
