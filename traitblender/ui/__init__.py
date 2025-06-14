"""
TraitBlender UI Module

Contains all user interface components including operators and panels.
"""

# Don't import submodules explicitly to avoid exposing them globally
# Import specific classes only when needed
from .operators import TRAITBLENDER_OT_setup_scene
from .panels import TRAITBLENDER_PT_main_panel

__all__ = [
    "TRAITBLENDER_OT_setup_scene",
    "TRAITBLENDER_PT_main_panel",
]
