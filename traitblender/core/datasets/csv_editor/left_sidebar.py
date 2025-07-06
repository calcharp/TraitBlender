import dearpygui.dearpygui as dpg

def create_sidebar() -> None:
    """
    Create the sidebar with controls and options
    """
    with dpg.window(label="Left Sidebar", no_move=True, no_title_bar=True, no_resize=True, no_collapse=True, menubar=False, pos=(0, 0), height=600, width=200) as left_sidebar:
        dpg.add_text("Sidebar")


    """Sidebar Them"""
    with dpg.theme() as sidebar_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (71, 114, 179), category=dpg.mvThemeCat_Core)

        dpg.bind_item_theme(left_sidebar, sidebar_theme)

