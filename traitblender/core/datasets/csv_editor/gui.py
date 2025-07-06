import dearpygui.dearpygui as dpg
from .context_wrapper import dpg_context
from .csv_handlers import get_table
from .pd_to_gui import pd_to_gui
from .left_sidebar import create_sidebar
from .themes import create_theme

@dpg_context
def gui(datatable: str) -> str | None:

    df = get_table(datatable)
    pd_to_gui(df)
    create_sidebar()
    create_theme()

    with dpg.window(tag='Background'):
        pass

    # create a viewport
    dpg.create_viewport(title="Dataset Editor", width=900, height=600)
    dpg.set_primary_window('Background', True)

    return "Table Closed"

