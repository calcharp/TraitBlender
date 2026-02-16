import bpy
from ..register_config import register, TraitBlenderConfig
from ...morphospaces import get_orientations_for_morphospace


@register("orientations")
class OrientationsConfig(TraitBlenderConfig):
    """Orientation functions provided by the selected morphospace."""

    print_index = 1

    orientation: bpy.props.EnumProperty(
        name="Orientation",
        description="Orientation function to apply to the specimen (defined by the morphospace)",
        items=lambda self, context: self._get_orientation_items(context),
        default=0
    )

    def _get_orientation_items(self, context):
        """Get orientation options from the selected morphospace's ORIENTATIONS dict."""
        items = []
        try:
            setup = context.scene.traitblender_setup
            morphospace_name = setup.available_morphospaces
            orientations = get_orientations_for_morphospace(morphospace_name)
            for name, func in orientations.items():
                if callable(func):
                    items.append((name, name, f"Apply {name} orientation"))
            if not items:
                items = [("", "—", "No orientations defined")]
        except Exception as e:
            print(f"TraitBlender: Error getting orientation items: {e}")
            items = items or [("", "—", "No orientations defined")]
        return items
