# TraitBlender Config Module
# Configuration management for TraitBlender 

CONFIG = {}

from .register_config import register, configure_traitblender

__all__ = ["CONFIG", "register", "configure_traitblender"]