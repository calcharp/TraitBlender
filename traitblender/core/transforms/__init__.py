"""
TraitBlender Transforms Module

Transform factory system for morphological operations.
"""

from .transforms import (
    TransformFactory,
    transform_factory,
    register_transform,
    clear_scene,
    lighting_setup,
)

__all__ = [
    "TransformFactory",
    "transform_factory", 
    "register_transform",
    "clear_scene",
    "lighting_setup",
] 