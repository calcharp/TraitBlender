import typing

def pretty_type_hint(type_hint):
    origin = typing.get_origin(type_hint)
    args = typing.get_args(type_hint)
    if origin is None:
        return type_hint.__name__ if hasattr(type_hint, '__name__') else str(type_hint)
    elif args:
        args_str = ", ".join(pretty_type_hint(arg) for arg in args)
        return f"{origin.__name__}[{args_str}]"
    else:
        return str(type_hint) 