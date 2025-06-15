"""
TraitBlender UI Panels

Contains all panel classes for the TraitBlender add-on.
Panels define the user interface layout and elements.
"""

# Import all panel classes here
from .main_panel import TRAITBLENDER_PT_main_panel
from .camera_panel import TRAITBLENDER_PT_camera_panel

__all__ = [
    "TRAITBLENDER_PT_main_panel",
    "TRAITBLENDER_PT_camera_panel",
] 