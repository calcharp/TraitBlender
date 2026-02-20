"""Orientation functions for shell specimens."""

from .orient_helpers import _orient_default, _orient_geometric_center_xflipped

ORIENTATIONS = {
    "Default": _orient_default,
    "Flipped": _orient_geometric_center_xflipped,
}

__all__ = ['ORIENTATIONS']
