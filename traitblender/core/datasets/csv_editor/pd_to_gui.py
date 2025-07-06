import dearpygui.dearpygui as dpg
import pandas as pd

def pd_to_gui(df: pd.DataFrame) -> None:
    """
    Convert a pandas dataframe to a gui table
    """
    with dpg.window(label="Dataset", no_move=True, no_title_bar=True, no_resize=False, no_background=True, no_collapse=True, menubar=False,pos=(210, 100), height=500, width=680) as data_table_windows:
        with dpg.table(header_row=True, row_background=True, borders_innerH=True, borders_innerV=True, borders_outerH=True, borders_outerV=True, tag="data_table") as data_table:
            # Add columns
            for column in df.columns:
                dpg.add_table_column(label=column)
            
            # Add rows
            for row in df.index:
                with dpg.table_row():
                    for column in df.columns:
                        with dpg.table_cell():
                            dpg.add_text(str(df.iloc[row][column]))