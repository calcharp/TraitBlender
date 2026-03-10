"""Circle Grid morphospace: generates sample data (opacities and diameter traits for 16 circles)."""

from .circle_grid_morphospace_sample import CircleGridMorphospaceSample


class CircleGridMorphospace:
    """Morphospace that produces a white cube with 16 trait-controlled black circles on top."""

    def generate_sample(self, name="CircleGrid", opacities=None, diameters=None):
        """Generate a Circle Grid sample. opacities: 16 floats (0–1). diameters: 16 size traits (0 = default, 1 = 2×, 2 = 4×; scale = 2^trait)."""
        if opacities is None:
            opacities = [1.0] * 16
        opacities = list(opacities)[:16]
        while len(opacities) < 16:
            opacities.append(1.0)
        if diameters is None:
            diameters = [0.0] * 16
        diameters = list(diameters)[:16]
        while len(diameters) < 16:
            diameters.append(0.0)
        diameters = [float(d) for d in diameters]
        data = {"opacities": opacities, "diameters": diameters}
        return CircleGridMorphospaceSample(name=name, data=data)
