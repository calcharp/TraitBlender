"""Circle Grid morphospace: white cube with 16 black circles on top; traits = opacity and diameter (unitless) per circle."""

from .morphospace import CircleGridMorphospace, CircleGridMorphospaceSample

NAME = "Circle Grid"

# No hyperparameters
HYPERPARAMETERS = {}


def _orient_default(sample_obj):
    """Place at table center, no rotation."""
    sample_obj.tb_location = (0.0, 0.0, 0.0)
    sample_obj.tb_rotation = (0.0, 0.0, 0.0)


ORIENTATIONS = {
    "Default": _orient_default,
}


def sample(
    name="CircleGrid",
    opacity_0=1.0,
    opacity_1=1.0,
    opacity_2=1.0,
    opacity_3=1.0,
    opacity_4=1.0,
    opacity_5=1.0,
    opacity_6=1.0,
    opacity_7=1.0,
    opacity_8=1.0,
    opacity_9=1.0,
    opacity_10=1.0,
    opacity_11=1.0,
    opacity_12=1.0,
    opacity_13=1.0,
    opacity_14=1.0,
    opacity_15=1.0,
    diameter_0=0.0,
    diameter_1=0.0,
    diameter_2=0.0,
    diameter_3=0.0,
    diameter_4=0.0,
    diameter_5=0.0,
    diameter_6=0.0,
    diameter_7=0.0,
    diameter_8=0.0,
    diameter_9=0.0,
    diameter_10=0.0,
    diameter_11=0.0,
    diameter_12=0.0,
    diameter_13=0.0,
    diameter_14=0.0,
    diameter_15=0.0,
):
    """
    Generate a Circle Grid sample: white cube (0.29 m × 0.29 m × 1 cm) with 16 black circles
    on the top face in a 4×4 grid.

    Args:
        name: Object name in Blender.
        opacity_0 .. opacity_15: Opacity of each circle (0 = invisible, 1 = black). Row-major 4×4.
        diameter_0 .. diameter_15: Size trait (0 = default 0.03 m; 1 = 2×, 2 = 4×; scale = 2^trait). Values in (0, 0.01) treated as 0 so 0.03 in CSV = default. Row-major 4×4.
    """
    morphospace = CircleGridMorphospace()
    opacities = [
        opacity_0, opacity_1, opacity_2, opacity_3,
        opacity_4, opacity_5, opacity_6, opacity_7,
        opacity_8, opacity_9, opacity_10, opacity_11,
        opacity_12, opacity_13, opacity_14, opacity_15,
    ]
    diameters = [
        diameter_0, diameter_1, diameter_2, diameter_3,
        diameter_4, diameter_5, diameter_6, diameter_7,
        diameter_8, diameter_9, diameter_10, diameter_11,
        diameter_12, diameter_13, diameter_14, diameter_15,
    ]
    return morphospace.generate_sample(name=name, opacities=opacities, diameters=diameters)


__all__ = ["NAME", "sample", "HYPERPARAMETERS", "ORIENTATIONS", "CircleGridMorphospace", "CircleGridMorphospaceSample"]
