"""
Filter UI manager for DPG dataset editor.
Handles filtering logic, UI creation, and filter operations.
"""

import dearpygui.dearpygui as dpg
import pandas as pd


class FilterUIManager:
    """Manages filter UI and operations for the dataset editor."""

    def __init__(self, dataset_handler, table_ui_manager=None):
        self.dataset_handler = dataset_handler
        self.table_ui_manager = table_ui_manager
        self.filter_rows = []  # List of filter row data
        self.next_filter_id = 1  # Counter for unique filter row IDs
    
    def clear_filter_ui(self):
        """Clear all filter UI elements"""
        # Reset filter data
        self.filter_rows = []
        self.next_filter_id = 1
        
        # Clear only the filter rows container, don't rebuild the entire UI
        if dpg.does_item_exist("filter_rows_container"):
            dpg.delete_item("filter_rows_container")
        
        # Recreate the filter rows container
        dpg.add_child_window(tag="filter_rows_container", width=-1, height=200, no_scrollbar=False, parent="sidebar")
        
        # Add one empty filter row
        self.add_filter_row()
    
    def add_filter_row(self, update_dropdowns=True):
        """Add a new filter row"""
        print(f"Adding new filter row. Current count: {len(self.filter_rows)}")
        filter_id = self.next_filter_id
        self.next_filter_id += 1
        
        # Store filter row data
        filter_data = {
            'id': filter_id,
            'column_combo_tag': f"filter_column_{filter_id}",
            'filter_type_tag': f"filter_type_{filter_id}",
            'filter_controls_tag': f"filter_controls_{filter_id}",
            'text_input_tag': f"filter_text_{filter_id}",
            'operator_tag': f"filter_operator_{filter_id}",
            'value_input_tag': f"filter_value_{filter_id}",
            'boolean_value_tag': f"filter_boolean_{filter_id}",
            'regex_checkbox_tag': f"filter_regex_{filter_id}",
            'filter_type': 'Text'  # Default to Text
        }
        self.filter_rows.append(filter_data)
        
        # Create UI elements for this filter row
        dpg.add_text(f"Filter {len(self.filter_rows)}:", parent="filter_rows_container")
        
        # Column selection
        dpg.add_combo(
            items=[],
            tag=filter_data['column_combo_tag'],
            width=-1,
            default_value="Select column...",
            parent="filter_rows_container",
            callback=lambda s, a, u: self.on_column_selected(u),
            user_data=filter_id
        )
        
        # Filter type selection (Text/Numeric) - will be updated based on column selection
        dpg.add_combo(
            items=["Text"],  # Default to Text, will be updated when column is selected
            tag=filter_data['filter_type_tag'],
            width=-1,
            default_value="Text",
            parent="filter_rows_container",
            callback=lambda s, a, u: self.on_filter_type_changed(u),
            user_data=filter_id
        )
        
        # Filter controls container (will be populated based on type)
        dpg.add_child_window(
            tag=filter_data['filter_controls_tag'],
            width=-1,
            height=60,
            no_scrollbar=True,
            parent="filter_rows_container"
        )
        
        # Remove button (only for non-first rows)
        if len(self.filter_rows) > 1:  # Not the first row
            dpg.add_button(label="Remove", callback=lambda s, a, u: self.remove_filter_row(u), 
                         user_data=filter_id, width=60, parent="filter_rows_container")
        
        dpg.add_separator(parent="filter_rows_container")
        dpg.add_spacer(height=5, parent="filter_rows_container")
        
        # Update column dropdowns only if requested
        if update_dropdowns:
            self.update_filter_dropdown()
        
        # Create initial filter controls
        self.update_filter_controls(filter_data)
    
    def remove_filter_row(self, filter_id):
        """Remove a filter row"""
        if len(self.filter_rows) <= 1:
            print("Cannot remove the last filter row")
            return
        
        # Find and remove the filter data
        self.filter_rows = [row for row in self.filter_rows if row['id'] != filter_id]
        
        # Rebuild the entire filter UI
        self.rebuild_filter_ui()
    
    def rebuild_filter_ui(self):
        """Rebuild the entire filter UI"""
        # Clear the container
        if dpg.does_item_exist("filter_rows_container"):
            dpg.delete_item("filter_rows_container")
        
        # Recreate the container
        dpg.add_child_window(tag="filter_rows_container", width=-1, height=200, 
                           no_scrollbar=False, parent="sidebar")
        
        # Rebuild all existing filter rows without adding new ones
        for i, row in enumerate(self.filter_rows):
            self.recreate_filter_row(row, i + 1)
        
        # Update dropdowns once at the end
        self.update_filter_dropdown()
    
    def recreate_filter_row(self, row_data, filter_number):
        """Recreate a filter row UI without adding to the list"""
        # Create UI elements for this filter row
        dpg.add_text(f"Filter {filter_number}:", parent="filter_rows_container")
        
        # Column selection
        dpg.add_combo(
            items=[],
            tag=row_data['column_combo_tag'],
            width=-1,
            default_value="Select column...",
            parent="filter_rows_container",
            callback=lambda s, a, u: self.on_column_selected(u),
            user_data=row_data['id']
        )
        
        # Filter type selection (Text/Numeric) - will be updated based on column selection
        dpg.add_combo(
            items=["Text"],  # Default to Text, will be updated when column is selected
            tag=row_data['filter_type_tag'],
            width=-1,
            default_value=row_data.get('filter_type', 'Text'),
            parent="filter_rows_container",
            callback=lambda s, a, u: self.on_filter_type_changed(u),
            user_data=row_data['id']
        )
        
        # Filter controls container (will be populated based on type)
        dpg.add_child_window(
            tag=row_data['filter_controls_tag'],
            width=-1,
            height=60,
            no_scrollbar=True,
            parent="filter_rows_container"
        )
        
        # Remove button (only for non-first rows)
        if len(self.filter_rows) > 1:  # Not the first row
            dpg.add_button(label="Remove", callback=lambda s, a, u: self.remove_filter_row(u), 
                         user_data=row_data['id'], width=60, parent="filter_rows_container")
        
        dpg.add_separator(parent="filter_rows_container")
        dpg.add_spacer(height=5, parent="filter_rows_container")
        
        # Create initial filter controls
        self.update_filter_controls(row_data)
    
    def update_filter_dropdown(self):
        """Update all filter column dropdowns with current dataframe columns"""
        if self.dataset_handler.df_display is not None:
            column_names = list(self.dataset_handler.df_display.columns)
            # Update all filter row dropdowns
            for row in self.filter_rows:
                if dpg.does_item_exist(row['column_combo_tag']):
                    dpg.configure_item(row['column_combo_tag'], items=column_names)
        else:
            # Clear all filter row dropdowns
            for row in self.filter_rows:
                if dpg.does_item_exist(row['column_combo_tag']):
                    dpg.configure_item(row['column_combo_tag'], items=[])
    
    def on_column_selected(self, filter_id):
        """Handle column selection and auto-detect filter type"""
        # Find the filter row data
        filter_data = None
        for row in self.filter_rows:
            if row['id'] == filter_id:
                filter_data = row
                break
        
        if not filter_data:
            return
        
        # Get selected column
        selected_column = dpg.get_value(filter_data['column_combo_tag'])
        
        if not selected_column or selected_column == "Select column...":
            return
        
        # Check if we have data loaded
        if self.dataset_handler.df_display is None:
            dpg.set_value(filter_data['filter_type_tag'], "Text")
            filter_data['filter_type'] = "Text"
            self.update_filter_controls(filter_data)
            return
        
        # Auto-detect column type and set filter type
        if selected_column in self.dataset_handler.df_display.columns:
            column_dtype = self.dataset_handler.df_display[selected_column].dtype
            if column_dtype in ['int64', 'float64']:
                # Numeric column - can use both Text and Numeric filtering
                dpg.configure_item(filter_data['filter_type_tag'], items=["Text", "Numeric"])
                dpg.set_value(filter_data['filter_type_tag'], "Numeric")  # Default to Numeric for numeric columns
                filter_data['filter_type'] = "Numeric"
            elif column_dtype == 'bool':
                # Boolean column - only show Boolean option
                dpg.configure_item(filter_data['filter_type_tag'], items=["Boolean"])
                dpg.set_value(filter_data['filter_type_tag'], "Boolean")
                filter_data['filter_type'] = "Boolean"
            else:
                # Text column - only show Text option
                dpg.configure_item(filter_data['filter_type_tag'], items=["Text"])
                dpg.set_value(filter_data['filter_type_tag'], "Text")
                filter_data['filter_type'] = "Text"
        else:
            # Default to Text
            dpg.configure_item(filter_data['filter_type_tag'], items=["Text"])
            dpg.set_value(filter_data['filter_type_tag'], "Text")
            filter_data['filter_type'] = "Text"
        
        # Update filter controls
        self.update_filter_controls(filter_data)
    
    def on_filter_type_changed(self, filter_id):
        """Handle filter type change"""
        # Find the filter row data
        filter_data = None
        for row in self.filter_rows:
            if row['id'] == filter_id:
                filter_data = row
                break
        
        if not filter_data:
            return
        
        # Store the new filter type
        new_filter_type = dpg.get_value(filter_data['filter_type_tag'])
        filter_data['filter_type'] = new_filter_type
        
        # Update filter controls
        self.update_filter_controls(filter_data)
    
    def update_filter_controls(self, filter_data):
        """Update the filter controls based on selected type"""
        # Clear existing controls by deleting all children
        if dpg.does_item_exist(filter_data['filter_controls_tag']):
            # Get all children and delete them
            children = dpg.get_item_children(filter_data['filter_controls_tag'], 1)
            if children:
                for child in children:
                    dpg.delete_item(child)
        else:
            # Create controls container if it doesn't exist
            dpg.add_child_window(
                tag=filter_data['filter_controls_tag'],
                width=-1,
                height=60,
                no_scrollbar=True,
                parent="filter_rows_container"
            )
        
        # Get filter type from stored data or UI
        filter_type = filter_data.get('filter_type', dpg.get_value(filter_data['filter_type_tag']))
        
        if filter_type == "Numeric":
            # Numeric filter: operator + value input
            dpg.add_combo(
                items=["=", "!=", ">", ">=", "<", "<="],
                tag=filter_data['operator_tag'],
                width=60,
                default_value="=",
                parent=filter_data['filter_controls_tag'],
                pos=(10, 10)
            )
            dpg.add_input_text(
                tag=filter_data['value_input_tag'],
                width=120,
                hint="Enter numeric value...",
                parent=filter_data['filter_controls_tag'],
                pos=(80, 10),
                callback=lambda s, a, u: self.validate_numeric_input(u)
            )
        elif filter_type == "Boolean":
            # Boolean filter: True/False dropdown
            dpg.add_combo(
                items=["True", "False"],
                tag=filter_data['boolean_value_tag'],
                width=-1,
                default_value="True",
                parent=filter_data['filter_controls_tag'],
                pos=(10, 10)
            )
        else:
            # Text filter: text input + regex checkbox
            dpg.add_input_text(
                tag=filter_data['text_input_tag'],
                width=-1,
                hint="Enter text to filter by...",
                parent=filter_data['filter_controls_tag'],
                pos=(10, 10)
            )
            # Add regex checkbox underneath the text input
            dpg.add_checkbox(
                label="Regex", 
                tag=filter_data['regex_checkbox_tag'], 
                default_value=False, 
                parent=filter_data['filter_controls_tag'],
                pos=(10, 35)
            )
    
    def validate_numeric_input(self, input_tag):
        """Validate that numeric input contains only valid numbers"""
        value = dpg.get_value(input_tag)
        
        # Handle None or empty input
        if value is None or not value.strip():
            return
        
        # Check if it's a valid number (including negative and decimal)
        try:
            float(value)
        except ValueError:
            # Invalid input - revert to previous valid value
            # For now, just clear the invalid input
            dpg.set_value(input_tag, "")
            print("Invalid numeric input. Please enter a valid number.")
    
    def apply_filter(self):
        """Apply all current filters to the dataframe"""
        if self.dataset_handler.df_display is None:
            print("No data to filter")
            return
        
        # Collect all active filter conditions
        filter_conditions = []
        
        for row in self.filter_rows:
            # Get filter parameters for this row
            filter_column = dpg.get_value(row['column_combo_tag'])
            filter_type = dpg.get_value(row['filter_type_tag'])
            
            # Skip empty filters
            if not filter_column or filter_column == "Select column...":
                continue
            
            if filter_type == "Numeric":
                # Numeric filter
                operator = dpg.get_value(row['operator_tag'])
                value_text = dpg.get_value(row['value_input_tag'])
                
                if not value_text.strip():
                    continue
                
                try:
                    value = float(value_text)
                    filter_conditions.append({
                        'column': filter_column,
                        'type': 'numeric',
                        'operator': operator,
                        'value': value
                    })
                except ValueError:
                    print(f"Invalid numeric value: {value_text}")
                    continue
            elif filter_type == "Boolean":
                # Boolean filter
                boolean_value = dpg.get_value(row['boolean_value_tag'])
                
                if not boolean_value:
                    continue
                
                # Convert string to boolean
                bool_val = boolean_value == "True"
                
                filter_conditions.append({
                    'column': filter_column,
                    'type': 'boolean',
                    'value': bool_val
                })
            else:
                # Text filter - get individual regex setting
                use_regex = dpg.get_value(row['regex_checkbox_tag'])
                filter_text = dpg.get_value(row['text_input_tag'])
                
                if not filter_text.strip():
                    continue
                
                filter_conditions.append({
                    'column': filter_column,
                    'type': 'text',
                    'text': filter_text,
                    'regex': use_regex
                })
        
        if not filter_conditions:
            print("No active filters to apply")
            return
        
        # Apply filter to original data (not the already filtered data)
        base_data = self.dataset_handler.df_original.copy()
        
        try:
            # Start with all rows (True mask)
            combined_mask = pd.Series([True] * len(base_data), index=base_data.index)
            
            # Apply each filter condition (AND logic)
            for condition in filter_conditions:
                column = condition['column']
                
                if condition['type'] == 'numeric':
                    # Numeric filter
                    operator = condition['operator']
                    value = condition['value']
                    
                    # Create mask for numeric comparison
                    if operator == "=":
                        condition_mask = base_data[column] == value
                    elif operator == "!=":
                        condition_mask = base_data[column] != value
                    elif operator == ">":
                        condition_mask = base_data[column] > value
                    elif operator == ">=":
                        condition_mask = base_data[column] >= value
                    elif operator == "<":
                        condition_mask = base_data[column] < value
                    elif operator == "<=":
                        condition_mask = base_data[column] <= value
                    else:
                        continue  # Skip invalid operator
                    
                    # Handle NaN values (treat as False)
                    condition_mask = condition_mask.fillna(False)
                    
                elif condition['type'] == 'boolean':
                    # Boolean filter
                    value = condition['value']
                    
                    # Create mask for boolean comparison
                    condition_mask = base_data[column] == value
                    
                    # Handle NaN values (treat as False)
                    condition_mask = condition_mask.fillna(False)
                    
                else:
                    # Text filter
                    text = condition['text']
                    use_regex = condition['regex']
                    
                    # Create mask for this condition
                    if use_regex:
                        # Use regex matching
                        condition_mask = base_data[column].astype(str).str.contains(
                            text, 
                            case=False, 
                            na=False,
                            regex=True
                        )
                    else:
                        # Use regular string matching
                        condition_mask = base_data[column].astype(str).str.contains(
                            text, 
                            case=False, 
                            na=False,
                            regex=False
                        )
                
                # Combine with existing mask (AND logic)
                combined_mask = combined_mask & condition_mask
            
            # Apply the combined filter
            self.dataset_handler.df_display = base_data[combined_mask].reset_index(drop=True)
            
            # Update the table display if table manager is available
            if self.table_ui_manager:
                self.table_ui_manager.reset_pagination()
                self.table_ui_manager.update_display()
            
            print(f"Applied {len(filter_conditions)} filter(s): {len(self.dataset_handler.df_display)} rows match")
            
        except Exception as e:
            print(f"Error applying filters: {str(e)}")
            print("Check your regex patterns and filter text")
    
    def clear_filter(self):
        """Clear all filters but keep data changes"""
        if self.dataset_handler.df_display is not None:
            # Reset display to show all data (preserving any changes made)
            self.dataset_handler.df_display = self.dataset_handler.df_original.copy()
            
            # Update the table display if table manager is available
            if self.table_ui_manager:
                self.table_ui_manager.reset_pagination()
                self.table_ui_manager.update_display()
            
            print("Filters cleared")
        else:
            print("No data to clear filters from")
