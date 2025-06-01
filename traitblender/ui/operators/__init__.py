"""
TraitBlender UI Operators

Contains all operator classes for the TraitBlender add-on.
Operators handle user actions and commands.
"""

# Import all operator classes here
from .setup_scene_operator import TRAITBLENDER_OT_setup_scene

__all__ = [
    "TRAITBLENDER_OT_setup_scene",
] 