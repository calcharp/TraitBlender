"""
Main CSV viewer application.
Coordinates all managers and provides the main interface.
"""

import dearpygui.dearpygui as dpg
from .data_manager import DataManager
from .filter_manager import FilterManager
from .table_manager import TableManager
from .ui_manager import UIManager


class CSVViewer:
    """Main CSV viewer application that coordinates all managers."""
    
    def __init__(self):
        # Initialize managers
        self.data_manager = DataManager()
        self.table_manager = TableManager(self.data_manager)
        self.filter_manager = FilterManager(self.data_manager, self.table_manager)
        self.ui_manager = UIManager()
        
        # Export state
        self.export_requested = False
        self.final_csv_data = None
    
    def load_csv_from_string(self, csv_string):
        """Load CSV data from a string (for Blender integration)"""
        success = self.data_manager.load_csv_from_string(csv_string)
        
        if success:
            # Reset all managers' state (but not UI until GUI is created)
            self.table_manager.reset_pagination()
            self.table_manager.reset_sorting()
            # Don't call clear_filter_ui() here - it will be called after GUI creation
        
        return success
    
    def create_gui(self):
        """Create the main GUI"""
        self.ui_manager.create_gui(
            self.data_manager, 
            self.filter_manager, 
            self.table_manager
        )
        
    def run(self, window_title="CSV Viewer"):
        """Run the application"""
        self.create_gui()
        dpg.create_viewport(title=window_title, width=1000, height=700)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)
        
        # If we have data loaded, update the display now that GUI is ready
        if self.data_manager.df_display is not None:
            self.table_manager.update_display()
            self.filter_manager.clear_filter_ui()
        
        dpg.start_dearpygui()
        
        # Store export state and CSV data before destroying context
        self.export_requested = self.get_export_state()
        self.final_csv_data = self.data_manager.get_csv_string()
        
        dpg.destroy_context()
    
    def get_export_state(self):
        """Get whether export changes is checked"""
        try:
            return dpg.get_value("export_changes_checkbox")
        except:
            return False
    
    def get_csv_string(self):
        """Get current data as CSV string (for Blender integration)"""
        return self.data_manager.get_csv_string()


def launch_csv_viewer_with_string(csv_string, window_title="CSV Viewer"):
    """
    Launch the CSV viewer with data from a string (for Blender integration)
    
    Args:
        csv_string (str): CSV data as a string
        window_title (str): Title for the window
    
    Returns:
        str or None: CSV string if "Export Changes" is checked, None otherwise
    """
    try:
        # Create the viewer instance
        app = CSVViewer()
        
        # Load CSV data from string (without updating UI yet)
        success = app.load_csv_from_string(csv_string)
        
        if success:
            # Start the app with custom title - this will create GUI and then update it
            app.run(window_title)
            
            # Check if export changes was requested (stored before context destruction)
            if hasattr(app, 'export_requested') and app.export_requested:
                return app.final_csv_data
            else:
                return None
        else:
            print("Failed to load CSV data from string")
            return None
            
    except Exception as e:
        print(f"Error launching CSV viewer: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    app = CSVViewer()
    app.run()
