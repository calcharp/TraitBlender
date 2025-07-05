import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from io import StringIO
from copy import deepcopy
import importlib.util
import re

filtered_df = None

def edit_table_string(initial_string):
    """
    Opens a table editor window for editing CSV-like string data.
    
    Args:
        initial_string (str): The initial CSV-like string to edit
    
    Returns:
        str: The modified string after editing, or None if cancelled
    """
    # Check for Excel support
    has_excel_support = importlib.util.find_spec("openpyxl") is not None

    # Let pandas infer types automatically
    try:
        df = pd.read_csv(StringIO(initial_string))
        # Show loading message for large datasets
        if len(df) > 500:
            print(f"Loading large dataset with {len(df)} rows...")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to parse input string as CSV:\n{str(e)}")
        return None

    # After DataFrame creation, ensure proper dtypes
    df = df.convert_dtypes()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype("string")

    root = tk.Tk()
    root.title("CSV Editor")
    root.geometry("1000x600")

    # Store the final string
    result_string = [None]
    
    def on_closing():
        if save_on_exit_var.get():
            save_changes()
            root.destroy()
        else:
            if messagebox.askyesno("Save Changes?", "Do you want to save your changes before exiting?"):
                save_changes()
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Style for dark theme
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview", 
                    background="#2b2b2b", 
                    foreground="white", 
                    fieldbackground="#2b2b2b")
    style.configure("Treeview.Heading", 
                    background="#3d3d3d", 
                    foreground="white")
    style.map("Treeview", 
              background=[("selected", "#6A5ACD")], 
              foreground=[("selected", "white")])
    style.configure("TFrame", background="#383838")
    style.configure("TLabel", 
                    background="#383838", 
                    foreground="white")
    style.configure("TButton", 
                    padding=5)
    style.configure("TCheckbutton",
                    background="#383838",
                    foreground="white",
                    focuscolor="none")
    style.configure("Separator.TFrame", 
                    background="#2b2b2b")

    # Main container
    main_container = ttk.Frame(root)
    main_container.pack(fill="both", expand=True)

    # Undo system
    class UndoManager:
        def __init__(self, initial_df):
            self.history = [initial_df.copy()]
            self.current_index = 0
            self.max_history = 50  # Limit history to prevent memory issues
            self.buttons = {}  # Store button references
            
        def register_buttons(self, undo_btn, redo_btn, reset_btn):
            """Register button references for state management"""
            self.buttons = {
                'undo': undo_btn,
                'redo': redo_btn,
                'reset': reset_btn
            }
            self._update_buttons()
            
        def save_state(self, df):
            """Save current state to history"""
            # Remove any future states if we're not at the end
            self.history = self.history[:self.current_index + 1]
            # Add new state
            self.history.append(df.copy())
            self.current_index += 1
            
            # Limit history size for large datasets
            if len(self.history) > self.max_history:
                self.history = self.history[-self.max_history:]
                self.current_index = len(self.history) - 1
            
            self._update_buttons()
            
        def undo(self):
            """Go back one step in history"""
            if self.current_index > 0:
                self.current_index -= 1
                self._update_buttons()
                return self.history[self.current_index].copy()
            return None
        
        def redo(self):
            """Go forward one step in history"""
            if self.current_index < len(self.history) - 1:
                self.current_index += 1
                self._update_buttons()
                return self.history[self.current_index].copy()
            return None
        
        def reset(self):
            """Go back to the initial state"""
            if self.current_index > 0:
                self.current_index = 0
                self._update_buttons()
                return self.history[0].copy()
            return None
        
        def can_undo(self):
            """Check if undo is possible"""
            return self.current_index > 0
            
        def can_redo(self):
            """Check if redo is possible"""
            return self.current_index < len(self.history) - 1
            
        def can_reset(self):
            """Check if reset is possible"""
            return self.current_index > 0
        
        def _update_buttons(self):
            """Update button states based on current history position"""
            if not self.buttons:
                return
                
            # Update undo button
            if self.buttons.get('undo'):
                self.buttons['undo'].configure(
                    state="normal" if self.can_undo() else "disabled"
                )
            
            # Update redo button
            if self.buttons.get('redo'):
                self.buttons['redo'].configure(
                    state="normal" if self.can_redo() else "disabled"
                )
            
            # Update reset button
            if self.buttons.get('reset'):
                self.buttons['reset'].configure(
                    state="normal" if self.can_reset() else "disabled"
                )
        
        def get_history_info(self):
            """Get information about the current history state"""
            return {
                'total_states': len(self.history),
                'current_index': self.current_index,
                'can_undo': self.can_undo(),
                'can_redo': self.can_redo(),
                'can_reset': self.can_reset()
            }
        
        def debug_info(self):
            """Print debug information about the undo system"""
            info = self.get_history_info()
            print(f"=== Undo System Debug Info ===")
            print(f"Total states: {info['total_states']}")
            print(f"Current index: {info['current_index']}")
            print(f"Can undo: {info['can_undo']}")
            print(f"Can redo: {info['can_redo']}")
            print(f"Can reset: {info['can_reset']}")
            print(f"Button states: {list(self.buttons.keys()) if self.buttons else 'No buttons registered'}")
            print(f"History size: {len(self.history)}")
            if self.history:
                print(f"Current DataFrame shape: {self.history[self.current_index].shape}")
            print("=" * 30)

    undo_manager = UndoManager(df)
    
    # Print initial debug info
    print("=== Initial Undo System Setup ===")
    undo_manager.debug_info()

    # Left sidebar
    sidebar = ttk.Frame(main_container, style="TFrame", width=200)
    sidebar.pack(side="left", fill="y", padx=10, pady=10)
    sidebar.pack_propagate(False)

    # Save section at the top
    save_section = ttk.Frame(sidebar, style="TFrame")
    save_section.pack(fill="x", pady=(0, 10))

    save_on_exit_var = tk.BooleanVar(value=False)
    save_checkbox = ttk.Checkbutton(save_section, text="Save on exit", variable=save_on_exit_var)
    save_checkbox.pack(fill="x")

    def save_changes():
        string_buffer = StringIO()
        # Save the filtered view if present, otherwise the full DataFrame
        (filtered_df if filtered_df is not None else df).to_csv(string_buffer, index=False)
        result_string[0] = string_buffer.getvalue()

    # Separator after save section
    ttk.Frame(sidebar, height=1, style="Separator.TFrame").pack(fill="x", pady=10)

    # Search section in sidebar
    search_section = ttk.Frame(sidebar, style="TFrame")
    search_section.pack(fill="x", pady=(0, 10))

    ttk.Label(search_section, text="Search & Filter", style="TLabel").pack(fill="x", pady=(0, 10))

    # Create a frame to hold all search rows
    search_rows_frame = ttk.Frame(search_section, style="TFrame")
    search_rows_frame.pack(fill="x", pady=(0, 5))

    # List to keep track of search rows
    search_rows = []
    
    # Get column list
    columns = list(df.columns)

    class SearchRow:
        def __init__(self, parent):
            self.frame = ttk.Frame(parent, style="TFrame")
            self.frame.pack(fill="x", pady=(0, 2))

            # Column dropdown
            self.col_var = tk.StringVar(value=columns[0])
            self.col_select = ttk.Combobox(self.frame, textvariable=self.col_var, values=columns, state="readonly", width=15)
            self.col_select.pack(side="left", padx=(0, 2))

            # Search entry
            self.search_var = tk.StringVar()
            self.search_entry = ttk.Entry(self.frame, textvariable=self.search_var)
            self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 2))

            # Remove button
            self.remove_btn = ttk.Button(self.frame, text="×", width=3, 
                                       command=lambda: self.remove_row(),
                                       style="Remove.TButton")
            self.remove_btn.pack(side="right")
            
            # Add custom style for remove button
            style = ttk.Style()
            style.configure("Remove.TButton", 
                          background="#383838",
                          foreground="white",
                          padding=0)

        def remove_row(self):
            search_rows.remove(self)
            self.frame.destroy()

    def add_search_row():
        row = SearchRow(search_rows_frame)
        search_rows.append(row)

    # Add initial search row
    add_search_row()

    # Add top button frame
    top_button_frame = ttk.Frame(search_section, style="TFrame")
    top_button_frame.pack(fill="x", pady=(0, 2))

    # Add "Add Filter" button
    add_filter_btn = ttk.Button(top_button_frame, text="+ Add Filter", command=add_search_row)
    add_filter_btn.pack(side="left", fill="x", expand=True, padx=(0, 2))

    # Add global regex checkbox
    global_regex_mode = tk.BooleanVar(value=True)
    global_regex_check = tk.Checkbutton(top_button_frame, text="regex", variable=global_regex_mode, 
                                bg="#383838", fg="white", selectcolor="#2b2b2b", 
                                activebackground="#383838", activeforeground="white")
    global_regex_check.pack(side="left")

    # Add bottom button frame
    bottom_button_frame = ttk.Frame(search_section, style="TFrame")
    bottom_button_frame.pack(fill="x", pady=(2, 0))

    # Add filter button
    filter_btn = ttk.Button(bottom_button_frame, text="Filter")
    filter_btn.pack(side="left", fill="x", expand=True, padx=(0, 2))

    # Add clear button
    clear_btn = ttk.Button(bottom_button_frame, text="Clear")
    clear_btn.pack(side="left", fill="x", expand=True)

    # Separator
    ttk.Frame(sidebar, height=1, style="Separator.TFrame").pack(fill="x", pady=10)

    # Table operations section
    operations_section = ttk.Frame(sidebar, style="TFrame")
    operations_section.pack(fill="x")

    ttk.Label(operations_section, text="Table Operations", style="TLabel").pack(fill="x", pady=(0, 10))

    # Undo section
    undo_section = ttk.Frame(sidebar, style="TFrame")
    undo_section.pack(fill="x")

    ttk.Label(undo_section, text="History", style="TLabel").pack(fill="x", pady=(0, 10))

    def undo_action():
        nonlocal df
        new_df = undo_manager.undo()
        if new_df is not None:
            df = new_df.copy()  # Ensure we have a fresh copy
            refresh_tree()
            update_page_info()
            update_pagination_buttons()
            print(f"Undo: {undo_manager.get_history_info()}")

    def redo_action():
        nonlocal df
        new_df = undo_manager.redo()
        if new_df is not None:
            df = new_df.copy()  # Ensure we have a fresh copy
            refresh_tree()
            update_page_info()
            update_pagination_buttons()
            print(f"Redo: {undo_manager.get_history_info()}")

    def reset_action():
        nonlocal df
        new_df = undo_manager.reset()
        if new_df is not None:
            df = new_df.copy()  # Ensure we have a fresh copy
            refresh_tree()
            update_page_info()
            update_pagination_buttons()
            print(f"Reset: {undo_manager.get_history_info()}")

    # Create frame for undo/redo buttons side by side
    history_buttons = ttk.Frame(undo_section, style="TFrame")
    history_buttons.pack(fill="x")

    undo_btn = ttk.Button(history_buttons, text="↶ Undo", command=undo_action, state="disabled", width=10)
    undo_btn.pack(side="left", padx=(0, 2), fill="x", expand=True)

    redo_btn = ttk.Button(history_buttons, text="↷ Redo", command=redo_action, state="disabled", width=10)
    redo_btn.pack(side="left", fill="x", expand=True)

    # Add reset button below
    reset_btn = ttk.Button(undo_section, text="↺ Reset to Initial", command=reset_action, state="disabled")
    reset_btn.pack(fill="x", pady=(2, 0))

    # Register buttons with the undo manager
    undo_manager.register_buttons(undo_btn, redo_btn, reset_btn)

    # Separator after undo section
    ttk.Frame(sidebar, height=1, style="Separator.TFrame").pack(fill="x", pady=10)

    # Table operations section
    operations_section = ttk.Frame(sidebar, style="TFrame")
    operations_section.pack(fill="x")

    def insert_row(above=True):
        global filtered_df
        selection = tree.selection()
        if not selection:
            return
        # Use filtered data if filter is active, otherwise use full data
        data_source = filtered_df if filtered_df is not None else df
        # Get index to insert at (convert from tree index to DataFrame index)
        tree_idx = tree.index(selection[0])
        if filtered_df is not None:
            # Insert into filtered_df for immediate UI feedback
            original_idx = data_source.iloc[tree_idx]["index"]
            insert_idx = tree_idx
            # Insert new row into filtered_df
            empty_data = {col: pd.NA for col in data_source.columns}
            filtered_upper = data_source.iloc[:insert_idx]
            filtered_lower = data_source.iloc[insert_idx:]
            filtered_new = pd.concat([filtered_upper, pd.DataFrame([empty_data]), filtered_lower], ignore_index=True)
            filtered_df = filtered_new
            # Now insert into the full DataFrame at the correct position
            full_insert_idx = df.index.get_loc(original_idx)
            if not above:
                full_insert_idx += 1
            df_upper = df.iloc[:full_insert_idx]
            df_lower = df.iloc[full_insert_idx:]
            df_new = pd.concat([df_upper, pd.DataFrame([{col: pd.NA for col in df.columns}]), df_lower], ignore_index=True)
            df.loc[:] = df_new
        else:
            insert_idx = tree_idx + current_page * rows_per_page
            if not above:
                insert_idx += 1
            # Clamp insert_idx to valid range
            df_length = len(df)
            if insert_idx < 0:
                insert_idx = 0
            if insert_idx > df_length:
                insert_idx = df_length
            empty_data = {col: pd.NA for col in df.columns}
            df_upper = df.iloc[:insert_idx]
            df_lower = df.iloc[insert_idx:]
            df_new = pd.concat([df_upper, pd.DataFrame([empty_data]), df_lower], ignore_index=True)
            df.loc[:] = df_new
        # After insertion, ensure proper dtypes
        df[:] = df.convert_dtypes()
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype("string")
        # Update pagination
        nonlocal total_pages
        total_pages = max(1, (len(df) + rows_per_page - 1) // rows_per_page)
        save_state()
        refresh_tree()
        update_page_info()
        update_pagination_buttons()

    def duplicate_rows():
        selection = tree.selection()
        if not selection:
            return
        
        # Get selected indices (convert from tree indices to DataFrame indices)
        tree_indices = [tree.index(item) for item in selection]
        df_indices = [current_page * rows_per_page + idx for idx in tree_indices]
        
        # Duplicate rows in DataFrame
        for idx in sorted(df_indices, reverse=True):
            new_row = df.iloc[idx:idx+1].copy()
            # Try to modify species column if it exists
            if 'species' in df.columns and pd.notna(new_row.iloc[0]['species']):
                n = 1
                while any(df['species'] == f"{new_row.iloc[0]['species']} ({n})"):
                    n += 1
                new_row.iloc[0]['species'] = f"{new_row.iloc[0]['species']} ({n})"
            df.loc[idx + 0.5] = new_row.iloc[0]
        
        df.sort_index(inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        # Update pagination
        nonlocal total_pages
        total_pages = max(1, (len(df) + rows_per_page - 1) // rows_per_page)
        
        save_state()
        refresh_tree()
        update_page_info()
        update_pagination_buttons()

    def delete_rows():
        selection = tree.selection()
        if not selection:
            return
        # Use filtered data if filter is active, otherwise use full data
        data_source = filtered_df if filtered_df is not None else df
        # Get selected indices and map to DataFrame indices
        tree_indices = [tree.index(item) for item in selection]
        df_indices = []
        for tree_idx in tree_indices:
            if filtered_df is not None:
                original_idx = data_source.iloc[tree_idx]["index"]
                df_idx = df.index.get_loc(original_idx)
            else:
                df_idx = tree_idx + current_page * rows_per_page
            df_indices.append(df_idx)
        # Remove from DataFrame
        df.drop(df_indices, inplace=True)
        df.reset_index(drop=True, inplace=True)
        # After deletion, ensure proper dtypes
        df[:] = df.convert_dtypes()
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype("string")
        # Update pagination
        nonlocal total_pages
        total_pages = max(1, (len(df) + rows_per_page - 1) // rows_per_page)
        # If current page is now empty, go to previous page
        if current_page >= total_pages:
            go_to_page(total_pages - 1)
        else:
            save_state()
            refresh_tree()
            update_page_info()
            update_pagination_buttons()

    insert_above_btn = ttk.Button(operations_section, text="Insert Above", command=lambda: insert_row(True))
    insert_above_btn.pack(fill="x", pady=(0, 2))

    insert_below_btn = ttk.Button(operations_section, text="Insert Below", command=lambda: insert_row(False))
    insert_below_btn.pack(fill="x", pady=(0, 2))

    duplicate_btn = ttk.Button(operations_section, text="Duplicate", command=duplicate_rows)
    duplicate_btn.pack(fill="x", pady=(0, 2))

    delete_btn = ttk.Button(operations_section, text="Delete", command=delete_rows)
    delete_btn.pack(fill="x")

    # Separator after operations section
    ttk.Frame(sidebar, height=1, style="Separator.TFrame").pack(fill="x", pady=10)

    # Zoom control section
    zoom_section = ttk.Frame(sidebar, style="TFrame")
    zoom_section.pack(fill="x", pady=(0, 10))

    ttk.Label(zoom_section, text="Table Zoom", style="TLabel").pack(fill="x", pady=(0, 5))

    # Configure style for Treeview with base settings
    style = ttk.Style()
    BASE_ROW_HEIGHT = 25
    BASE_FONT_SIZE = 9
    style.configure("Treeview", 
        rowheight=BASE_ROW_HEIGHT,
        font=('TkDefaultFont', BASE_FONT_SIZE)
    )

    # Create a frame for zoom controls
    zoom_controls = ttk.Frame(zoom_section)
    zoom_controls.pack(fill="x", padx=5)

    current_zoom = tk.IntVar(value=100)

    def apply_zoom():
        try:
            zoom_factor = current_zoom.get() / 100.0
            
            # Calculate new dimensions with bounds checking
            # Allow larger maximum sizes for high zoom levels
            new_height = max(20, min(200, int(BASE_ROW_HEIGHT * zoom_factor)))
            new_font_size = max(7, min(72, int(BASE_FONT_SIZE * zoom_factor)))
            
            # Update Treeview styles
            style.configure("Treeview", 
                rowheight=new_height,
                font=('TkDefaultFont', new_font_size)
            )
            style.configure("Treeview.Heading",
                font=('TkDefaultFont', new_font_size)
            )
            
            # Update alternating row styles
            tree.tag_configure("odd", font=('TkDefaultFont', new_font_size))
            tree.tag_configure("even", font=('TkDefaultFont', new_font_size))
            
            # Update zoom label with thousands separator for large numbers
            zoom_text = f"{current_zoom.get():,}%"
            zoom_label.configure(text=zoom_text)
        except Exception as e:
            print(f"Zoom error: {e}")

    def change_zoom(delta):
        # Adjust step size based on current zoom level for smoother scaling
        if current_zoom.get() >= 500:
            delta *= 5  # Larger steps at high zoom
        elif current_zoom.get() >= 200:
            delta *= 2  # Medium steps at medium-high zoom
        
        new_zoom = min(1000, max(50, current_zoom.get() + delta))
        current_zoom.set(new_zoom)
        apply_zoom()

    # Variables to track button hold state
    button_held = None
    after_id = None

    def start_repeat(delta):
        global button_held, after_id
        button_held = delta
        # Start the repeat after initial delay
        after_id = zoom_controls.after(400, repeat_zoom)

    def stop_repeat(event=None):
        global button_held, after_id
        button_held = None
        if after_id:
            zoom_controls.after_cancel(after_id)
            after_id = None

    def repeat_zoom():
        global after_id
        if button_held is not None:
            change_zoom(button_held)
            # Start with 400ms delay, then repeat every 50ms
            delay = 50 if after_id else 400
            after_id = zoom_controls.after(delay, repeat_zoom)

    # Create - button
    minus_btn = ttk.Button(zoom_controls, text="-", width=3,
                          command=lambda: change_zoom(-10))  # Add back the command
    minus_btn.pack(side="left")
    # Add hold-down behavior as additional bindings
    minus_btn.bind('<ButtonPress-1>', lambda e: start_repeat(-10))
    minus_btn.bind('<ButtonRelease-1>', stop_repeat)

    # Create a frame just for the label to ensure proper centering
    label_frame = ttk.Frame(zoom_controls)
    label_frame.pack(side="left", expand=True, fill="x", padx=10)

    # Add zoom percentage label in the middle with fixed width
    zoom_label = ttk.Label(label_frame, text="100%", style="TLabel", anchor="center")
    zoom_label.pack(expand=True)

    def show_zoom_entry(event=None):
        zoom_label.pack_forget()
        zoom_entry = ttk.Entry(label_frame, width=5, justify="center")
        zoom_entry.insert(0, str(current_zoom.get()))
        zoom_entry.select_range(0, tk.END)
        zoom_entry.pack(expand=True)
        zoom_entry.focus_set()

        def apply_zoom_entry(event=None):
            try:
                val = int(zoom_entry.get())
                if not (10 <= val <= 500):
                    raise ValueError
                current_zoom.set(val)
                apply_zoom()
            except Exception:
                pass  # Ignore invalid input
            zoom_entry.destroy()
            zoom_label.pack(expand=True)
            # Unbind the root click handler
            root.unbind("<Button-1>", root_click_id)

        zoom_entry.bind("<Return>", apply_zoom_entry)
        zoom_entry.bind("<FocusOut>", apply_zoom_entry)

        def on_root_click(event):
            # If click is outside the zoom_entry, apply/revert
            widget = event.widget
            if widget is not zoom_entry:
                apply_zoom_entry()

        # Bind to root, store the binding id so we can unbind later
        global root_click_id
        root_click_id = root.bind("<Button-1>", on_root_click, add="+")

    zoom_label.bind("<Button-1>", show_zoom_entry)

    # Create + button
    plus_btn = ttk.Button(zoom_controls, text="+", width=3,
                         command=lambda: change_zoom(10))  # Add back the command
    plus_btn.pack(side="right")
    # Add hold-down behavior as additional bindings
    plus_btn.bind('<ButtonPress-1>', lambda e: start_repeat(10))
    plus_btn.bind('<ButtonRelease-1>', stop_repeat)

    # Add reset button below
    reset_btn = ttk.Button(zoom_section, text="Reset Zoom", 
                          command=lambda: (current_zoom.set(100), apply_zoom()))
    reset_btn.pack(fill="x", padx=5, pady=(5, 0))

    # Export section at bottom of sidebar
    export_section = ttk.Frame(sidebar, style="TFrame")
    export_section.pack(fill="x", side="bottom", pady=(10, 0))

    ttk.Label(export_section, text="Export", style="TLabel").pack(fill="x", pady=(0, 5))

    # Format selection frame
    format_frame = ttk.Frame(export_section, style="TFrame")
    format_frame.pack(fill="x", pady=(0, 5))

    # Format dropdown
    export_formats = {
        "CSV (*.csv)": (".csv", "csv"),
        "TSV (*.tsv)": (".tsv", "tsv"),
        "Excel (*.xlsx)": (".xlsx", "excel")
    }

    format_var = tk.StringVar(value="CSV (*.csv)")
    format_dropdown = ttk.Combobox(format_frame, 
                                  textvariable=format_var,
                                  values=list(export_formats.keys()),
                                  state="readonly")
    format_dropdown.pack(fill="x")

    def export_table():
        # Get selected format
        format_key = format_var.get()
        extension, format_type = export_formats[format_key]
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=extension,
            filetypes=[(format_key, f"*{extension}")],
            title="Export Table As",
            initialfile=f"table{extension}"
        )
        
        if file_path:
            try:
                # Ensure the DataFrame is up to date
                if format_type == "csv":
                    df.to_csv(file_path, index=False, encoding='utf-8')
                elif format_type == "tsv":
                    df.to_csv(file_path, index=False, sep='\t', encoding='utf-8')
                elif format_type == "excel":
                    try:
                        df.to_excel(file_path, index=False)
                    except ImportError:
                        messagebox.showerror("Export Error", 
                            "Excel export requires the openpyxl package.\n"
                            "Please install it using:\n"
                            "pip install openpyxl")
                        return
                
                # Verify file was created
                try:
                    if format_type in ["csv", "tsv"]:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            pass
                    else:  # Excel files can't be opened for reading text
                        import os
                        if not os.path.exists(file_path):
                            raise Exception("File was not created")
                
                    # Success feedback
                    export_btn.configure(text="✓ Exported!", state="disabled")
                    root.after(1000, lambda: export_btn.configure(text="📤 Export As", state="normal"))
                
                except Exception as e:
                    raise Exception(f"File verification failed: {str(e)}")
                
            except Exception as e:
                import traceback
                error_msg = f"Export failed: {str(e)}\n{traceback.format_exc()}"
                print(error_msg)  # Print for debugging
                
                # Show error in GUI
                export_btn.configure(text="❌ Error!", state="disabled")
                root.after(1000, lambda: export_btn.configure(text="📤 Export As", state="normal"))
                
                # Show error dialog
                messagebox.showerror("Export Error", 
                    f"Failed to export file:\n{str(e)}\n\nPlease check if the file is not open in another program.")

    export_btn = ttk.Button(export_section, text="📤 Export As", command=export_table)
    export_btn.pack(fill="x", pady=(5, 0))

    # Main content area with tree
    content_frame = ttk.Frame(main_container)
    content_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)
    
    # Pagination variables
    current_page = 0
    rows_per_page = 100
    total_pages = max(1, (len(df) + rows_per_page - 1) // rows_per_page)
    
    # Pagination controls frame
    pagination_frame = ttk.Frame(content_frame)
    pagination_frame.pack(fill="x", pady=(0, 10))
    
    # Page info label
    page_info_label = ttk.Label(pagination_frame, text="", style="TLabel")
    page_info_label.pack(side="left")
    
    # Pagination buttons frame
    pagination_buttons = ttk.Frame(pagination_frame)
    pagination_buttons.pack(side="right")
    
    def update_page_info():
        data_source = filtered_df if filtered_df is not None else df
        start_row = current_page * rows_per_page + 1
        end_row = min((current_page + 1) * rows_per_page, len(data_source))
        filter_text = f" (filtered from {len(df)})" if filtered_df is not None else ""
        page_info_label.configure(text=f"Showing {start_row}-{end_row} of {len(data_source)} rows{filter_text} (Page {current_page + 1} of {total_pages})")
    
    def go_to_page(page_num):
        nonlocal current_page
        if 0 <= page_num < total_pages:
            current_page = page_num
            refresh_tree()
            update_page_info()
            update_pagination_buttons()
    
    def update_pagination_buttons():
        # Update button states
        first_btn.configure(state="normal" if current_page > 0 else "disabled")
        prev_btn.configure(state="normal" if current_page > 0 else "disabled")
        next_btn.configure(state="normal" if current_page < total_pages - 1 else "disabled")
        last_btn.configure(state="normal" if current_page < total_pages - 1 else "disabled")
        
        # Update page number display
        page_entry.delete(0, tk.END)
        page_entry.insert(0, str(current_page + 1))
    
    # Pagination buttons
    next_btn = ttk.Button(pagination_buttons, text="Next", command=lambda: go_to_page(current_page + 1), width=6)
    next_btn.pack(side="left", padx=(0, 2))

    prev_btn = ttk.Button(pagination_buttons, text="Prev", command=lambda: go_to_page(current_page - 1), width=6)
    prev_btn.pack(side="left", padx=(0, 2))

    first_btn = ttk.Button(pagination_buttons, text="First", command=lambda: go_to_page(0), width=6)
    first_btn.pack(side="left", padx=(0, 2))

    last_btn = ttk.Button(pagination_buttons, text="Last", command=lambda: go_to_page(total_pages - 1), width=6)
    last_btn.pack(side="left", padx=(0, 2))

    # Page entry
    ttk.Label(pagination_buttons, text="Page:", style="TLabel").pack(side="left", padx=(5, 2))
    page_entry = ttk.Entry(pagination_buttons, width=5)
    page_entry.pack(side="left", padx=(0, 2))

    def on_page_entry(event):
        try:
            page_num = int(page_entry.get()) - 1
            go_to_page(page_num)
        except ValueError:
            update_pagination_buttons()  # Reset to current page

    page_entry.bind("<Return>", on_page_entry)

    ttk.Label(pagination_buttons, text=f"of {total_pages}", style="TLabel").pack(side="left", padx=(2, 5))

    # Create a separate frame for the tree and scrollbars to use grid layout
    tree_frame = ttk.Frame(content_frame)
    tree_frame.pack(fill="both", expand=True)
    
    # Setup Treeview without index column
    columns = list(df.columns)
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

    # Sorting functionality
    current_sort = {'column': None, 'reverse': False}

    def sort_column(col):
        global filtered_df
        if current_sort['column'] == col:
            current_sort['reverse'] = not current_sort['reverse']
        else:
            current_sort['column'] = col
            current_sort['reverse'] = False
        
        # Sort DataFrame
        df.sort_values(by=col, ascending=not current_sort['reverse'], inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        # If filter is active, re-apply it to get sorted filtered results
        if filtered_df is not None:
            # Re-apply the current filter to the sorted data
            apply_filter()
        
        # Reset to first page after sorting
        nonlocal current_page
        current_page = 0
        
        # Update tree
        refresh_tree()
        update_page_info()
        update_pagination_buttons()
        
        # Update headers
        for column in columns:
            if column == col:
                direction = " ↓" if current_sort['reverse'] else " ↑"
                tree.heading(column, text=f"{column}{direction}",
                            command=lambda c=column: sort_column(c))
            else:
                tree.heading(column, text=column,
                            command=lambda c=column: sort_column(c))

    # Setup column headings with sorting
    for col in columns:
        tree.heading(col, text=col, command=lambda c=col: sort_column(c), anchor=tk.W)
        tree.column(col, width=100, anchor=tk.W)

    def refresh_tree():
        # Clear existing items
        tree.delete(*tree.get_children())
        # Use filtered data if filter is active, otherwise use full data
        data_source = filtered_df if filtered_df is not None else df
        # Calculate page bounds
        start_idx = current_page * rows_per_page
        end_idx = min(start_idx + rows_per_page, len(data_source))
        # Only show current page data
        page_df = data_source.iloc[start_idx:end_idx]
        for i, (idx, row) in enumerate(page_df.iterrows()):
            values = []
            for col in data_source.columns:
                val = row[col]
                if pd.isna(val):
                    values.append("")
                elif isinstance(val, bool):
                    values.append(str(val))
                else:
                    values.append(str(val))
            tag = "odd" if i % 2 else "even"
            tree.insert("", "end", values=values, tags=(tag,))

    # Cell editing
    def on_cell_double_click(event):
        rowid = tree.identify_row(event.y)
        colid = tree.identify_column(event.x)
        if not rowid or not colid:
            return
        
        # Prevent row selection
        tree.selection_remove(*tree.selection())
        
        # Get column index (strip the '#' prefix from colid)
        col_idx = int(colid.strip("#")) - 1
        col_name = df.columns[col_idx]
        # Convert tree row index to actual DataFrame index
        tree_row_idx = tree.index(rowid)
        row_idx = current_page * rows_per_page + tree_row_idx
        
        # Get bounding box for the specific cell
        bbox = tree.bbox(rowid, colid)
        if not bbox:
            return
        x, y, width, height = bbox
        
        # Get the cell's current value
        value = tree.set(rowid, colid)
        
        # Create and configure the entry widget
        edit = ttk.Entry(tree)
        edit.insert(0, value)
        edit.select_range(0, tk.END)
        
        def save_edit(event=None):
            try:
                new_val = edit.get()
                if new_val == "":
                    df.iloc[row_idx, col_idx] = pd.NA
                else:
                    col_dtype = df.dtypes[col_idx]
                    if pd.api.types.is_bool_dtype(col_dtype):
                        val = new_val.strip().lower()
                        if val in ("true", "1", "yes"):
                            converted = True
                        elif val in ("false", "0", "no"):
                            converted = False
                        else:
                            raise ValueError(f"Invalid boolean value: '{new_val}'")
                    else:
                        try:
                            converted = pd.Series([new_val]).astype(col_dtype)[0]
                        except Exception:
                            raise ValueError(f"Invalid value '{new_val}' for column '{col_name}' of type {col_dtype}")
                    df.iloc[row_idx, col_idx] = converted
                save_state()
                display_val = df.iloc[row_idx, col_idx]
                tree.set(rowid, colid, str(display_val) if pd.notna(display_val) else "")
                edit.destroy()
            except (ValueError, TypeError) as e:
                orig_x = edit.winfo_x()
                for i in range(5):
                    edit.place(x=orig_x + (10 if i % 2 == 0 else -10), y=y)
                    root.update()
                    root.after(50)
                edit.place(x=orig_x, y=y)
                print(f"Error: {e}")
        
        def on_focus_out(event=None):
            try:
                save_edit()
            except (ValueError, TypeError):
                edit.destroy()
        
        edit.bind("<Return>", save_edit)
        edit.bind("<Escape>", lambda e: edit.destroy())
        edit.bind("<FocusOut>", on_focus_out)
        
        # Position the entry widget exactly over the cell
        edit.place(x=x, y=y, width=width, height=height)
        edit.focus_set()

    tree.bind("<Double-1>", on_cell_double_click)

    # Drag and drop reordering
    class DragManager:
        def __init__(self, tree):
            self.tree = tree
            self.dragged_items = ()
            self.drop_indicator = None
            
            # Create indicator line canvas
            self.indicator = tk.Canvas(tree, width=tree.winfo_width(), height=2, 
                                     bg='#6A5ACD', highlightthickness=0)
            
            # Bind events
            tree.bind("<ButtonPress-1>", self.on_press)
            tree.bind("<B1-Motion>", self.on_drag)
            tree.bind("<ButtonRelease-1>", self.on_release)
            tree.bind("<Configure>", self.on_configure)  # Update indicator width when tree resizes
        
        def on_configure(self, event):
            self.indicator.configure(width=self.tree.winfo_width())
        
        def show_indicator(self, y):
            if not self.indicator.winfo_ismapped():
                self.indicator.place(x=0, y=y)
            else:
                self.indicator.place_configure(y=y)
        
        def hide_indicator(self):
            if self.indicator.winfo_ismapped():
                self.indicator.place_forget()
        
        def on_press(self, event):
            iid = self.tree.identify_row(event.y)
            if iid:
                sel = self.tree.selection()
                if iid in sel:
                    self.dragged_items = sel
                else:
                    self.dragged_items = (iid,)
                    self.tree.selection_set(iid)
        
        def on_drag(self, event):
            if not self.dragged_items:
                return
            
            target_row = self.tree.identify_row(event.y)
            if not target_row:
                self.hide_indicator()
                return
            
            if target_row not in self.dragged_items:
                # Show drop indicator
                target_bbox = self.tree.bbox(target_row)
                if target_bbox:
                    # Determine if we should show indicator above or below the target row
                    middle_y = target_bbox[1] + target_bbox[3] // 2
                    if event.y < middle_y:
                        indicator_y = target_bbox[1]
                    else:
                        indicator_y = target_bbox[1] + target_bbox[3]
                    self.show_indicator(indicator_y)
                    
                    # Move items
                    target_idx = self.tree.index(target_row)
                    if event.y > middle_y:
                        target_idx += 1
                    
                    for item in self.dragged_items:
                        self.tree.move(item, '', target_idx)
                    
                    # Update alternating colors
                    for idx, item in enumerate(self.tree.get_children()):
                        self.tree.item(item, tags=("odd" if idx % 2 else "even",))
        
        def on_release(self, event):
            self.hide_indicator()
            
            if not self.dragged_items:
                return
            
            # Get the current page's data
            start_idx = current_page * rows_per_page
            end_idx = min(start_idx + rows_per_page, len(df))
            page_df = df.iloc[start_idx:end_idx].copy()
            
            # Get the new order from tree items
            new_order = []
            for item in self.tree.get_children():
                values = self.tree.item(item)["values"]
                for idx, row in page_df.iterrows():
                    if all(str(row[col]) == str(values[i]) for i, col in enumerate(df.columns)):
                        new_order.append(idx)
                        break
            
            # Reorder the current page's rows
            if new_order:
                page_df = page_df.reindex(new_order)
                # Update the main dataframe
                df.iloc[start_idx:end_idx] = page_df
                save_state()
            
            self.dragged_items = ()

    # Initialize drag manager
    drag_manager = DragManager(tree)

    # Filter functionality
    def apply_filter():
        global filtered_df
        nonlocal current_page, total_pages
        print('DEBUG: global_regex_mode.get() =', global_regex_mode.get())
        # Start with full dataset
        result_df = df
        # Collect all valid filters first
        valid_filters = []
        for row in search_rows:
            q = row.search_var.get().strip()
            col = row.col_var.get()
            if q == "":
                continue
            valid_filters.append((col, q))
        # Apply all filters to the full dataset
        try:
            if global_regex_mode.get():
                # Validate all regex patterns first
                for col, q in valid_filters:
                    try:
                        re.compile(q)
                    except re.error as regex_err:
                        messagebox.showerror("Regex Error", f"Invalid regex for column '{col}':\n'{q}'\n\nError: {regex_err}")
                        return
                for col, q in valid_filters:
                    mask = result_df[col].astype(str).str.contains(q, regex=True, na=False)
                    print(f'DEBUG: regex filter col={col}, pattern={q}, matches={mask.sum()}')
                    result_df = result_df[mask]
            else:
                for col, q in valid_filters:
                    mask = result_df[col].astype(str).str.lower().str.contains(q.lower(), regex=False, na=False)
                    result_df = result_df[mask]
        except Exception as e:
            messagebox.showerror("Filter Error", f"Error applying filters:\n{str(e)}")
            return
        # Update filtered results
        if len(result_df) == len(df):
            filtered_df = None
        else:
            filtered_df = result_df.copy()  # Do not add index as a column
        current_page = 0
        total_pages = max(1, (len(result_df) + rows_per_page - 1) // rows_per_page)
        # Update pagination and refresh
        refresh_tree()
        update_page_info()
        update_pagination_buttons()

    filter_btn.configure(command=apply_filter)
    def clear_filters():
        # Clear all search rows except the first one
        while len(search_rows) > 1:
            search_rows[-1].remove_row()
        
        # Clear the first row's search
        search_rows[0].search_var.set("")
        apply_filter()

    clear_btn.configure(command=clear_filters)

    # Initial tree population and pagination setup
    refresh_tree()
    update_page_info()
    update_pagination_buttons()

    # Configure tag colors
    tree.tag_configure("odd", background="#343434")
    tree.tag_configure("even", background="#2b2b2b")

        # Scrollbars
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscroll=vsb.set, xscroll=hsb.set)
    
    # Grid layout for tree and scrollbars within the tree frame
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    tree_frame.grid_columnconfigure(0, weight=1)
    tree_frame.grid_rowconfigure(0, weight=1)

    def save_state():
        """Save current state to undo history"""
        try:
            undo_manager.save_state(df)
            print(f"State saved: {undo_manager.get_history_info()}")
        except Exception as e:
            print(f"Error saving state: {e}")
            import traceback
            traceback.print_exc()

    root.mainloop()
    
    return result_string[0]

def create_example_data():
    # Create column headers
    headers = [
        "ID", "Name", "Age", "Height", "Weight", "Active", "Email",
        "Phone", "Birthday", "Balance", "Last Login", "Premium",
        "Score", "Rating", "Status", "Region", "Joined Date",
        "Points", "Level", "Verified"
    ]
    
    # Sample data generation helpers
    import random
    from datetime import datetime, timedelta
    
    def random_date(start_year=2020):
        days = random.randint(0, 1095)  # Up to 3 years of dates
        base = datetime(start_year, 1, 1)
        date = base + timedelta(days=days)
        return date.strftime("%Y-%m-%d")
    
    def random_phone():
        return f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
    
    # Create sample data
    data = []
    for i in range(1000):  # 1000 rows of data
        row = [
            str(i + 1001),  # ID
            f"User {chr(65 + i)}",  # Name
            str(random.randint(18, 65)),  # Age
            f"{random.uniform(1.50, 2.00):.2f}",  # Height in meters
            str(random.randint(50, 100)),  # Weight in kg
            str(random.choice([True, False])),  # Active
            f"user{chr(97 + i)}@example.com",  # Email
            random_phone(),  # Phone
            random_date(2000),  # Birthday
            f"${random.uniform(100, 10000):.2f}",  # Balance
            random_date(2023),  # Last Login
            str(random.choice([True, False])),  # Premium
            str(random.randint(0, 100)),  # Score
            f"{random.uniform(1, 5):.1f}",  # Rating
            random.choice(["Active", "Pending", "Inactive"]),  # Status
            random.choice(["North", "South", "East", "West"]),  # Region
            random_date(2020),  # Joined Date
            str(random.randint(1000, 50000)),  # Points
            str(random.randint(1, 100)),  # Level
            str(random.choice([True, False]))  # Verified
        ]
        data.append(",".join(row))
    
    return ",".join(headers) + "\n" + "\n".join(data)

if __name__ == "__main__":
    # Example usage
    sample_data = create_example_data()
    # Print the head of the CSV before opening
    import pandas as pd
    from io import StringIO
    print("=== CSV HEAD BEFORE ===")
    print(pd.read_csv(StringIO(sample_data)).head())
    print("======================\n")
    result = edit_table_string(sample_data)
    if result:
        print("=== CSV RETURNED AFTER (HEAD) ===")
        print(pd.read_csv(StringIO(result)).head())
        print("==========================")
    else:
        print("No changes were saved")

def populate_tree(tree, data_string):
    # Clear existing items
    tree.delete(*tree.get_children())
    
    # Parse the data
    lines = data_string.strip().split('\n')
    headers = lines[0].split('\t')
    
    # Setup columns
    tree["columns"] = headers
    tree["show"] = "headings"
    
    # Add data rows
    for i, line in enumerate(lines[1:], 1):
        values = line.split('\t')
        tag = 'odd' if i % 2 else 'even'
        tree.insert('', 'end', values=values, tags=(tag,))
