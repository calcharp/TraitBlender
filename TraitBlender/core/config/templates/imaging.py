"""
Imaging pipeline configuration: selected orientations and images per orientation.
"""

import bpy
from bpy.props import BoolProperty, CollectionProperty, IntProperty, StringProperty

from .. import config_subsection_register, TraitBlenderConfig


class ImagingOrientationItem(bpy.types.PropertyGroup):
    """One orientation option for the imaging pipeline (name + enabled checkbox)."""

    name: StringProperty(name="Orientation", default="")
    enabled: BoolProperty(name="Include", description="Include this orientation in the imaging pipeline", default=True)


# Register so ImagingConfig can use CollectionProperty(type=ImagingOrientationItem)
bpy.utils.register_class(ImagingOrientationItem)


@config_subsection_register("imaging")
class ImagingConfig(TraitBlenderConfig):
    """Which orientations to run in the imaging pipeline and how many images per orientation."""

    print_index = 7

    orientation_options: CollectionProperty(
        type=ImagingOrientationItem,
        name="Orientations",
        description="Orientations from the selected morphospace; checked = include in pipeline",
    )
    images_per_orientation: IntProperty(
        name="Images Per Orientation",
        description="Number of images to render per orientation (transforms applied each time)",
        default=1,
        min=1,
    )

    def _to_yaml(self, indent_level=0, parent_path=""):
        """Export imaging section; orientation_options as orientation_names list."""
        indent = "  " * (indent_level + 1)
        names = [item.name for item in self.orientation_options if item.enabled]
        safe = [repr(n) for n in names]
        lines = [f'{indent}orientation_names: [{", ".join(safe)}]', f"{indent}images_per_orientation: {self.images_per_orientation}"]
        return "\n".join(lines)

    def from_dict(self, data_dict):
        """Load imaging section; restore orientation_options from orientation_names list."""
        if not isinstance(data_dict, dict):
            raise ValueError("Input must be a dictionary")
        if "images_per_orientation" in data_dict:
            self.images_per_orientation = data_dict["images_per_orientation"]
        if "orientation_names" in data_dict:
            names = data_dict["orientation_names"]
            if isinstance(names, list):
                self.orientation_options.clear()
                for n in names:
                    if isinstance(n, str):
                        item = self.orientation_options.add()
                        item.name = n
                        item.enabled = True
