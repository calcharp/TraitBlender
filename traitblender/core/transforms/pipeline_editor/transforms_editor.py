"""
Transform Pipeline Editor - Main Application
Standalone DearPyGUI app for editing transform pipelines.
"""

import dearpygui.dearpygui as dpg
from .transforms_manager import TransformsManager
from .ui_manager import UIManager


class TransformEditor:
    """Main transform editor application that coordinates all managers."""
    
    def __init__(self):
        # Initialize managers
        self.transforms_manager = TransformsManager()
        self.ui_manager = UIManager()
        
        # Export state
        self.export_requested = False
        self.final_yaml_data = None
    
    def load_pipeline_from_yaml(self, yaml_string):
        """Load pipeline data from YAML string (for Blender integration)"""
        success = self.transforms_manager.load_from_yaml(yaml_string)
        return success
    
    def create_gui(self):
        """Create the main GUI"""
        self.ui_manager.create_gui(self.transforms_manager)
    
    def run(self, window_title="Transform Pipeline Editor"):
        """Run the application"""
        self.create_gui()
        dpg.create_viewport(title=window_title, width=600, height=800)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)
        
        # If we have data loaded, update the display now that GUI is ready
        if self.transforms_manager.has_transforms():
            self.transforms_manager.update_display()
        
        dpg.start_dearpygui()
        
        # Store export state and YAML data before destroying context
        self.export_requested = self.get_export_state()
        self.final_yaml_data = self.transforms_manager.get_yaml_string()
        
        dpg.destroy_context()
    
    def get_export_state(self):
        """Get whether export changes is checked"""
        try:
            return dpg.get_value("export_changes_checkbox")
        except:
            return False
    
    def get_yaml_string(self):
        """Get current pipeline as YAML string (for Blender integration)"""
        return self.transforms_manager.get_yaml_string()


def launch_transform_editor(yaml_string="", window_title="Transform Pipeline Editor"):
    """
    Launch the transform editor with pipeline data from a YAML string (for Blender integration)
    
    Args:
        yaml_string (str): Pipeline state as YAML string
        window_title (str): Title for the window
    
    Returns:
        str or None: YAML string if "Export Changes" is checked, None otherwise
    """
    try:
        # Create the editor instance
        app = TransformEditor()
        
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
        print(f"Error launching transform editor: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # Test data - sample transforms
    test_yaml = """- property_path: world.color
  sampler_name: dirichlet
  params:
    alphas: [0.3, 0.3, 0.3, 1]
- property_path: lamp.power
  sampler_name: gamma
  params:
    alpha: 2
    beta: 5
- property_path: camera.location
  sampler_name: normal
  params:
    mu: 0
    sigma: 0.1
    n: 3
"""
    
    app = TransformEditor()
    app.load_pipeline_from_yaml(test_yaml)
    app.run()

