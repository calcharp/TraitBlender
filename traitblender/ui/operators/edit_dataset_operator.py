"""
TraitBlender Edit Dataset Operator

Operator for editing the dataset CSV data using the CSV editor GUI.
"""

import bpy
from bpy.types import Operator
from ...core.datasets.csv_editor import edit_table_string


class TRAITBLENDER_OT_edit_dataset(Operator):
    """Edit dataset using CSV editor"""
    
    bl_idname = "traitblender.edit_dataset"
    bl_label = "Edit Dataset"
    bl_description = "Open CSV editor to edit the dataset"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        """Execute the edit dataset operation"""
        dataset = context.scene.traitblender_dataset
        
        # Check if there's CSV data to edit
        if not dataset.csv:
            self.report({'WARNING'}, "No dataset loaded. Import a dataset first.")
            return {'CANCELLED'}
        
        try:
            # Call the CSV editor with the current CSV string
            result = edit_table_string(dataset.csv)
            
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