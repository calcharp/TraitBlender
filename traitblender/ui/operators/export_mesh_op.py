"""
TraitBlender Export Mesh Operator

Wraps `TraitBlender.core.meshes.export_current_sample` with a file picker.
"""

import bpy
from bpy.types import Operator
from bpy.props import StringProperty

from ...core.meshes import export_current_sample


class TRAITBLENDER_OT_export_mesh(Operator):
    """Export current sample as a 3D mesh file"""

    bl_idname = "traitblender.export_mesh"
    bl_label = "Export Mesh"
    bl_description = "Export the current sample mesh to a file"

    filepath: StringProperty(
        name="File Path",
        description="Path to export mesh",
        subtype='FILE_PATH',
        default="",
    )

    filter_glob: StringProperty(
        default="*.obj",
        options={'HIDDEN'},
    )

    def invoke(self, context, event):
        # Default filename: {sample name}.{file type}
        sample_name = getattr(context.scene.traitblender_dataset, "sample", "") or "sample"
        if sample_name == "NONE" or not sample_name:
            sample_name = "sample"
        etype = getattr(context.scene.traitblender_config.meshes, "file_export_type", "obj") or "obj"
        self.filter_glob = f"*.{etype}"
        self.filepath = f"{sample_name}.{etype}"
        if getattr(bpy.app, "background", False):
            return self.execute(context)
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        try:
            export_current_sample(filepath=self.filepath, context=context)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export mesh: {e}")
            return {'CANCELLED'}
        return {'FINISHED'}

