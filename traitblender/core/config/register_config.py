import bpy
from bpy.props import PointerProperty
from . import CONFIG
from ..helpers import get_property_type


class TraitBlenderConfig(bpy.types.PropertyGroup):
    """Base class for all TraitBlender configuration property groups."""
    
    show: bpy.props.BoolProperty(
        name="Show",
        description="Show this section in the UI",
        default=False
    )
    
    def __str__(self):
        """Recursively display all parameters and their values in YAML format."""
        return self._to_yaml()
    
    def _to_yaml(self, indent_level=0, parent_path=""):
        """Convert the configuration to YAML format with proper indentation."""
        result = []
        indent = "  " * indent_level
        missing_any = False
        
        # Add YAML document start marker at the top level
        if indent_level == 0:
            result.append('---')
        
        # Collect all properties with their print_index values for sorting
        properties_to_sort = []
        
        for prop_name in self.__class__.__annotations__.keys():
            if prop_name == "show":
                continue  # Skip the show property
            try:
                prop_value = getattr(self, prop_name)
                # Get print_index if it exists, otherwise use a large number to put it at the end
                print_index = getattr(prop_value, 'print_index', float('inf')) if hasattr(prop_value, 'print_index') else float('inf')
                properties_to_sort.append((print_index, prop_name, prop_value))
            except Exception:
                # If we can't get the property, still include it but with no print_index
                properties_to_sort.append((float('inf'), prop_name, None))
        
        # Sort properties: first by print_index, then alphabetically within same index
        properties_to_sort.sort(key=lambda x: (x[0], x[1]))
        
        # Process sorted properties
        for print_index, prop_name, prop_value in properties_to_sort:
            try:
                if prop_value is None:
                    # Property couldn't be accessed earlier
                    result.append(f"{indent}{prop_name}: # missing required Blender objects")
                    missing_any = True
                    continue
                
                # If it's another TraitBlenderConfig, recurse
                if isinstance(prop_value, TraitBlenderConfig):
                    result.append(f"{indent}{prop_name}:")
                    # Build the path for nested properties
                    current_path = f"{parent_path}.{prop_name}" if parent_path else prop_name
                    nested_yaml = prop_value._to_yaml(indent_level + 1, current_path)
                    if nested_yaml.strip():  # Only add if there's content
                        result.append(nested_yaml)
                else:
                    # Handle different property types for YAML
                    # Build the full property path for type checking
                    current_path = f"{parent_path}.{prop_name}" if parent_path else prop_name
                    prop_type = get_property_type(current_path)
                    yaml_value = self._format_value_for_yaml(prop_value, prop_type)
                    result.append(f"{indent}{prop_name}: {yaml_value}")
            except Exception:
                result.append(f"{indent}{prop_name}: # missing required Blender objects")
                missing_any = True
        
        yaml_str = '\n'.join(result)
        if indent_level == 0 and missing_any:
            yaml_str += ("\n\n[TraitBlender] Some configuration values are missing. "
                         "To fix this, run the following in the Blender Python console to set up the scene:\n"
                         "    bpy.ops.traitblender.setup_scene()\n"
                         "This will create any required objects (such as Camera, World, etc.) that are missing.")
        return yaml_str
    
    def _format_value_for_yaml(self, value, prop_type=None):
        """Format a value appropriately for YAML output."""
        if value is None:
            return "null"
        
        # Use property type to determine formatting (esp for vectors)
        if prop_type in ['FloatVectorProperty', 'IntVectorProperty', 'BoolVectorProperty']:
            # Convert vector properties to list format
            try:
                items = [str(item) for item in value]
                return f"[{', '.join(items)}]"
            except:
                return str(value)
        elif prop_type == 'EnumProperty':
            # Enums should be strings
            return str(value)
        elif prop_type in ['FloatProperty', 'IntProperty']:
            # Simple numeric properties
            return str(value)
        elif prop_type == 'BoolProperty':
            # Boolean properties
            return str(value).lower()
        elif prop_type == 'StringProperty':
            # String properties - quote if needed
            if not value or any(char in value for char in '":{}[]&*#?|-<>=!%@`,\'\\'):
                return f'"{value}"'
            return value
        else:
            # Fallback for unknown types
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
            if prop_name not in self.__class__.__annotations__:
                continue
            current_prop = getattr(self, prop_name)
            if isinstance(current_prop, TraitBlenderConfig) and isinstance(value, (dict, list)):
                current_prop.from_dict(value)
            else:
                try:
                    setattr(self, prop_name, value)
                except Exception:
                    pass
    
    def to_dict(self):
        """
        Convert the configuration to a dictionary.
        
        Returns:
            dict: Dictionary representation of the configuration.
        """
        result = {}
        
        for prop_name in self.__class__.__annotations__.keys():
            if prop_name == "show":
                continue  # Skip the show property
            prop_value = getattr(self, prop_name)
            if isinstance(prop_value, TraitBlenderConfig):
                result[prop_name] = prop_value.to_dict()
            else:
                if hasattr(prop_value, '__iter__') and not isinstance(prop_value, str):
                    try:
                        result[prop_name] = list(prop_value)
                    except Exception:
                        result[prop_name] = str(prop_value)
                else:
                    result[prop_name] = prop_value
        
        return result
    
    def get_config_sections(self):
        """
        Get all nested TraitBlenderConfig sections in this configuration.
        
        Returns:
            dict: Dictionary mapping section names to their TraitBlenderConfig instances
        """
        sections = {}
        
        for prop_name in self.__class__.__annotations__.keys():
            try:
                prop_value = getattr(self, prop_name)
                if isinstance(prop_value, TraitBlenderConfig):
                    sections[prop_name] = prop_value
            except Exception:
                # Skip properties that can't be accessed
                continue
        
        return sections

def register(name: str):

    """
    Decorator to register a class as a property of the CONFIG dictionary. 
    It will convert the class to inherit from TraitBlenderConfig if it does not already do so.
    """
    def decorator(cls):
        try:
            # Convert the class to inherit from TraitBlenderConfig if needed
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