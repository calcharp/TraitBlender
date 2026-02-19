"""
App UI manager for DPG dataset editor.
Handles main GUI creation, theming, and layout.
"""

import dearpygui.dearpygui as dpg


class AppUIManager:
    """Manages main app GUI creation, theming, and layout."""

    def __init__(self):
        self.theme_created = False

    def create_gui(self, dataset_handler, filter_ui_manager, table_ui_manager):
        """Create the main GUI"""
        dpg.create_context()

        # Create Blender-like theme
        self.create_blender_theme()

        # Create main window as primary window
        with dpg.window(tag="main_window", label="", width=-1, height=-1):
            # Create left sidebar
            self.create_sidebar(dataset_handler, filter_ui_manager)

            # Create main content area
            self.create_content_area(table_ui_manager)
    
    def create_blender_theme(self):
        """Create Blender-like theme"""
        if self.theme_created:
            return
        
        with dpg.theme() as blender_theme:
            with dpg.theme_component(dpg.mvAll):
                # Main background colors (Blender dark theme)
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (43, 43, 43, 255))  # #2b2b2b - Main background
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (60, 60, 60, 255))   # #3c3c3c - Panel background
                dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (43, 43, 43, 255))   # #2b2b2b - Popup background
                
                # Text colors
                dpg.add_theme_color(dpg.mvThemeCol_Text, (200, 200, 200, 255))   # #c8c8c8 - Main text
                dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (120, 120, 120, 255))  # #787878 - Disabled text
                dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (70, 130, 180, 255))  # #4682b4 - Selected text bg
                
                # Button colors
                dpg.add_theme_color(dpg.mvThemeCol_Button, (60, 60, 60, 255))    # #3c3c3c - Button background
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (80, 80, 80, 255))  # #505050 - Button hover
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (100, 100, 100, 255))  # #646464 - Button active
                
                # Frame/Input colors (darker than table background)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (35, 35, 35, 255))   # #232323 - Input background (darker)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (40, 40, 40, 255))  # #282828 - Input hover
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (45, 45, 45, 255))   # #2d2d2d - Input active
                
                # Title bar colors
                dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (35, 35, 35, 255))   # #232323 - Title background
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (50, 50, 50, 255))  # #323232 - Active title
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (30, 30, 30, 255))  # #1e1e1e - Collapsed title
                
                # Scrollbar colors
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (50, 50, 50, 255))  # #323232 - Scrollbar background
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (80, 80, 80, 255))  # #505050 - Scrollbar grab
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (100, 100, 100, 255))  # #646464 - Scrollbar hover
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (120, 120, 120, 255))  # #787878 - Scrollbar active
                
                # Table colors (header matches input fields, but we'll handle Row column separately)
                dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, (35, 35, 35, 255))  # #232323 - Table header (matches input cells)
                dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong, (80, 80, 80, 255))  # #505050 - Strong borders
                dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight, (60, 60, 60, 255))  # #3c3c3c - Light borders
                dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, (40, 40, 40, 255))  # #282828 - Row background (lighter than headers)
                dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt, (45, 45, 45, 255))  # #2d2d2d - Alt row background (lighter than headers)
                
                # Header colors
                dpg.add_theme_color(dpg.mvThemeCol_Header, (60, 60, 60, 255))    # #3c3c3c - Header background
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (80, 80, 80, 255))  # #505050 - Header hover
                dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (100, 100, 100, 255))  # #646464 - Header active
                
                # Separator colors
                dpg.add_theme_color(dpg.mvThemeCol_Separator, (80, 80, 80, 255))  # #505050 - Separator
                dpg.add_theme_color(dpg.mvThemeCol_SeparatorHovered, (100, 100, 100, 255))  # #646464 - Separator hover
                dpg.add_theme_color(dpg.mvThemeCol_SeparatorActive, (120, 120, 120, 255))  # #787878 - Separator active
                
                # Border colors
                dpg.add_theme_color(dpg.mvThemeCol_Border, (80, 80, 80, 255))     # #505050 - Border
                dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 255))  # #000000 - Border shadow
                
                # Resize grip colors
                dpg.add_theme_color(dpg.mvThemeCol_ResizeGrip, (80, 80, 80, 255))  # #505050 - Resize grip
                dpg.add_theme_color(dpg.mvThemeCol_ResizeGripHovered, (100, 100, 100, 255))  # #646464 - Resize grip hover
                dpg.add_theme_color(dpg.mvThemeCol_ResizeGripActive, (120, 120, 120, 255))  # #787878 - Resize grip active
                
                # Check mark and slider colors
                dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (200, 200, 200, 255))  # #c8c8c8 - Check mark
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (100, 150, 200, 255))  # #6496c8 - Slider grab
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (120, 170, 220, 255))  # #78aadc - Slider active
                
                # Button border colors (using Border color for button outlines)
                dpg.add_theme_color(dpg.mvThemeCol_Border, (100, 100, 100, 255))  # #646464 - General border color
                
                # Navigation colors
                dpg.add_theme_color(dpg.mvThemeCol_NavHighlight, (100, 150, 200, 255))  # #6496c8 - Nav highlight
                dpg.add_theme_color(dpg.mvThemeCol_NavWindowingHighlight, (200, 200, 200, 255))  # #c8c8c8 - Nav windowing
                dpg.add_theme_color(dpg.mvThemeCol_NavWindowingDimBg, (0, 0, 0, 100))  # Dim background
                
                # Modal and drag drop colors
                dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg, (0, 0, 0, 100))  # Modal dim background
                dpg.add_theme_color(dpg.mvThemeCol_DragDropTarget, (100, 150, 200, 255))  # #6496c8 - Drag drop target
                
                # Plot colors
                dpg.add_theme_color(dpg.mvThemeCol_PlotLines, (200, 200, 200, 255))  # #c8c8c8 - Plot lines
                dpg.add_theme_color(dpg.mvThemeCol_PlotLinesHovered, (255, 255, 255, 255))  # #ffffff - Plot lines hover
                dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, (150, 150, 150, 255))  # #969696 - Plot histogram
                dpg.add_theme_color(dpg.mvThemeCol_PlotHistogramHovered, (200, 200, 200, 255))  # #c8c8c8 - Plot histogram hover
                
                # Button and frame styles (Blender-style outlines)
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1.0)   # 1px border for buttons and inputs
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 2.0)     # Slight rounding like Blender
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 2.0)     # Child window rounding
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 2.0)    # Window rounding
        
        # Create a special theme for row index cells with hover effect
        with dpg.theme(tag="row_index_theme"):
            with dpg.theme_component(dpg.mvButton):
                # Make row index buttons look like text but with hover effects
                dpg.add_theme_color(dpg.mvThemeCol_Button, (40, 40, 40, 0))  # Transparent background
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (100, 150, 200, 50))  # Blue background on hover
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (100, 150, 200, 100))  # Blue background on click
                dpg.add_theme_color(dpg.mvThemeCol_Text, (200, 200, 200, 255))  # Light grey text
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0.0)  # No border
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0.0)  # No rounding
        
        # Apply the Blender theme globally
        dpg.bind_theme(blender_theme)
        self.theme_created = True
    
    def create_sidebar(self, dataset_handler, filter_ui_manager):
        """Create the left sidebar"""
        with dpg.child_window(tag="sidebar", parent="main_window", width=200, height=-1, pos=(0, 0)):
            dpg.add_spacer(height=10)
            
            # Data Management section
            dpg.add_text("Data Management", color=(100, 150, 200))
            dpg.add_spacer(height=2)
            dpg.add_button(label="Save Changes", callback=lambda: dataset_handler.save_changes(), width=180)
            dpg.add_button(label="Reset to Last Save", callback=lambda: dataset_handler.reset_to_original(), width=180)
            dpg.add_spacer(height=5)
            dpg.add_checkbox(label="Export Changes", tag="export_changes_checkbox", default_value=False)
            dpg.add_spacer(height=10)
            
            # Filtering section
            dpg.add_text("Filtering", color=(100, 150, 200))
            dpg.add_spacer(height=2)
            
            # Filter control buttons - arranged vertically to ensure visibility
            dpg.add_button(label="Insert Filter", callback=filter_ui_manager.add_filter_row, width=180)
            dpg.add_button(label="Apply Filters", callback=filter_ui_manager.apply_filter, width=180)
            dpg.add_button(label="Clear All", callback=filter_ui_manager.clear_filter, width=180)
            
            dpg.add_spacer(height=2)
            
            # Filter rows container
            dpg.add_child_window(tag="filter_rows_container", width=-1, height=200, no_scrollbar=False)
            
            # Initialize with one filter row
            filter_ui_manager.add_filter_row()
    
    def create_content_area(self, table_ui_manager):
        """Create the main content area"""
        with dpg.child_window(tag="content_area", parent="main_window", width=-1, height=-1, pos=(200, 0)):
            dpg.add_spacer(height=10)
            # Pagination controls (initially hidden)
            dpg.add_child_window(tag="pagination_controls", width=-1, height=80, show=False, no_scrollbar=True, border=False)
            dpg.add_text("Navigation", parent="pagination_controls")
            dpg.add_spacer(height=5, parent="pagination_controls")
            
            # Page navigation buttons - create a horizontal layout manually
            dpg.add_button(label="<< First", callback=table_ui_manager.go_to_first_page, width=60, height=25, parent="pagination_controls", pos=(10, 30))
            dpg.add_button(label="< Prev", callback=table_ui_manager.go_to_previous_page, width=60, height=25, parent="pagination_controls", pos=(80, 30))
            dpg.add_button(label="Next >", callback=table_ui_manager.go_to_next_page, width=60, height=25, parent="pagination_controls", pos=(150, 30))
            dpg.add_button(label="Last >>", callback=table_ui_manager.go_to_last_page, width=60, height=25, parent="pagination_controls", pos=(220, 30))
            
            dpg.add_text("Page info", tag="pagination_info", parent="pagination_controls", pos=(10, 60))
            
            dpg.add_separator()
            dpg.add_spacer(height=5)
    
    def on_viewport_resize(self):
        """Handle viewport resize events"""
        try:
            viewport_width = dpg.get_viewport_width()
            viewport_height = dpg.get_viewport_height()
            
            # Update sidebar height
            if dpg.does_item_exist("sidebar"):
                dpg.configure_item("sidebar", height=viewport_height - 20)
            
            # Update content area position and size
            if dpg.does_item_exist("content_area"):
                dpg.configure_item("content_area", 
                                 pos=(200, 20), 
                                 width=viewport_width - 200, 
                                 height=viewport_height - 20)
        except:
            pass  # Ignore errors during resize
