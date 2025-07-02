import bpy
from bpy.props import PointerProperty
from . import CONFIG
from ..helpers import get_property_type


class TraitBlenderConfig(bpy.types.PropertyGroup):
    """Base class for all TraitBlender configuration property groups."""
    
    def __str__(self):
        """Recursively display all parameters and their values in YAML format."""
        return self._to_yaml()
    
    def _to_yaml(self, indent_level=0, parent_path=""):
        """Convert the configuration to YAML format with proper indentation."""
        result = []
        indent = "  " * indent_level
        missing_any = False
        
        # Get all properties of this class
        for prop_name in self.__class__.__annotations__.keys():
            try:
                prop_value = getattr(self, prop_name)
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
                    
                    # Add toggle properties for each TraitBlenderConfig section
                    for prop_name in cls.__annotations__.keys():
                        if isinstance(cls.__annotations__[prop_name], type) and issubclass(cls.__annotations__[prop_name], TraitBlenderConfig):
                            toggle_prop_name = f"show_{prop_name}"
                            new_dict[toggle_prop_name] = bpy.props.BoolProperty(
                                name=f"Show {prop_name.replace('_', ' ').title()}",
                                description=f"Show/hide the {prop_name.replace('_', ' ')} configuration section",
                                default=False
                            )
                    
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