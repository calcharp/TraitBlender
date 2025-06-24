# TraitBlender Config Module
# Configuration management for TraitBlender 

CONFIG = {}




from .register_config import register

# Import config templates to ensure decorators are executed
from .config_templates import configs

from .register_config import configure_traitblender


__all__ = ["CONFIG", "register", "configure_traitblender", "configs"]