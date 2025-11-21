"""
Helper module for determining property dimensions.
Automatically determines the 'n' parameter for samplers based on property type.
"""

import sys
import os


def get_property_dimension(property_path):
    """
    Get the dimension of a property (determines the 'n' parameter).
    
    Args:
        property_path: Relative property path (e.g., 'camera.location', 'world.color')
        
    Returns:
        int or None: The dimension (length) of the property if it's a vector, None if scalar
        
    Examples:
        - 'lamp.power' (FloatProperty) → None (scalar)
        - 'camera.location' (FloatVectorProperty, length 3) → 3
        - 'world.color' (FloatVectorProperty, length 4) → 4
    """
    try:
        # Try to import from TraitBlender
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        import bpy
        from core.helpers.property_type_checker import get_property_type
        
        # Get the property type
        prop_type = get_property_type(property_path, in_config=True)
        
        if prop_type is None:
            return None
        
        # If it's a vector property, get its length
        if 'Vector' in prop_type:
            # Evaluate the property to get its actual value and length
            full_path = f"bpy.context.scene.traitblender_config.{property_path}"
            try:
                value = eval(full_path, {"bpy": bpy})
                if hasattr(value, '__len__') and not isinstance(value, str):
                    return len(value)
            except Exception as e:
                print(f"Could not evaluate property '{property_path}' to get length: {e}")
                # Default vector lengths based on common patterns
                if 'color' in property_path.lower():
                    return 4  # RGBA
                elif 'location' in property_path.lower() or 'rotation' in property_path.lower():
                    return 3  # XYZ
                else:
                    return 3  # Default 3D vector
        
        # Scalar property - n should be None
        return None
        
    except (ImportError, AttributeError, Exception) as e:
        print(f"Could not determine dimension for '{property_path}': {e}")
        # Return mock dimensions for standalone testing
        return _get_mock_dimension(property_path)


def _get_mock_dimension(property_path):
    """Return mock dimensions for standalone testing."""
    # Common patterns
    if 'color' in property_path.lower():
        return 4  # RGBA
    elif 'location' in property_path.lower():
        return 3  # XYZ
    elif 'rotation' in property_path.lower():
        return 3  # Euler angles
    elif any(scalar in property_path.lower() for scalar in ['power', 'strength', 'focal_length', 'brightness', 'intensity']):
        return None  # Scalar
    else:
        # Default: assume scalar
        return None


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

