"""
Blender version differences: Eevee render.engine enum id varies (BLENDER_EEVEE_NEXT vs BLENDER_EEVEE).
"""

from __future__ import annotations

import bpy


def _engine_enum_identifiers() -> list[str]:
    try:
        prop = bpy.types.RenderSettings.bl_rna.properties["engine"]
        return [item.identifier for item in prop.enum_items]
    except Exception:
        return []


def get_eevee_engine_identifier() -> str:
    ids = set(_engine_enum_identifiers())
    if "BLENDER_EEVEE_NEXT" in ids:
        return "BLENDER_EEVEE_NEXT"
    if "BLENDER_EEVEE" in ids:
        return "BLENDER_EEVEE"
    return "BLENDER_EEVEE"


def render_engine_enum_items() -> list[tuple[str, str, str]]:
    eevee = get_eevee_engine_identifier()
    return [
        ("CYCLES", "Cycles", "Cycles"),
        (eevee, "Eevee", "Eevee"),
        ("BLENDER_WORKBENCH", "Workbench", "Workbench"),
    ]


def render_engine_options() -> list[str]:
    return [item[0] for item in render_engine_enum_items()]


def normalize_render_engine_value(value) -> str:
    """
    Map a config/YAML engine value to a valid bpy.context.scene.render.engine identifier
    for this Blender build.
    """
    ids = _engine_enum_identifiers()
    avail = set(ids)
    eevee = get_eevee_engine_identifier()
    ordered = ["CYCLES", eevee, "BLENDER_WORKBENCH"]

    if isinstance(value, int):
        if 0 <= value < len(ordered):
            candidate = ordered[value]
            return candidate if candidate in avail else (ordered[0] if ordered[0] in avail else ids[0])
        return eevee if eevee in avail else "CYCLES"

    s = str(value).strip()
    if s in avail:
        return s
    if s == "BLENDER_EEVEE_NEXT" and "BLENDER_EEVEE" in avail:
        return "BLENDER_EEVEE"
    if s == "BLENDER_EEVEE" and "BLENDER_EEVEE_NEXT" in avail:
        return "BLENDER_EEVEE_NEXT"
    if eevee in avail:
        return eevee
    return "CYCLES" if "CYCLES" in avail else (ids[0] if ids else "CYCLES")
