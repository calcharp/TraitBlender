import dearpygui.dearpygui as dpg

def dpg_context(fxn):
    """
    A decorator to run a function in a dpg context
    """
    def wrapper(*args, **kwargs):
        # setup the context
        dpg.create_context()
        # run the function
        fxn(*args, **kwargs)
        # start the engine
        dpg.setup_dearpygui()
        # show the viewport
        dpg.show_viewport()
        # start the engine
        dpg.start_dearpygui()
        # destroy the context
        dpg.destroy_context()
    return wrapper