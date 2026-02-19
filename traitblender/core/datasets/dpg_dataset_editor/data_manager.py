"""
Data management module for CSV viewer.
Handles CSV data loading, validation, and manipulation.
"""

import pandas as pd
from io import StringIO


class DataManager:
    """Manages CSV data loading, validation, and manipulation."""
    
    def __init__(self):
        self.df_original = None  # Unaltered CSV data
        self.df_display = None   # Filtered/sorted data for display
    
    def load_csv_from_string(self, csv_string):
        """Load CSV data from a string (for Blender integration)"""
        try:
            # Use StringIO to read CSV string as if it were a file
            csv_buffer = StringIO(csv_string)
            self.df_original = pd.read_csv(csv_buffer)
            self.df_display = self.df_original.copy()
            
            print(f"Loaded CSV from string")
            print(f"Shape: {self.df_original.shape}")
            return True
            
        except Exception as e:
            print(f"Error loading CSV from string: {e}")
            return False
    
    def save_changes(self):
        """Save current display state as the new original"""
        if self.df_display is not None:
            self.df_original = self.df_display.copy()
            print("Changes saved - current state is now the original")
        else:
            print("No data to save")
    
    def reset_to_original(self):
        """Reset display to the original/last saved state"""
        if self.df_original is not None:
            self.df_display = self.df_original.copy()
            print("Reset to original data")
        else:
            print("No original data to reset to")
    
    def get_csv_string(self):
        """Get current data as CSV string (for Blender integration)"""
        if self.df_display is None:
            return ""
        
        try:
            # Convert DataFrame to CSV string
            csv_string = self.df_display.to_csv(index=False)
            return csv_string
        except Exception as e:
            print(f"Error converting to CSV string: {e}")
            return ""
    
    def update_cell_value(self, row, col, new_value):
        """Update the dataframe when a cell value is changed"""
        if self.df_display is None:
            return False
        
        col_name = self.df_display.columns[col]
        column_dtype = self.df_display.dtypes.iloc[col]
        
        # Check if the input can be coerced to the column's data type
        if not self._is_valid_input_for_dtype(new_value, column_dtype):
            return False
        
        # Input is valid - proceed with update
        try:
            # Check if this is an NA value
            na_values = ['na', 'NA', 'n/a', 'N/A', '-', 'nan', 'NaN', 'null', 'NULL']
            is_na = not new_value or new_value.strip() == "" or new_value.strip().lower() in [v.lower() for v in na_values]
            
            if is_na:
                # Set to pandas NA to preserve data type
                self.df_display.iloc[row, col] = pd.NA
            elif column_dtype in ['int64', 'float64']:
                # Numeric columns
                self.df_display.iloc[row, col] = float(new_value)
            else:
                # String columns
                self.df_display.iloc[row, col] = str(new_value)
            
            return True
        except (ValueError, TypeError):
            return False
    
    def _is_valid_input_for_dtype(self, value, dtype):
        """Check if input value can be coerced to the given pandas dtype"""
        if not value or value.strip() == "":
            return True  # Empty values are allowed
        
        # Check for NA values (case insensitive)
        na_values = ['na', 'NA', 'n/a', 'N/A', '-', 'nan', 'NaN', 'null', 'NULL']
        if value.strip().lower() in [v.lower() for v in na_values]:
            return True  # NA values are allowed
        
        try:
            if dtype in ['int64', 'float64']:
                # For numeric columns, try to convert to float
                float(value)
                return True
            elif dtype == 'object':
                # String columns accept any input
                return True
            else:
                # For other dtypes, try to convert using pandas
                pd.Series([value]).astype(dtype)
                return True
        except (ValueError, TypeError, OverflowError):
            return False
    
    def add_row(self, above_index=None):
        """Add a new row to the dataframe"""
        if self.df_display is None:
            return False
        
        # Create a new row with default values
        new_row = {}
        for col in self.df_display.columns:
            if self.df_display[col].dtype in ['int64', 'float64']:
                new_row[col] = 0.0  # Default numeric value
            else:
                new_row[col] = ""  # Default string value
        
        # Convert to DataFrame
        new_row_df = pd.DataFrame([new_row])
        
        # Determine insertion position
        if above_index is not None:
            insert_pos = above_index
        else:
            insert_pos = len(self.df_display)
        
        # Insert the row
        self.df_display = pd.concat([
            self.df_display.iloc[:insert_pos],
            new_row_df,
            self.df_display.iloc[insert_pos:]
        ]).reset_index(drop=True)
        
        return True

    def copy_row(self, source_row_index, above_index=None):
        """Add a new row by copying values from an existing row."""
        if self.df_display is None or source_row_index >= len(self.df_display):
            return False

        new_row = self.df_display.iloc[source_row_index].to_dict()
        new_row_df = pd.DataFrame([new_row])

        if above_index is not None:
            insert_pos = above_index
        else:
            insert_pos = len(self.df_display)

        self.df_display = pd.concat([
            self.df_display.iloc[:insert_pos],
            new_row_df,
            self.df_display.iloc[insert_pos:]
        ]).reset_index(drop=True)

        return True

    def delete_row(self, row_index):
        """Delete a row from the dataframe"""
        if self.df_display is None or row_index >= len(self.df_display):
            return False
        
        # Delete the row from the dataframe
        self.df_display = self.df_display.drop(self.df_display.index[row_index]).reset_index(drop=True)
        return True
    
    def sort_data(self, column_name, ascending=True):
        """Sort the dataframe by the specified column"""
        if self.df_display is None:
            return False
        
        try:
            # Sort the dataframe with stable sort for deterministic behavior
            self.df_display = self.df_display.sort_values(
                by=column_name, 
                ascending=ascending,
                kind='mergesort'  # Stable sort algorithm
            ).reset_index(drop=True)
            return True
        except Exception as e:
            print(f"Error sorting data: {e}")
            return False
