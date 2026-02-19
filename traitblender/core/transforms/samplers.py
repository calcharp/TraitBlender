"""
Transformable paths and sampling functions for the transform pipeline.
"""

import numpy as np


def normal(mu: float, sigma: float) -> float:
    """Univariate normal distribution sampler. Returns a single float."""
    return float(np.random.normal(mu, sigma))


SAMPLERS = {
    "normal": normal,
}

# Sampler name -> list of allowed config paths (all scalar/univariate).
# Config paths resolve to bpy.context.scene.traitblender_config.<path>
# Vector components use x/y/z (position, rotation) or r/g/b/a (color).
SAMPLER_ALLOWED_PATHS = {
    "normal": [
        "world.color.r",
        "world.color.g",
        "world.color.b",
        "world.color.a",
        "world.strength",
        "camera.location.x",
        "camera.location.y",
        "camera.location.z",
        "camera.rotation.x",
        "camera.rotation.y",
        "camera.rotation.z",
        "camera.focal_length",
        "camera.shift_x",
        "camera.shift_y",
        "lamp.location.x",
        "lamp.location.y",
        "lamp.location.z",
        "lamp.rotation.x",
        "lamp.rotation.y",
        "lamp.rotation.z",
        "lamp.color.r",
        "lamp.color.g",
        "lamp.color.b",
        "lamp.power",
        "mat.location.x",
        "mat.location.y",
        "mat.location.z",
        "mat.rotation.x",
        "mat.rotation.y",
        "mat.rotation.z",
        "mat.color.r",
        "mat.color.g",
        "mat.color.b",
        "mat.color.a",
        "mat.roughness",
        "sample.tb_location.x",
        "sample.tb_location.y",
        "sample.tb_location.z",
        "sample.tb_rotation.x",
        "sample.tb_rotation.y",
        "sample.tb_rotation.z",
    ],
}
