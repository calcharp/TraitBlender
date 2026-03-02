"""Orientation functions for shell specimens."""

from .orient_helpers import _orient_default, _orient_geometric_center_xflipped, _orient_default_xminus90

ORIENTATIONS = {
    "Default": _orient_default,
    "Flipped": _orient_geometric_center_xflipped,
    "Aperture View": _orient_default_xminus90,
}

__all__ = ['ORIENTATIONS']
