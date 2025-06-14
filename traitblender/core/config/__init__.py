# TraitBlender Config Module
# Configuration management for TraitBlender 

CONFIG = {}

from .register_config import register_config

__all__ = ["CONFIG", "register_config"]