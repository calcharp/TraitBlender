"""
TraitBlender UI Module

Contains all user interface components including operators and panels.
"""

# Don't import submodules explicitly to avoid exposing them globally
# Import specific classes only when needed
from . import operators

from .panels import (
    TRAITBLENDER_PT_main_panel,
)

from . import properties
from . import panels

__all__ = [
    # Operators
    "register",
    "unregister",
]

def register():
    properties.register()
    operators.register()
    panels.register()


def unregister():
    panels.unregister()
    properties.unregister()
    operators.unregister()
