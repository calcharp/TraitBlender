import bpy
from bpy.props import PointerProperty
from . import CONFIG


class TraitBlenderConfig(bpy.types.PropertyGroup):
    """Base class for all TraitBlender configuration property groups."""
    
    def __str__(self):
        """Recursively display all parameters and their values with pretty formatting."""
        result = []
        
        # Get all properties of this class
        for i, prop_name in enumerate(self.__class__.__annotations__.keys()):
            prop_value = getattr(self, prop_name)
            
            # If it's another TraitBlenderConfig, recurse
            if isinstance(prop_value, TraitBlenderConfig):
                # Add blank line before new section (except for the first one)
                if i > 0:
                    result.append("")
                
                # Indent the nested config and remove the class name header
                nested_str = str(prop_value).replace('\n', '\n    ')
                result.append(f"{prop_name}:")
                result.append(f"    {nested_str}")
            else:
                # Handle different property types
                if hasattr(prop_value, '__iter__') and not isinstance(prop_value, str):
                    # For vectors, arrays, etc. - convert to tuple/list
                    try:
                        display_value = tuple(prop_value)
                    except:
                        display_value = prop_value
                else:
                    display_value = prop_value
                
                result.append(f"  {prop_name}: {display_value}")
        
        return '\n'.join(result)

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
                    new_cls = type(
                        cls.__name__,
                        (TraitBlenderConfig,),
                        {
                            '__module__': cls.__module__,
                            '__doc__': cls.__doc__,
                            '__annotations__': cls.__annotations__
                        }
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