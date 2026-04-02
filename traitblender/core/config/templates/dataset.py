"""
Dataset configuration.

This section intentionally stores only the dataset filepath (not the dataset contents)
so configs can be shared/reproduced while the dataset itself remains a separate file.
"""

import bpy
import warnings

from .. import config_subsection_register, TraitBlenderConfig
from ...helpers import get_property, set_property


@config_subsection_register("dataset")
class DatasetConfig(TraitBlenderConfig):
    """Configuration for selecting the external dataset CSV/TSV/Excel file."""

    print_index = -2  # show near the start of exported configs

    filepath: bpy.props.StringProperty(
        name="Dataset File",
        description=(
            "Path to a CSV/TSV/XLSX dataset file. "
            "When set, TraitBlender will import it and use its rows as simulated specimens. "
            "If the file can't be read or doesn't match the active morphospace columns, "
            "TraitBlender will warn and fall back to the morphospace default dataset."
        ),
        default="",
        subtype="FILE_PATH",
        get=get_property("bpy.context.scene.traitblender_dataset.filepath", object_dependencies=None, default=""),
        set=set_property("bpy.context.scene.traitblender_dataset.filepath", object_dependencies=None),
    )

