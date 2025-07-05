import bpy
from bpy.props import StringProperty
import pandas as pd
import os
from io import StringIO


def update_filepath(self, context):
    """Automatically import dataset when filepath changes"""
    if not self.filepath:
        # Clear CSV data if no file is selected
        self.csv = ""
        return
    
    # Check if file exists
    if not os.path.exists(self.filepath):
        print(f"TraitBlender: Dataset file not found: {self.filepath}")
        return
    
    # Infer file type from extension
    file_ext = os.path.splitext(self.filepath)[1].lower()
    
    # Check if extension is supported
    if file_ext not in ['.csv', '.tsv', '.xlsx', '.xls']:
        print(f"TraitBlender: Unsupported file type '{file_ext}'. Only CSV, TSV, and Excel files are supported.")
        return
    
    try:
        # Load the dataset based on the file extension
        if file_ext == '.csv':
            df = pd.read_csv(self.filepath)
        elif file_ext == '.tsv':
            df = pd.read_csv(self.filepath, sep='\t')
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(self.filepath)
        
        # Convert DataFrame to CSV string
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_string = csv_buffer.getvalue()
        
        # Store the CSV string in the dataset property
        self.csv = csv_string
        
        # Print success message
        rows, cols = df.shape
        print(f"TraitBlender: Dataset imported successfully: {rows} rows, {cols} columns")
        
    except Exception as e:
        # Print helpful error message based on file type
        if file_ext in ['.csv', '.tsv']:
            print(f"TraitBlender: Failed to import {file_ext.upper()} file. The file may not be properly formatted or may contain invalid data: {str(e)}")
        elif file_ext in ['.xlsx', '.xls']:
            print(f"TraitBlender: Failed to import Excel file. The file may be corrupted, password-protected, or contain invalid data: {str(e)}")
        else:
            print(f"TraitBlender: Failed to import dataset: {str(e)}")


class TRAITBLENDER_PG_dataset(bpy.types.PropertyGroup):
    """Property group for TraitBlender dataset management."""
    
    csv: StringProperty(
        name="CSV Data",
        description="CSV dataset content as string",
        default=""
    )
    
    filepath: StringProperty(
        name="Dataset File",
        description="Path to the dataset file (automatically imports when selected)",
        default="",
        subtype='FILE_PATH',
        update=update_filepath
    )
    
    def _get_dataframe(self):
        """Get DataFrame from CSV string"""
        if not self.csv:
            return pd.DataFrame()
        try:
            df = pd.read_csv(StringIO(self.csv))
            # Use the first column as the index
            if not df.empty and len(df.columns) > 0:
                df = df.set_index(df.columns[0])
            return df
        except Exception as e:
            print(f"TraitBlender: Error parsing CSV data: {e}")
            return pd.DataFrame()
    
    def __str__(self):
        """Return pretty formatted DataFrame"""
        df = self._get_dataframe()
        if df.empty:
            return "No dataset loaded"
        return str(df)
    
    def head(self, n=5):
        """Return first n rows of the dataset"""
        df = self._get_dataframe()
        return df.head(n)
    
    def tail(self, n=5):
        """Return last n rows of the dataset"""
        df = self._get_dataframe()
        return df.tail(n)
    
    @property
    def colnames(self):
        """Return column names"""
        df = self._get_dataframe()
        return df.columns.tolist()
    
    @property
    def rownames(self):
        """Return row names/indices"""
        df = self._get_dataframe()
        return df.index.tolist()
    
    def __iter__(self):
        """Iterate over column names"""
        df = self._get_dataframe()
        return iter(df.columns)
    
    def __len__(self):
        """Return number of rows in the dataset"""
        df = self._get_dataframe()
        return len(df)
    
    @property
    def shape(self):
        """Return shape of the dataset (rows, columns)"""
        df = self._get_dataframe()
        return df.shape
    
    def loc(self, *args, **kwargs):
        """Access a group of rows and columns by label(s) or a boolean array."""
        df = self._get_dataframe()
        if len(args) == 1:
            return df.loc[args[0]]
        elif len(args) == 2:
            return df.loc[args[0], args[1]]
        elif kwargs:
            return df.loc[kwargs]
        return df.loc
    
    def iloc(self, *args, **kwargs):
        """Purely integer-location based indexing for selection by position."""
        df = self._get_dataframe()
        if len(args) == 1:
            return df.iloc[args[0]]
        elif len(args) == 2:
            return df.iloc[args[0], args[1]]
        elif kwargs:
            return df.iloc[kwargs]
        return df.iloc 