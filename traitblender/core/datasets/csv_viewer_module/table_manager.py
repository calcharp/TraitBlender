"""
Table management module for CSV viewer.
Handles table display, pagination, sorting, and row operations.
"""

import dearpygui.dearpygui as dpg
import pandas as pd


class TableManager:
    """Manages table display, pagination, sorting, and row operations."""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.current_page = 0
        self.rows_per_page = 100
        self.visible_rows = 15
        self.sort_column = None  # Currently sorted column index
        self.sort_ascending = True  # Sort direction
        self.selected_row_index = None  # Currently selected row for operations
    
    def update_display(self):
        """Update the table display with current page data"""
        if self.data_manager.df_display is None:
            return
        
        # Clear existing table
        if dpg.does_item_exist("data_table"):
            dpg.delete_item("data_table")
        
        # Calculate pagination
        total_rows = len(self.data_manager.df_display)
        total_pages = (total_rows + self.rows_per_page - 1) // self.rows_per_page
        start_row = self.current_page * self.rows_per_page
        end_row = min(start_row + self.rows_per_page, total_rows)
        
        # Create new table
        with dpg.table(tag="data_table", parent="content_area", 
                      header_row=False, resizable=True, policy=dpg.mvTable_SizingStretchProp,
                      height=self.visible_rows * 25 + 30):
            
            # Add row index column first (display only, no header)
            dpg.add_table_column(label="", width_fixed=True, init_width_or_weight=30)
            
            # Add data columns
            for col in self.data_manager.df_display.columns:
                dpg.add_table_column(label=col, width_fixed=False)
            
            # Add header row manually to control the row column header
            with dpg.table_row():
                # Empty cell for row column (just background)
                dpg.add_text("")
                
                # Add data column headers (clickable for sorting)
                for j, col in enumerate(self.data_manager.df_display.columns):
                    # Add sort indicator to button label
                    if self.sort_column == j:
                        indicator = " ^" if self.sort_ascending else " v"
                        button_label = col + indicator
                    else:
                        button_label = col
                    
                    dpg.add_button(
                        label=button_label,
                        width=-1,
                        callback=lambda s, a, u: self.sort_by_column(u),
                        user_data=j
                    )
            
            # Add data rows
            for i in range(start_row, end_row):
                with dpg.table_row():
                    # Add row index (1-based) with hover highlighting
                    row_index_button = dpg.add_button(
                        label=str(i + 1),
                        width=-1,
                        height=0,  # Auto height
                        callback=lambda s, a, u: self.show_row_operation_dialog(u),
                        user_data=i  # Pass the actual row index (0-based)
                    )
                    dpg.bind_item_theme(row_index_button, "row_index_theme")
                    
                    # Add data cells (editable)
                    for j, col in enumerate(self.data_manager.df_display.columns):
                        cell_tag = f"cell_{i}_{j}"
                        cell_value = self.data_manager.df_display.iloc[i, j]
                        
                        # Handle pandas NA values for display
                        if pd.isna(cell_value):
                            display_value = ""
                        else:
                            display_value = str(cell_value)
                        
                        dpg.add_input_text(
                            tag=cell_tag,
                            default_value=display_value,
                            width=-1,
                            callback=lambda s, a, u: self.update_cell_value(u[0], u[1], a)
                        )
                        # Store row and column info for the callback
                        dpg.set_item_user_data(cell_tag, (i, j))
        
        # Show pagination controls and update info
        dpg.show_item("pagination_controls")
        dpg.hide_item("placeholder_text")
        dpg.hide_item("default_table")  # Hide default table when CSV is loaded
        self.update_pagination_info(total_pages, start_row, end_row, total_rows)
    
    def update_pagination_info(self, total_pages, start_row, end_row, total_rows):
        """Update pagination information display"""
        if dpg.does_item_exist("pagination_info"):
            dpg.set_value("pagination_info", f"Page {self.current_page + 1} of {total_pages} | Rows {start_row + 1}-{end_row} of {total_rows} | Scroll to see more")
    
    def go_to_first_page(self):
        """Go to the first page"""
        if self.data_manager.df_display is not None and self.current_page > 0:
            self.current_page = 0
            self.update_display()
    
    def go_to_previous_page(self):
        """Go to the previous page"""
        if self.data_manager.df_display is not None and self.current_page > 0:
            self.current_page -= 1
            self.update_display()
    
    def go_to_next_page(self):
        """Go to the next page"""
        if self.data_manager.df_display is not None:
            total_pages = (len(self.data_manager.df_display) + self.rows_per_page - 1) // self.rows_per_page
            if self.current_page < total_pages - 1:
                self.current_page += 1
                self.update_display()
    
    def go_to_last_page(self):
        """Go to the last page"""
        if self.data_manager.df_display is not None:
            total_pages = (len(self.data_manager.df_display) + self.rows_per_page - 1) // self.rows_per_page
            self.current_page = total_pages - 1
            self.update_display()
    
    def sort_by_column(self, column_index):
        """Sort the dataframe by the specified column"""
        if self.data_manager.df_display is not None:
            column_name = self.data_manager.df_display.columns[column_index]
            
            # Toggle sort direction if clicking the same column
            if self.sort_column == column_index:
                self.sort_ascending = not self.sort_ascending
            else:
                self.sort_ascending = True
                self.sort_column = column_index
            
            # Sort the data using data manager
            success = self.data_manager.sort_data(column_name, self.sort_ascending)
            
            if success:
                # Reset to first page and update display
                self.current_page = 0
                self.update_display()
    
    def update_cell_value(self, row, col, new_value):
        """Update the dataframe when a cell value is changed"""
        success = self.data_manager.update_cell_value(row, col, new_value)
        
        if not success:
            # Invalid input - revert to original value
            original_value = str(self.data_manager.df_display.iloc[row, col])
            # Find the cell input and reset its value
            cell_tag = f"cell_{row}_{col}"
            if dpg.does_item_exist(cell_tag):
                dpg.set_value(cell_tag, original_value)
    
    def show_row_operation_dialog(self, row_index):
        """Show dialog for row operations (Delete/Insert)"""
        if self.data_manager.df_display is None:
            print("No data to operate on")
            return
        
        print(f"Showing row operation dialog for row {row_index + 1}")
        
        # Store the row index for the operation
        self.selected_row_index = row_index
        
        # Create the row operation dialog
        dpg.add_window(
            label="Row Operations", 
            modal=True, 
            width=300, 
            height=150, 
            tag="row_ops_dialog",
            show=True,
            pos=(400, 200)
        )
        dpg.add_text(f"Row {row_index + 1} selected", parent="row_ops_dialog")
        dpg.add_separator(parent="row_ops_dialog")
        dpg.add_spacer(height=10, parent="row_ops_dialog")
        
        # Delete button
        dpg.add_button(
            label="Delete Row",
            callback=self.delete_row_direct,
            width=-1,
            height=30,
            parent="row_ops_dialog"
        )
        dpg.add_spacer(height=5, parent="row_ops_dialog")
        
        # Insert button
        dpg.add_button(
            label="Insert Row",
            callback=lambda: self.insert_row_direct(above=True),
            width=-1,
            height=30,
            parent="row_ops_dialog"
        )
        dpg.add_spacer(height=5, parent="row_ops_dialog")
        
        # Cancel button
        dpg.add_button(
            label="Cancel",
            callback=lambda: dpg.delete_item("row_ops_dialog"),
            width=-1,
            height=30,
            parent="row_ops_dialog"
        )
    
    def delete_row_direct(self):
        """Delete row directly without confirmation dialog"""
        print("Delete row direct called")
        if self.data_manager.df_display is not None and self.selected_row_index is not None:
            print(f"Deleting row {self.selected_row_index + 1}")
            
            # Delete the row using data manager
            success = self.data_manager.delete_row(self.selected_row_index)
            
            if success:
                # Reset to first page and update display
                self.current_page = 0
                self.update_display()
                print(f"Successfully deleted row {self.selected_row_index + 1}")
            else:
                print("Failed to delete row")
        else:
            print("No data or selected row index not found")
        
        # Close the dialog
        dpg.delete_item("row_ops_dialog")
    
    def insert_row_direct(self, above=True):
        """Insert row directly with position choice"""
        print(f"Insert row direct called - above: {above}")
        if self.data_manager.df_display is not None and self.selected_row_index is not None:
            position = "above" if above else "below"
            print(f"Inserting row {position} row {self.selected_row_index + 1}")
            
            # Determine insertion position
            if above:
                insert_pos = self.selected_row_index
            else:
                insert_pos = self.selected_row_index + 1
            
            # Insert the row using data manager
            success = self.data_manager.add_row(insert_pos)
            
            if success:
                # Reset to first page and update display
                self.current_page = 0
                self.update_display()
                print(f"Successfully inserted new row {position} row {self.selected_row_index + 1}")
            else:
                print("Failed to insert row")
        else:
            print("No data or selected row index not found")
        
        # Close the dialog
        dpg.delete_item("row_ops_dialog")
    
    def update_default_cell_value(self, row, col, new_value):
        """Update the default table when a cell value is changed"""
        # This is just for the default table - no data storage needed
        pass
    
    def reset_pagination(self):
        """Reset pagination to first page"""
        self.current_page = 0
    
    def reset_sorting(self):
        """Reset sorting state"""
        self.sort_column = None
        self.sort_ascending = True
