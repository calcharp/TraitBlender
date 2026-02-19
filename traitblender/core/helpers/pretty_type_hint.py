"""
Pretty-print Python type hints for display (e.g. dict[str, int] instead of repr).
"""

import typing


def pretty_type_hint(type_hint):
    """
    Convert a type hint to a readable string (e.g. list[int], dict[str, float]).

    Args:
        type_hint: A typing type hint (e.g. list[int], Optional[str])

    Returns:
        str: Human-readable representation of the type
    """
    origin = typing.get_origin(type_hint)  # e.g. list for list[int]
    args = typing.get_args(type_hint)     # e.g. (int,) for list[int]

    if origin is None:
        # Simple type (int, str, etc.)
        return type_hint.__name__ if hasattr(type_hint, '__name__') else str(type_hint)
    elif args:
        # Generic with args (list[int], dict[str, float])
        args_str = ", ".join(pretty_type_hint(arg) for arg in args)
        return f"{origin.__name__}[{args_str}]"
    else:
        # Generic without args
        return str(type_hint) 