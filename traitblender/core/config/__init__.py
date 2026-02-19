# TraitBlender Config Module

from .registration import CONFIG, config_subsection_register, config_register
from .traitblender_config import TraitBlenderConfig

# Import config templates to ensure decorators are executed
from .templates import configs

__all__ = ["CONFIG", "config_subsection_register", "config_register", "configs", "TraitBlenderConfig"]
