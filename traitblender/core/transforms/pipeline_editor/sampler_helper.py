"""
Helper module for sampler parameter information.
Uses hardcoded signatures for supported samplers.
"""

import inspect


def get_sampler_signature(sampler_name):
    """
    Get the parameter signature for a sampler function.
    
    Returns:
        dict: Parameter info per param name (type_str, default, required)
    """
    try:
        from ..transforms import SAMPLERS
        if sampler_name not in SAMPLERS:
            return {}
        func = SAMPLERS[sampler_name]
        sig = inspect.signature(func)
        params = {}
        for name, param in sig.parameters.items():
            params[name] = {
                'type': param.annotation if param.annotation != inspect.Parameter.empty else None,
                'type_str': _format_type_hint(param.annotation),
                'default': param.default if param.default != inspect.Parameter.empty else None,
                'required': param.default == inspect.Parameter.empty,
                'annotation': param.annotation
            }
        return params
    except (ImportError, AttributeError, Exception):
        return _get_mock_signature(sampler_name)


def _format_type_hint(annotation):
    """Format a type annotation to a readable string."""
    if annotation == inspect.Parameter.empty:
        return 'unknown'
    
    # Handle type hints
    type_str = str(annotation)
    
    # Clean up common patterns
    type_str = type_str.replace('typing.', '')
    type_str = type_str.replace("<class '", "").replace("'>", "")
    
    # Handle special cases
    if 'list[float]' in type_str.lower():
        return 'list[float]'
    elif 'list[int]' in type_str.lower():
        return 'list[int]'
    elif 'float' in type_str.lower():
        return 'float'
    elif 'int' in type_str.lower():
        return 'int'
    elif 'str' in type_str.lower():
        return 'str'
    elif 'bool' in type_str.lower():
        return 'bool'
    
    return type_str


def _get_mock_signature(sampler_name):
    """Return parameter signatures (fallback when transforms not importable)."""
    signatures = {
        'normal': {
            'mu': {'type': float, 'type_str': 'float', 'default': None, 'required': True},
            'sigma': {'type': float, 'type_str': 'float', 'default': None, 'required': True},
        },
    }
    return signatures.get(sampler_name, {})


def validate_parameter_value(value_str, type_str):
    """
    Validate and convert a parameter value string based on its expected type.
    
    Args:
        value_str: String value from input field
        type_str: Expected type ('float', 'int', 'list[float]', 'list[int]')
        
    Returns:
        tuple: (success: bool, converted_value or error_message)
    """
    if not value_str or value_str.strip() == '':
        return False, "Value cannot be empty"
    
    value_str = value_str.strip()
    
    try:
        if type_str == 'float':
            return True, float(value_str)
        
        elif type_str == 'int':
            return True, int(value_str)
        
        elif type_str == 'bool':
            lower = value_str.lower()
            if lower in ('true', '1', 'yes'):
                return True, True
            elif lower in ('false', '0', 'no'):
                return True, False
            else:
                return False, "Boolean must be true/false"
        
        elif type_str == 'str':
            return True, value_str
        
        elif type_str == 'list[float]':
            # Parse comma-separated floats or JSON-like list
            value_str = value_str.strip('[]')
            parts = [p.strip() for p in value_str.split(',')]
            values = [float(p) for p in parts if p]
            return True, values
        
        elif type_str == 'list[int]':
            # Parse comma-separated ints
            value_str = value_str.strip('[]')
            parts = [p.strip() for p in value_str.split(',')]
            values = [int(p) for p in parts if p]
            return True, values
        
        else:
            return False, f"Unknown type: {type_str}"
    
    except ValueError as e:
        return False, f"Invalid {type_str}: {e}"
    except Exception as e:
        return False, f"Parse error: {e}"


def format_parameter_value(value):
    """
    Format a parameter value for display in an input field.
    
    Args:
        value: The parameter value (scalar or list)
        
    Returns:
        str: Formatted string for display
    """
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return ", ".join(str(v) for v in value)
    return str(value)

