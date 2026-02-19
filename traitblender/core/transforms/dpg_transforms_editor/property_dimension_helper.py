"""
Helper module for determining property dimensions.
All transformable paths are now univariate (scalar).
"""


def get_property_dimension(property_path):
    """
    Get the dimension of a property (determines the 'n' parameter for vectors).
    
    Returns:
        int or None: Size if vector, None if scalar. All paths are scalar now.
    """
    return None  # All paths are univariate


def should_auto_set_n_parameter(property_path):
    """
    Determine if the 'n' parameter should be automatically set for this property.
    
    Args:
        property_path: Relative property path
        
    Returns:
        tuple: (should_auto_set: bool, dimension: int or None)
    """
    dimension = get_property_dimension(property_path)
    
    if dimension is not None:
        # Vector property - auto-set n to its dimension
        return True, dimension
    else:
        # Scalar property - leave n as None (don't show in UI)
        return False, None

