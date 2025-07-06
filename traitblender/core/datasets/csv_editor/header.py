import dearpygui.dearpygui as dpg

def create_header() -> None:
    """
    Create the sidebar with controls and options
    """
    with dpg.window(label="Header", 
                    no_move=True, 
                    no_title_bar=True, 
                    no_collapse=True, 
                    menubar=False, 
                    pos=(200, 0), 
                    height=100, 
                    width=700) as header:
        pass


    """Header Theme"""
    with dpg.theme() as header_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (51, 52, 86), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0, category=dpg.mvThemeCat_Core)


        dpg.bind_item_theme(header, header_theme)
