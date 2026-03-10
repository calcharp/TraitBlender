"""
Decorator to register a config subsection class.
"""

import bpy
from ..traitblender_config import TraitBlenderConfig

# Mutable dict populated by @config_subsection_register decorator
CONFIG = {}


def config_subsection_register(name: str):
    """
    Decorator to register a class as a property of the CONFIG dictionary.
    Converts the class to inherit from TraitBlenderConfig if it does not already do so.
    """
    def decorator(cls):
        try:
            if not issubclass(cls, TraitBlenderConfig):
                if not issubclass(cls, bpy.types.PropertyGroup):
                    raise ValueError(f"Class {cls.__name__} does not inherit from bpy.types.PropertyGroup")

                try:
                    new_dict = {
                        '__module__': cls.__module__,
                        '__doc__': cls.__doc__,
                        '__annotations__': cls.__annotations__
                    }

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
            CONFIG[name] = bpy.props.PointerProperty(type=cls)
            print(f"CONFIG[{name}] = {CONFIG[name]}")
        except Exception as e:
            print(f"(decorator exception) Error registering {name}: {e}")
        return cls
    return decorator
