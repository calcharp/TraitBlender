"""
TraitBlender Import Dataset Operator

Operator for importing datasets from various formats (CSV, TSV, Excel) using pandas.
"""

import bpy
from bpy.types import Operator
import pandas as pd
import os
from io import StringIO


class TRAITBLENDER_OT_import_dataset(Operator):
    """Import dataset from file and convert to CSV string"""
    
    bl_idname = "traitblender.import_dataset"
    bl_label = "Import Dataset"
    bl_description = "Import dataset from CSV, TSV, or Excel file and store as CSV string"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        """Execute the import dataset operation"""
        dataset = context.scene.traitblender_dataset
        
        # Check if filepath is provided
        if not dataset.filepath:
            self.report({'ERROR'}, "No dataset file specified")
            return {'CANCELLED'}
        
        # Check if file exists
        if not os.path.exists(dataset.filepath):
            self.report({'ERROR'}, f"Dataset file not found: {dataset.filepath}")
            return {'CANCELLED'}
        
        # Infer file type from extension
        file_ext = os.path.splitext(dataset.filepath)[1].lower()
        
        # Check if extension is supported
        if file_ext not in ['.csv', '.tsv', '.xlsx', '.xls']:
            self.report({'ERROR'}, f"Unsupported file type '{file_ext}'. Only CSV, TSV, and Excel files are supported.")
            return {'CANCELLED'}
        
        try:
            # Load the dataset based on the file extension
            if file_ext == '.csv':
                df = pd.read_csv(dataset.filepath)
            elif file_ext == '.tsv':
                df = pd.read_csv(dataset.filepath, sep='\t')
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(dataset.filepath)
            
            # Convert DataFrame to CSV string
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_string = csv_buffer.getvalue()
            
            # Store the CSV string in the dataset property
            dataset.csv = csv_string
            
            # Report success
            rows, cols = df.shape
            self.report({'INFO'}, f"Dataset imported successfully: {rows} rows, {cols} columns")
            
        except Exception as e:
            # Provide helpful error message based on file type
            if file_ext in ['.csv', '.tsv']:
                self.report({'ERROR'}, f"Failed to import {file_ext.upper()} file. The file may not be properly formatted or may contain invalid data: {str(e)}")
            elif file_ext in ['.xlsx', '.xls']:
                self.report({'ERROR'}, f"Failed to import Excel file. The file may be corrupted, password-protected, or contain invalid data: {str(e)}")
            else:
                self.report({'ERROR'}, f"Failed to import dataset: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'} 