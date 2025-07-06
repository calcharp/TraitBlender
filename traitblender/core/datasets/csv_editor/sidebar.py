import dearpygui.dearpygui as dpg

def create_sidebar() -> None:
    """
    Create the sidebar with controls and options
    """
    with dpg.child_window(width=225, autosize_y=True, tag="sidebar", no_scrollbar=True):
        dpg.add_text("Sidebar")
        dpg.add_separator()
        # Add more sidebar content here later 