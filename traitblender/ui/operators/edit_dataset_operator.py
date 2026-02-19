"""
TraitBlender Edit Dataset Operator

Operator for editing the dataset CSV data using the CSV editor GUI.
"""

import bpy
from bpy.types import Operator
from ...core.datasets.dpg_dataset_editor import launch_csv_viewer_with_string

class TRAITBLENDER_OT_edit_dataset(Operator):
    """Edit dataset using CSV editor"""
    
    bl_idname = "traitblender.edit_dataset"
    bl_label = "Edit Dataset"
    bl_description = "Open CSV editor to edit the dataset"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        """Execute the edit dataset operation"""
        dataset = context.scene.traitblender_dataset
        
        # Get CSV to edit (uses default virtual dataset when no file imported)
        csv_to_edit = dataset.get_csv_for_editing()
        if not csv_to_edit:
            self.report({'WARNING'}, "No dataset loaded. Import a dataset first.")
            return {'CANCELLED'}
        
        try:
            # Call the CSV viewer with the CSV string (real or default)
            result = launch_csv_viewer_with_string(csv_to_edit, "Edit Dataset")
            print(f"CSV Viewer result: {result}")
            
            # If result is not None, update the dataset
            if result is not None:
                dataset.csv = result
                self.report({'INFO'}, "Dataset updated successfully")
            else:
                # User cancelled or chose not to save
                self.report({'INFO'}, "Dataset edit cancelled")
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to edit dataset: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'} 