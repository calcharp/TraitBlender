import bpy
from bpy.props import PointerProperty
from . import CONFIG


class TraitBlenderConfig(bpy.types.PropertyGroup):
    """Base class for all TraitBlender configuration property groups."""
    
    def __str__(self):
        """Recursively display all parameters and their values in YAML format."""
        return self._to_yaml()
    
    def _to_yaml(self, indent_level=0):
        """Convert the configuration to YAML format with proper indentation."""
        result = []
        indent = "  " * indent_level
        
        # Get all properties of this class
        for prop_name in self.__class__.__annotations__.keys():
            prop_value = getattr(self, prop_name)
            
            # If it's another TraitBlenderConfig, recurse
            if isinstance(prop_value, TraitBlenderConfig):
                result.append(f"{indent}{prop_name}:")
                nested_yaml = prop_value._to_yaml(indent_level + 1)
                if nested_yaml.strip():  # Only add if there's content
                    result.append(nested_yaml)
            else:
                # Handle different property types for YAML
                yaml_value = self._format_value_for_yaml(prop_value)
                result.append(f"{indent}{prop_name}: {yaml_value}")
        
        return '\n'.join(result)
    
    def _format_value_for_yaml(self, value):
        """Format a value appropriately for YAML output."""
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            # Quote strings that contain special characters or are empty
            if not value or any(char in value for char in '":{}[]&*#?|-<>=!%@`,\'\\'):
                return f'"{value}"'
            return value
        elif hasattr(value, '__iter__') and not isinstance(value, str):
            # Handle lists, tuples, vectors, etc.
            try:
                if len(value) == 0:
                    return "[]"
                elif len(value) == 1:
                    return f"[{self._format_value_for_yaml(value[0])}]"
                else:
                    items = [self._format_value_for_yaml(item) for item in value]
                    return f"[{', '.join(items)}]"
            except (TypeError, IndexError) as e:
                # Fallback for non-indexable iterables
                import traceback
                print(f"Warning: Error formatting iterable value {value} (type: {type(value)}): {e}")
                print(f"Traceback: {traceback.format_exc()}")
                return str(value)
        else:
            return str(value)
    
    def from_dict(self, data_dict):
        """
        Load configuration values from a dictionary.
        
        Args:
            data_dict (dict): Dictionary containing configuration values.
                             Can contain nested dictionaries for nested TraitBlenderConfig objects.
        """
        if not isinstance(data_dict, dict):
            raise ValueError("Input must be a dictionary")
        
        for prop_name, value in data_dict.items():
            print(f"Property {prop_name} value: {value}")
            # Check if this property exists in the class annotations
            if prop_name not in self.__class__.__annotations__:
                print(f"Warning: Property '{prop_name}' not found in {self.__class__.__name__}")
                continue
            
            # Get the current property value
            current_prop = getattr(self, prop_name)
            print(f"Current property {prop_name} value: {current_prop}")
            
            # If the current property is a TraitBlenderConfig and the value is a dict, recurse
            if isinstance(current_prop, TraitBlenderConfig) and isinstance(value, dict):
                current_prop.from_dict(value)
                print(f"Current property {prop_name} value: {current_prop}")
            else:
                # For simple properties, just set the value directly
                try:
                    setattr(self, prop_name, value)
                    print(f"Property {prop_name} value: {getattr(self, prop_name)}")
                except Exception as e:
                    print(f"Warning: Could not set property '{prop_name}' to value '{value}': {e}")
    
    def to_dict(self):
        """
        Convert the configuration to a dictionary.
        
        Returns:
            dict: Dictionary representation of the configuration.
        """
        result = {}
        
        for prop_name in self.__class__.__annotations__.keys():
            prop_value = getattr(self, prop_name)
            print(f"Property {prop_name} value: {prop_value}")
            
            # If it's another TraitBlenderConfig, recurse
            if isinstance(prop_value, TraitBlenderConfig):
                result[prop_name] = prop_value.to_dict()
                print(type(prop_value))
                print(f"Property {prop_name} value: {result[prop_name]}")
            else:
                # For simple properties, convert to a serializable format
                if hasattr(prop_value, '__iter__') and not isinstance(prop_value, str):
                    try:
                        result[prop_name] = list(prop_value)
                        print(f"Property {prop_name} value: {result[prop_name]}")
                    except Exception as e:
                        result[prop_name] = str(prop_value)
                        print(f"Unable to convert {prop_name} to {prop_value}/ Exception: {e}")
                else:
                    result[prop_name] = prop_value
                    print(f"Property {prop_name} value: {result[prop_name]}")
        
        return result

def register(name: str):

    """
    Decorator to register a class as a property of the CONFIG dictionary. 
    It will convert the class to inherit from TraitBlenderConfig if it does not already do so.
    """
    def decorator(cls):
        try:
            # Convert the class to inherit from TraitBlenderConfig
            if not issubclass(cls, TraitBlenderConfig):
                # Create a new class that inherits from TraitBlenderConfig
                # and has all the same properties as the original class
                if not issubclass(cls, bpy.types.PropertyGroup):
                    raise ValueError(f"Class {cls.__name__} does not inherit from bpy.types.PropertyGroup")
                
                try:
                    # Copy all attributes from the original class, including property definitions
                    new_dict = {
                        '__module__': cls.__module__,
                        '__doc__': cls.__doc__,
                        '__annotations__': cls.__annotations__
                    }
                    
                    # Copy all property definitions from the original class
                    for attr_name in dir(cls):
                        if not attr_name.startswith('_'):
                            attr_value = getattr(cls, attr_name)
                            if hasattr(attr_value, '__class__') and 'Property' in attr_value.__class__.__name__:
                                new_dict[attr_name] = attr_value
                    
                    new_cls = type(
                        cls.__name__,
                        (TraitBlenderConfig,),
                        new_dict
                    )
                    cls = new_cls
                    print(f"Class {cls.__name__} converted to {new_cls}")
                except Exception as e:
                    print(f"Error creating new class: {e}")

            bpy.utils.register_class(cls)
            print(f"Registered {name} as {cls.__name__}")
            CONFIG[name] = PointerProperty(type=cls)
            print(f"CONFIG[{name}] = {CONFIG[name]}")
        except Exception as e:
            print(f"(decorator exception) Error registering {name}: {e}")
        return cls
    return decorator

def configure_traitblender():
    dyn_class = type(
        "TraitBlenderConfig",
        (TraitBlenderConfig,), 
        {"__annotations__": CONFIG}
    )
    bpy.utils.register_class(dyn_class)
    bpy.types.Scene.traitblender_config = bpy.props.PointerProperty(type=dyn_class)
    print("TraitBlenderConfig registered")