"""
Config registration submodule.
"""

from .config_subsection_register import CONFIG, config_subsection_register
from .config_register import config_register

__all__ = ["CONFIG", "config_subsection_register", "config_register"]
