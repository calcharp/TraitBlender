"""
Helpers for optional third-party dependencies.

In particular, this add-on can ship a "headless" build that intentionally omits
DearPyGui. We must therefore avoid importing/registration paths that depend
on DearPyGui at add-on register time.
"""

from __future__ import annotations


def is_dearpygui_available() -> bool:
    """Return True if `dearpygui` can be imported."""

    try:
        import dearpygui.dearpygui  # noqa: F401

        return True
    except Exception:
        return False

