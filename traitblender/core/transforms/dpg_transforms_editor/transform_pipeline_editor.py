"""
Transform Pipeline Editor - Main Application
Standalone DearPyGUI app for editing transform pipelines.
"""

import dearpygui.dearpygui as dpg
from .transform_pipeline_manager import TransformPipelineManager
from .ui_manager import UIManager


class TransformPipelineEditor:
    """Main transform pipeline editor application that coordinates all managers."""
    
    def __init__(self):
        # Initialize managers
        self.transform_pipeline_manager = TransformPipelineManager()
        self.ui_manager = UIManager()
        
        # Export state
        self.export_requested = False
        self.final_yaml_data = None
    
    def load_pipeline_from_yaml(self, yaml_string):
        """Load pipeline data from YAML string (for Blender integration)"""
        success = self.transform_pipeline_manager.load_from_yaml(yaml_string)
        return success
    
    def create_gui(self):
        """Create the main GUI"""
        self.ui_manager.create_gui(self.transform_pipeline_manager)
    
    def run(self, window_title="Transform Pipeline Editor"):
        """Run the application"""
        self.create_gui()
        dpg.create_viewport(title=window_title, width=600, height=800)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)
        
        # If we have data loaded, update the display now that GUI is ready
        if self.transform_pipeline_manager.has_transforms():
            self.transform_pipeline_manager.update_display()
        
        dpg.start_dearpygui()
        
        # Store export state and YAML data before destroying context
        self.export_requested = self.get_export_state()
        self.final_yaml_data = self.transform_pipeline_manager.get_yaml_string()
        
        dpg.destroy_context()
    
    def get_export_state(self):
        """Get whether export changes is checked"""
        try:
            return dpg.get_value("export_changes_checkbox")
        except:
            return False
    
    def get_yaml_string(self):
        """Get current pipeline as YAML string (for Blender integration)"""
        return self.transform_pipeline_manager.get_yaml_string()


def launch_transform_pipeline_editor(yaml_string="", window_title="Transform Pipeline Editor"):
    """
    Launch the transform pipeline editor with pipeline data from a YAML string (for Blender integration)
    
    Args:
        yaml_string (str): Pipeline state as YAML string
        window_title (str): Title for the window
    
    Returns:
        str or None: YAML string if "Export Changes" is checked, None otherwise
    """
    try:
        # Create the editor instance
        app = TransformPipelineEditor()
        
        # Load pipeline data from YAML string (if provided)
        if yaml_string:
            success = app.load_pipeline_from_yaml(yaml_string)
            if not success:
                print("Failed to load pipeline data from YAML string")
        
        # Start the app with custom title
        app.run(window_title)
        
        # Check if export changes was requested (stored before context destruction)
        if hasattr(app, 'export_requested') and app.export_requested:
            return app.final_yaml_data
        else:
            return None
            
    except Exception as e:
        print(f"Error launching transform pipeline editor: {e}")
        import traceback
        traceback.print_exc()
        return None
