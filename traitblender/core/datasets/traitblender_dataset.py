import bpy
from bpy.props import StringProperty, EnumProperty


class TRAITBLENDER_PG_dataset(bpy.types.PropertyGroup):
    """Property group for TraitBlender dataset management."""
    
    csv: StringProperty(
        name="CSV Data",
        description="CSV dataset content as string",
        default=""
    )
    
    ext: EnumProperty(
        name="File Format",
        description="File format for the dataset",
        items=[
            ('csv', "CSV", "Comma-separated values"),
            ('tsv', "TSV", "Tab-separated values"),
            ('excel', "Excel", "Excel spreadsheet (.xlsx)")
        ],
        default='csv'
    )
    
    filepath: StringProperty(
        name="Dataset File",
        description="Path to the dataset file",
        default="",
        subtype='FILE_PATH'
    ) 