# Dataset Management

For Pandas documentation, see: [Pandas Documentation](https://pandas.pydata.org/docs/)

For DearPyGUI documentation, see: [DearPyGUI Documentation](https://dearpygui.readthedocs.io/)

---

## Overview

The Dataset Management system provides a pandas-like interface for working with morphological trait data in Blender. It handles CSV/Excel file import, provides intuitive data access methods, and includes an interactive DearPyGUI-based editor for viewing and modifying datasets.

**Key Features:**

- **Pandas-Like Interface**: Familiar `loc()`, `iloc()`, `head()`, `tail()` methods
- **Automatic Species Detection**: Finds and prioritizes species/label columns
- **Multiple File Formats**: CSV, TSV, Excel (.xlsx, .xls)
- **Interactive Editor**: DearPyGUI-based CSV viewer with filtering, sorting, editing
- **Blender Integration**: Dataset stored as CSV string in scene properties
- **Morphospace Mapping**: Automatic parameter mapping from dataset columns to morphospace functions

---
## How Datasets are Stored in TraitBlender

Blender cannot natively store pandas DataFrames in PropertyGroups. To work around this, TraitBlender uses `TRAITBLENDER_PG_dataset` (in `core/datasets/traitblender_dataset.py`), a PropertyGroup subclass that stores a string representation of the DataFrame internally, but provides a pandas-like interface for reading and writing data. The DataFrame is reconstructed from the CSV string on each access, converted back to a string when modified, and serialized with the `.blend` file.

**Performance considerations:** This approach is inefficient for large-scale operations since the DataFrame is rebuilt on every access. However, TraitBlender's intended use cases don't require high-performance data manipulation:

- **Viewing large datasets**: Users can browse and inspect datasets without modifying them. Changes only persist if explicitly saved via the DearPyGUI editor.
- **Small datasets and exploration**: Users can make small changes or add new rows to explore how morphospaces work without needing to generate entire external datasets. This is especially useful for testing a few specimens without the overhead of external dataset creation and import.

The string-based storage also ensures datasets persist across Blender sessions, making it easy to save scene configurations with their associated data.

**Core properties:**

- `csv` - Stores the entire dataset as a CSV string. Automatically updates sample selection when changed.
- `filepath` - Path to the dataset file. Setting this triggers automatic import (supports CSV, TSV, and Excel formats).
- `sample` - Dynamic enum populated with row names (species/specimen identifiers) from the dataset.

**Species column detection:** The system automatically detects and reorders species/label columns during import. It recognizes column names like `species`, `label`, `tips`, `sample`, `name`, or `id` (case-insensitive), moves the first matching column to position zero, and sets it as the DataFrame index.

**Internal DataFrame management:** The `_get_dataframe()` method converts the CSV string to a pandas DataFrame with proper indexing. The DataFrame is reconstructed on each call (not cached), ensuring data is always fresh but potentially slower for large datasets.

### Data Access Methods

The PropertyGroup provides familiar pandas-like methods for data access:

**`loc(row_label, column_label=None)`** and **`iloc(row_index, column_index=None)`** - Access rows and columns by label or position. Support standard pandas indexing patterns including bracket notation for multiple rows.

**`head(n=5)`** and **`tail(n=5)`** - Return the first or last n rows as a DataFrame for quick inspection.

**`colnames`**, **`rownames`**, and **`shape`** - Properties that return column names, row names (species identifiers), and dataset dimensions `(rows, columns)`.

**`__str__()`**, **`__len__()`**, and **`__iter__()`** - Special methods enabling `print(dataset)`, `len(dataset)`, and `for col in dataset` operations.

---

## CSV Viewer System

Interactive dataset editor built with DearPyGUI in `core/datasets/dpg_dataset_editor/`. The viewer provides filtering, sorting, pagination, and editing capabilities for viewing and modifying datasets outside of Blender's normal UI.

**Architecture:** The system is organized into four manager classes that coordinate to provide the viewing experience:

- **DataManager** (`data_manager.py`) - Maintains `df_original` (unmodified data) and `df_display` (filtered/sorted view). Handles loading from CSV strings and exporting back to strings.
- **FilterManager** (`filter_manager.py`) - Tracks active filters and applies case-insensitive substring matching. Multiple filters combine with AND logic. Resets pagination when filters change.
- **TableManager** (`table_manager.py`) - Handles pagination (50 rows per page), sorting (click headers to toggle), and rendering the visible page slice.
- **UIManager** (`ui_manager.py`) - Creates the DearPyGUI interface with toolbar, filter section, table display, and pagination controls.

**Integration:** The `launch_csv_viewer_with_string()` function in `csv_viewer.py` is the main entry point. It accepts a CSV string from Blender, launches the viewer window (blocking until closed), and returns the modified CSV string if the user checked "Export Changes", otherwise returns `None`. Operators call this function and update the dataset only if changes were exported.

---

## Common Operations

### Import Dataset

```python
dataset = bpy.context.scene.traitblender_dataset

# Import from file (auto-detects format)
dataset.filepath = "/path/to/dataset.csv"

# Check import success
if dataset.csv:
    print(f"Loaded {len(dataset)} rows, {len(dataset.colnames)} columns")
```

### Access Data

```python
# Get all data for a species
row = dataset.loc("SpeciesName")
print(row)

# Get specific parameter
value = dataset.loc("SpeciesName", "parameter_name")

# Get first 5 rows
print(dataset.head(5))

# Iterate over all species
for species_name in dataset.rownames:
    row_data = dataset.loc(species_name)
    print(f"{species_name}: {row_data['trait1']}")
```

### Dataset Metadata

```python
# Get column names
columns = dataset.colnames

# Get row names (species)
species = dataset.rownames

# Get shape
rows, cols = dataset.shape

# Get length
num_specimens = len(dataset)
```

### Edit Dataset

```python
# Launch CSV viewer
bpy.ops.traitblender.edit_dataset()

# User edits in DearPyGUI window
# If "Export Changes" checked → dataset.csv updated automatically
```

### Morphospace Integration

```python
# Get parameters for morphospace generation
setup = bpy.context.scene.traitblender_setup
dataset = bpy.context.scene.traitblender_dataset

# Select morphospace and sample
setup.available_morphospaces = "CO_Raup"
dataset.sample = "SpeciesName"

# Get row data
row_data = dataset.loc(dataset.sample)

# Parameters automatically mapped to morphospace function
# Column names → lowercase, spaces → underscores
# e.g., "Growth Rate" → "growth_rate"
```

---