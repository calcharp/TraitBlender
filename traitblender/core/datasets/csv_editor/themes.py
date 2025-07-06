import dearpygui.dearpygui as dpg

def create_theme() -> dict:
    """
    Create the theme for the GUI
    """
    with dpg.theme() as sidebar_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255,255,255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)


    my_themes = {
        "Left Sidebar Theme": sidebar_theme
    }

    return my_themes