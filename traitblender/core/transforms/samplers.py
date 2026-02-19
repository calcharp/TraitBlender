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
# Vector props use numeric indices: location.0, location.1, location.2; color.0, color.1, color.2, color.3
SAMPLER_ALLOWED_PATHS = {
    "normal": [
        "world.color.0",
        "world.color.1",
        "world.color.2",
        "world.color.3",
        "world.strength",
        "camera.location.0",
        "camera.location.1",
        "camera.location.2",
        "camera.rotation.0",
        "camera.rotation.1",
        "camera.rotation.2",
        "camera.focal_length",
        "camera.shift_x",
        "camera.shift_y",
        "lamp.location.0",
        "lamp.location.1",
        "lamp.location.2",
        "lamp.rotation.0",
        "lamp.rotation.1",
        "lamp.rotation.2",
        "lamp.color.0",
        "lamp.color.1",
        "lamp.color.2",
        "lamp.power",
        "mat.location.0",
        "mat.location.1",
        "mat.location.2",
        "mat.rotation.0",
        "mat.rotation.1",
        "mat.rotation.2",
        "mat.color.0",
        "mat.color.1",
        "mat.color.2",
        "mat.color.3",
        "mat.roughness",
    ],
}
