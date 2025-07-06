import dearpygui.dearpygui as dpg

def create_sidebar() -> None:
    """
    Create the sidebar with controls and options
    """
    with dpg.window(label="Dataset", no_move=True, no_title_bar=True, no_resize=True, no_background=True, no_collapse=True, menubar=False,pos=(0, 0), height=600, width=200):
        dpg.add_text("Sidebar")
