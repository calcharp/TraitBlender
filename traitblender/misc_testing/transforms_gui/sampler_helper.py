"""
Helper module for extracting sampler parameter information.
Works both standalone and when integrated with TraitBlender.
"""

import inspect
import sys
import os


def get_sampler_signature(sampler_name):
    """
    Get the parameter signature for a sampler function.
    
    Args:
        sampler_name: Name of the sampler
        
    Returns:
        dict: Parameter information with structure:
        {
            'param_name': {
                'type': type hint (e.g., float, int, list[float]),
                'type_str': string representation (e.g., 'float', 'list[float]'),
                'default': default value or None if required,
                'required': True if no default value,
                'annotation': raw annotation object
            }
        }
    """
    try:
        # Try to import from TraitBlender
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        # Import the registry module to get the original sampler functions
        import core.transforms.registry as registry_module
        
        # Get the original sampler function by its name from the module
        # The decorated functions are defined in the module with names like 'uniform_sampler', 'normal_sampler', etc.
        func_name = f"{sampler_name}_sampler"
        
        if not hasattr(registry_module, func_name):
            print(f"Could not find sampler function '{func_name}' in registry module")
            return {}
        
        # Get the original function (not the factory wrapper)
        original_func = getattr(registry_module, func_name)
        
        # Get signature from the original function
        sig = inspect.signature(original_func)
        
        params = {}
        for name, param in sig.parameters.items():
            param_info = {
                'type': param.annotation if param.annotation != inspect.Parameter.empty else None,
                'type_str': _format_type_hint(param.annotation),
                'default': param.default if param.default != inspect.Parameter.empty else None,
                'required': param.default == inspect.Parameter.empty,
                'annotation': param.annotation
            }
            params[name] = param_info
        
        return params
        
    except (ImportError, AttributeError, Exception) as e:
        print(f"Could not load sampler signature for '{sampler_name}': {e}")
        # Return mock signatures for standalone testing
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
    elif 'list[list[float]]' in type_str.lower():
        return 'list[list[float]]'
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
    """Return mock parameter signatures for standalone testing."""
    mock_signatures = {
        'uniform': {
            'low': {'type': float, 'type_str': 'float', 'default': None, 'required': True},
            'high': {'type': float, 'type_str': 'float', 'default': None, 'required': True},
            'n': {'type': int, 'type_str': 'int', 'default': None, 'required': False}
        },
        'normal': {
            'mu': {'type': float, 'type_str': 'float', 'default': None, 'required': True},
            'sigma': {'type': float, 'type_str': 'float', 'default': None, 'required': True},
            'n': {'type': int, 'type_str': 'int', 'default': None, 'required': False}
        },
        'gamma': {
            'alpha': {'type': float, 'type_str': 'float', 'default': None, 'required': True},
            'beta': {'type': float, 'type_str': 'float', 'default': None, 'required': True},
            'n': {'type': int, 'type_str': 'int', 'default': None, 'required': False}
        },
        'beta': {
            'a': {'type': float, 'type_str': 'float', 'default': None, 'required': True},
            'b': {'type': float, 'type_str': 'float', 'default': None, 'required': True},
            'n': {'type': int, 'type_str': 'int', 'default': None, 'required': False}
        },
        'dirichlet': {
            'alphas': {'type': list[float], 'type_str': 'list[float]', 'default': None, 'required': True},
            'n': {'type': int, 'type_str': 'int', 'default': None, 'required': False}
        },
        'poisson': {
            'lam': {'type': float, 'type_str': 'float', 'default': None, 'required': True},
            'n': {'type': int, 'type_str': 'int', 'default': None, 'required': False}
        },
        'cauchy': {
            'x0': {'type': float, 'type_str': 'float', 'default': None, 'required': True},
            'gamma': {'type': float, 'type_str': 'float', 'default': None, 'required': True},
            'n': {'type': int, 'type_str': 'int', 'default': None, 'required': False}
        },
        'exponential': {
            'lambd': {'type': float, 'type_str': 'float', 'default': None, 'required': True},
            'n': {'type': int, 'type_str': 'int', 'default': None, 'required': False}
        },
        'multivariate_normal': {
            'mu': {'type': list[float], 'type_str': 'list[float]', 'default': None, 'required': True},
            'cov': {'type': list, 'type_str': 'list[list[float]]', 'default': None, 'required': True},
            'n': {'type': int, 'type_str': 'int', 'default': None, 'required': False}
        },
        'discrete_uniform': {
            'low': {'type': int, 'type_str': 'int', 'default': None, 'required': True},
            'high': {'type': int, 'type_str': 'int', 'default': None, 'required': True},
            'n': {'type': int, 'type_str': 'int', 'default': None, 'required': False}
        },
    }
    
    return mock_signatures.get(sampler_name, {})


def validate_parameter_value(value_str, type_str):
    """
    Validate and convert a parameter value string based on its expected type.
    
    Args:
        value_str: String value from input field
        type_str: Expected type ('float', 'int', 'list[float]', 'list[list[float]]')
        
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
        
        elif type_str == 'list[list[float]]':
            # Parse nested list (simple JSON-like format)
            # Expected format: [[1,2,3],[4,5,6]]
            import json
            try:
                values = json.loads(value_str)
                # Validate structure
                if not isinstance(values, list):
                    return False, "Must be a list of lists"
                for row in values:
                    if not isinstance(row, list):
                        return False, "Must be a list of lists"
                    for val in row:
                        float(val)  # Ensure can convert to float
                return True, values
            except json.JSONDecodeError:
                return False, "Invalid JSON format. Use [[1,2],[3,4]]"
        
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
        value: The parameter value (can be scalar, list, or nested list)
        
    Returns:
        str: Formatted string for display
    """
    if value is None:
        return ""
    
    if isinstance(value, (list, tuple)):
        # Check if nested list
        if value and isinstance(value[0], (list, tuple)):
            # Nested list - use JSON format
            import json
            return json.dumps(value)
        else:
            # Simple list - comma separated
            return ", ".join(str(v) for v in value)
    
    return str(value)

