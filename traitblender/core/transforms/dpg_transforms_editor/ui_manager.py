"""
UI Manager
Handles GUI creation, theming, and layout.
"""

import dearpygui.dearpygui as dpg


class UIManager:
    """Manages GUI creation, theming, and UI layout."""
    
    def __init__(self):
        self.theme_created = False
    
    def create_gui(self, transforms_manager):
        """Create the main GUI"""
        dpg.create_context()
        
        # Create Blender-like theme
        self.create_blender_theme()
        
        # Create main window as primary window
        with dpg.window(tag="main_window", label="", width=-1, height=-1):
            # Title section
            dpg.add_text("Transform Pipeline Editor", color=(100, 150, 200))
            dpg.add_spacer(height=10)
            
            # Control buttons section
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Add Transform",
                    callback=lambda: self._show_add_transform_dialog(transforms_manager),
                    width=120
                )
                dpg.add_button(
                    label="Clear All",
                    callback=lambda: transforms_manager.clear_all(),
                    width=120
                )
            
            dpg.add_spacer(height=10)
            
            # Export checkbox
            dpg.add_checkbox(label="Export Changes", tag="export_changes_checkbox", default_value=False)
            
            dpg.add_spacer(height=10)
            dpg.add_separator()
            dpg.add_spacer(height=10)
            
            # Transforms list label
            dpg.add_text("Transforms in Pipeline:", color=(200, 200, 200))
            dpg.add_spacer(height=5)
            
            # Scrollable transforms list container
            with dpg.child_window(
                tag="transforms_list",
                width=-1,
                height=-1,
                border=False
            ):
                # Transform cards will be added here
                pass
    
    def _show_add_transform_dialog(self, transforms_manager):
        """Show dialog to add a new transform (placeholder for now)"""
        # TODO: Implement full add transform dialog with dynamic parameter inputs
        # For now, just add a dummy transform for testing
        transforms_manager.add_transform(
            property_path="world.color.r",
            sampler_name="normal",
            params={"mu": 0.5, "sigma": 0.1}
        )
    
    def create_blender_theme(self):
        """Create Blender-like theme (same as CSV viewer)"""
        if self.theme_created:
            return
        
        with dpg.theme() as blender_theme:
            with dpg.theme_component(dpg.mvAll):
                # Main background colors (Blender dark theme)
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (43, 43, 43, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (60, 60, 60, 255))
                dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (43, 43, 43, 255))
                
                # Text colors
                dpg.add_theme_color(dpg.mvThemeCol_Text, (200, 200, 200, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (120, 120, 120, 255))
                
                # Button colors
                dpg.add_theme_color(dpg.mvThemeCol_Button, (60, 60, 60, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (80, 80, 80, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (100, 100, 100, 255))
                
                # Frame/Input colors
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (35, 35, 35, 255))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (40, 40, 40, 255))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (45, 45, 45, 255))
                
                # Scrollbar colors
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (50, 50, 50, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (80, 80, 80, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (100, 100, 100, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (120, 120, 120, 255))
                
                # Border colors
                dpg.add_theme_color(dpg.mvThemeCol_Border, (80, 80, 80, 255))
                
                # Check mark
                dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (200, 200, 200, 255))
                
                # Button and frame styles
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1.0)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 2.0)
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 2.0)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 2.0)
        
        # Apply the Blender theme globally
        dpg.bind_theme(blender_theme)
        self.theme_created = True

