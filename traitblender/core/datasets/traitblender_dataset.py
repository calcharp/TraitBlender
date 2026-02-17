import bpy
from bpy.props import StringProperty, EnumProperty
import pandas as pd
import os
from io import StringIO
from ..morphospaces import get_trait_parameters_with_defaults_for_morphospace


def update_csv(self, context):
    """Reset sample selection when CSV data changes"""
    # Reset sample to first item when CSV changes
    if hasattr(self, 'sample'):
        try:
            # Get the current sample items to see what's available
            items = self._get_sample_items()
            if items and len(items) > 0:
                # Set to the first available item
                self.sample = items[0][0]  # Use the identifier (first element of tuple)
            else:
                self.sample = 0
        except Exception as e:
            print(f"TraitBlender: Error updating sample selection: {e}")
            self.sample = 0

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
        
        # Apply column reordering (same logic as _get_dataframe)
        if not df.empty and len(df.columns) > 0:
            # Define possible species/label column names (case-insensitive)
            species_column_names = ['species', 'label', 'tips', 'tip', 'sample', 'samples', 'name', 'names', 'id', 'ids']
            
            # Check if first column is already a species column
            first_col_lower = df.columns[0].lower().strip()
            if first_col_lower not in species_column_names:
                # Look for species columns in the dataset
                species_columns = []
                for col in df.columns:
                    col_lower = col.lower().strip()
                    if col_lower in species_column_names:
                        species_columns.append(col)
                
                if species_columns:
                    # Sort alphabetically and pick the first one
                    species_columns.sort()
                    species_col = species_columns[0]
                    
                    # Move the species column to the first position
                    cols = list(df.columns)
                    species_idx = cols.index(species_col)
                    
                    # Reorder columns: species column first, then the rest
                    new_cols = [species_col] + [col for i, col in enumerate(cols) if i != species_idx]
                    df = df[new_cols]
                    
                    print(f"TraitBlender: Moved '{species_col}' column to first position for species identification")
        
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
        default="",
        update=update_csv
    )
    
    filepath: StringProperty(
        name="Dataset File",
        description="Path to the dataset file (automatically imports when selected)",
        default="",
        subtype='FILE_PATH',
        update=update_filepath
    )
    
    sample: EnumProperty(
        name="Sample",
        description="Select a sample from the dataset",
        items=lambda self, context: self._get_sample_items(),
        default=0
    )
    
    def _get_sample_items(self):
        """Get sample items for the enum property (includes default 't1' when no file imported)."""
        try:
            rownames = self.rownames
            if not rownames:
                return [("NONE", "No samples", "")]
            
            # Create items with proper tuple format
            items = []
            for i, name in enumerate(rownames):
                items.append((name, name, f"Sample {i+1}"))
            
            return items
        except Exception as e:
            print(f"TraitBlender: Error getting sample items: {e}")
            return [("NONE", "No samples", "")]
    
    def _get_default_dataframe(self):
        """Get default DataFrame when no file imported: one row 't1' with trait columns from active morphospace."""
        try:
            morphospace_name = bpy.context.scene.traitblender_setup.available_morphospaces
        except Exception:
            morphospace_name = ""
        traits = get_trait_parameters_with_defaults_for_morphospace(morphospace_name)
        columns = ["species"] + list(traits.keys())
        default_values = list(traits.values())
        df = pd.DataFrame([["t1"] + default_values], columns=columns)
        return df.set_index("species")

    def get_csv_for_editing(self):
        """Return CSV string for the editor: from csv property, or serialized default when no file imported."""
        if self.csv:
            return self.csv
        if not self.filepath:
            df = self._get_default_dataframe()
            # Reset index so species is a column, then export as CSV
            csv_buffer = StringIO()
            df.reset_index().to_csv(csv_buffer, index=False)
            return csv_buffer.getvalue()
        return ""

    def _get_dataframe(self):
        """Get DataFrame from CSV string, or default (one row 't1') when no file imported."""
        if not self.csv and not self.filepath:
            return self._get_default_dataframe()
        if not self.csv:
            return pd.DataFrame()
        try:
            df = pd.read_csv(StringIO(self.csv))
            if df.empty or len(df.columns) == 0:
                return df
            
            # Define possible species/label column names (case-insensitive)
            species_column_names = ['species', 'label', 'tips', 'tip', 'sample', 'samples', 'name', 'names', 'id', 'ids']
            
            # Check if first column is already a species column
            first_col_lower = df.columns[0].lower().strip()
            if first_col_lower in species_column_names:
                # First column is already a species column, use it as index
                df = df.set_index(df.columns[0])
                return df
            
            # Look for species columns in the dataset
            species_columns = []
            for col in df.columns:
                col_lower = col.lower().strip()
                if col_lower in species_column_names:
                    species_columns.append(col)
            
            if species_columns:
                # Sort alphabetically and pick the first one
                species_columns.sort()
                species_col = species_columns[0]
                
                # Move the species column to the first position
                cols = list(df.columns)
                species_idx = cols.index(species_col)
                
                # Reorder columns: species column first, then the rest
                new_cols = [species_col] + [col for i, col in enumerate(cols) if i != species_idx]
                df = df[new_cols]
                
                print(f"TraitBlender: Moved '{species_col}' column to first position for species identification")
            
            # Use the first column as the index
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