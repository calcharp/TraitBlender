"""
TraitBlender Export Dataset Operator

Exports the current dataset to a CSV file via Blender's file selector.
"""

import os
import bpy
from bpy.types import Operator
from bpy.props import StringProperty


class TRAITBLENDER_OT_export_dataset(Operator):
    """Export current dataset as CSV"""

    bl_idname = "traitblender.export_dataset"
    bl_label = "Export Dataset"
    bl_description = "Export the current dataset to a CSV file"

    filepath: StringProperty(
        name="File Path",
        description="Path to export CSV",
        subtype='FILE_PATH',
        default="dataset.csv",
    )

    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
    )

    def invoke(self, context, event):
        # Provide a sensible default filename
        if not self.filepath:
            self.filepath = "dataset.csv"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        dataset = context.scene.traitblender_dataset

        csv_string = dataset.csv
        if not csv_string:
            # Fall back to default dataset CSV (for current morphospace) when nothing imported/edited yet
            csv_string = dataset.get_csv_for_editing()

        if not csv_string:
            self.report({'WARNING'}, "No dataset to export.")
            return {'CANCELLED'}

        path = self.filepath
        if not path.lower().endswith(".csv"):
            path = path + ".csv"

        try:
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(csv_string)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export dataset: {e}")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Dataset exported: {path}")
        return {'FINISHED'}

