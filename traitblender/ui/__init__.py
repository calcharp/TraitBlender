"""
TraitBlender UI Module

Contains all user interface components including operators and panels.
"""

# Don't import submodules explicitly to avoid exposing them globally
# Import specific classes only when needed
from . import operators

from .panels import (
    TRAITBLENDER_PT_main_panel,
    register as register_panels,
    unregister as unregister_panels,
)

from . import properties

__all__ = [
    # Operators
    "register",
    "unregister",

    # Panels
    "TRAITBLENDER_PT_main_panel",

]

def register():
    properties.register()
    operators.register()
    register_panels()


def unregister():
    unregister_panels()
    properties.unregister()
    operators.unregister()
