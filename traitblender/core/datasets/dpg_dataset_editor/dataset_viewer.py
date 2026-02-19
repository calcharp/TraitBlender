"""
Main dataset viewer application.
Coordinates all managers and provides the main interface.
"""

import dearpygui.dearpygui as dpg
from .dataset_handler import DatasetHandler
from .filter_ui_manager import FilterUIManager
from .table_ui_manager import TableUIManager
from .app_ui_manager import AppUIManager


class DatasetViewer:
    """Main dataset viewer application that coordinates all managers."""

    def __init__(self):
        # Initialize managers
        self.dataset_handler = DatasetHandler()
        self.table_ui_manager = TableUIManager(self.dataset_handler)
        self.filter_ui_manager = FilterUIManager(self.dataset_handler, self.table_ui_manager)
        self.app_ui_manager = AppUIManager()

        # Export state
        self.export_requested = False
        self.final_csv_data = None

    def load_csv_from_string(self, csv_string):
        """Load CSV data from a string (for Blender integration)"""
        success = self.dataset_handler.load_csv_from_string(csv_string)

        if success:
            # Reset all managers' state (but not UI until GUI is created)
            self.table_ui_manager.reset_pagination()
            self.table_ui_manager.reset_sorting()
            # Don't call clear_filter_ui() here - it will be called after GUI creation

        return success

    def create_gui(self):
        """Create the main GUI"""
        self.app_ui_manager.create_gui(
            self.dataset_handler,
            self.filter_ui_manager,
            self.table_ui_manager
        )

    def run(self, window_title="Dataset Viewer"):
        """Run the application"""
        self.create_gui()
        dpg.create_viewport(title=window_title, width=1000, height=700)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)

        # If we have data loaded, update the display now that GUI is ready
        if self.dataset_handler.df_display is not None:
            self.table_ui_manager.update_display()
            self.filter_ui_manager.clear_filter_ui()

        dpg.start_dearpygui()

        # Store export state and CSV data before destroying context
        self.export_requested = self.get_export_state()
        self.final_csv_data = self.dataset_handler.get_csv_string()

        dpg.destroy_context()

    def get_export_state(self):
        """Get whether export changes is checked"""
        try:
            return dpg.get_value("export_changes_checkbox")
        except:
            return False

    def get_csv_string(self):
        """Get current data as CSV string (for Blender integration)"""
        return self.dataset_handler.get_csv_string()


def launch_dataset_viewer_with_string(csv_string, window_title="Dataset Viewer"):
    """
    Launch the dataset viewer with data from a string (for Blender integration)

    Args:
        csv_string (str): CSV data as a string
        window_title (str): Title for the window

    Returns:
        str or None: CSV string if "Export Changes" is checked, None otherwise
    """
    try:
        # Create the viewer instance
        app = DatasetViewer()

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
        print(f"Error launching dataset viewer: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    app = DatasetViewer()
    app.run()
