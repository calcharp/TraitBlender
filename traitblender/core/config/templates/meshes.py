"""
Mesh export configuration.
"""

import bpy
from bpy.props import EnumProperty

from .. import config_subsection_register, TraitBlenderConfig
from ...meshes import export_type_items


@config_subsection_register("meshes")
class MeshesConfig(TraitBlenderConfig):
    """Configuration for mesh exports."""

    # Place after imaging/sample/transforms in YAML/UI ordering (not the panel ordering)
    print_index = 9

    file_export_type: EnumProperty(
        name="File Export Type",
        description="Mesh export file type for exporting the current sample",
        items=lambda self, context: export_type_items(),
        default=0,
    )

