import numpy as np
from .shell_morphospace_sample import ShellMorphospaceSample


class ShellMorphospace:

    def __init__(self):
        pass

    def _gamma(self, t, sin_t, cos_t, b, d, z):
        """Spiral centerline position."""
        return np.array([d * sin_t, d * cos_t, z]) * np.exp(b * t)

    def _N(self, t, sin_t, cos_t, b):
        """Normal vector component."""
        numerator = np.array([b * cos_t - sin_t, -b * sin_t - cos_t, 0])
        denominator = np.sqrt(b**2 + 1)
        return numerator / denominator

    def _B(self, t, sin_t, cos_t, b, d, z):
        """Binormal vector component."""
        numerator = np.array([b * z * (b * sin_t + cos_t), b * z * (b * cos_t - sin_t), d * (b**2 + 1)])
        denominator = np.sqrt((b**2 + 1) * (d**2 * (b**2 + 1) + b**2 * z**2))
        return numerator / denominator

    def _R_b(self, psi):
        """Rotation matrix for aperture."""
        return np.array([
            [np.cos(psi), -np.sin(psi), 0],
            [np.sin(psi), np.cos(psi), 0],
            [0, 0, 1]
        ])

    def _C(self, t, theta, sin_t, cos_t, sin_theta, cos_theta, b, a, d, z, phi, psi, c_n, c_depth, n, n_depth):
        """Aperture shape terms: (axial_ribs * spiral_ribs), aperture_size, aperture_shape."""
        aperture_size = np.exp(b * t) - (1 / (t + 1))
        axial_ribs = (1 + c_depth * np.sin(c_n * t))
        rotation_matrix = self._R_b(psi)
        spiral_ribs = (1 + (n_depth * np.sin(n * theta)))

        vector_N = ((a * sin_theta * np.cos(phi)) + (cos_theta * np.sin(phi))) * self._N(t, sin_t, cos_t, b)
        vector_B = ((a * sin_theta * np.sin(phi)) - (cos_theta * np.cos(phi))) * self._B(t, sin_t, cos_t, b, d, z)

        aperture_shape = np.dot(rotation_matrix, vector_N + vector_B)
        return (axial_ribs * spiral_ribs), aperture_size, aperture_shape

    def _lambda(self, t, theta, sin_t, cos_t, sin_theta, cos_theta, b, d, z, a, phi, psi, c_n, c_depth, n, n_depth, inner, eps, h_0):
        """Single point on shell surface (outer or inner)."""
        surface = self._C(t, theta, sin_t, cos_t, sin_theta, cos_theta, b, a, d, z, phi, psi, c_n, c_depth, n, n_depth)

        if inner:
            surface = surface[1] * surface[2]
            surface_norm = np.linalg.norm(surface)
            thickness = ((np.exp(b * t) - (1 / (t + 1))) ** eps) * h_0

            # Numerical safeguards for inner surface thickness calculation.
            # Prevents NaN/Inf from division by zero, negative thickness, or extreme ratios.
            if surface_norm < 1e-10:
                surface_product = surface
            elif np.isnan(thickness) or np.isinf(thickness) or thickness < 0:
                surface_product = surface * 0.9
            elif thickness > surface_norm * 0.9:
                surface_product = surface * 0.1
            else:
                surface_product = surface * (1 - thickness / surface_norm)
        else:
            surface_product = surface[0] * surface[1] * surface[2]

        return self._gamma(t, sin_t, cos_t, b, d, z) + surface_product

    def _compute_surface_vertices(self, t_values, theta_values, sin_t_values, cos_t_values,
                                  sin_theta_values, cos_theta_values, b, d, z, a, phi, psi,
                                  c_n, c_depth, n, n_depth, eps, h_0, inner=False):
        """Compute full surface vertex array (outer or inner)."""
        return np.array([
            [
                self._lambda(t, theta, sin_t, cos_t, sin_theta, cos_theta,
                                    b, d, z, a, phi, psi, c_n, c_depth, n, n_depth, inner, eps, h_0)
                for theta, sin_theta, cos_theta in zip(theta_values, sin_theta_values, cos_theta_values)
            ]
            for t, sin_t, cos_t in zip(t_values, sin_t_values, cos_t_values)
        ])

    def generate_sample(self, name="Shell", b=0.2, d=1.65, z=0, a=1, phi=0, psi=0,
                        c_depth=0.1, c_n=70, n_depth=0, n=0, t=100,
                        points_in_circle=40, time_step=1/30, use_inner_surface=True,
                        eps=0.8, h_0=0.1, length=0.15):

        t_values = np.arange(0, t, time_step)
        theta_values = np.linspace(0, 2 * np.pi, points_in_circle, endpoint=False)

        sin_t_values = np.sin(t_values)
        cos_t_values = np.cos(t_values)
        sin_theta_values = np.sin(theta_values)
        cos_theta_values = np.cos(theta_values)

        outer_surface = self._compute_surface_vertices(
            t_values, theta_values, sin_t_values, cos_t_values,
            sin_theta_values, cos_theta_values, b, d, z, a, phi, psi,
            c_n, c_depth, n, n_depth, eps, h_0, inner=False
        )

        if use_inner_surface:
            inner_surface = self._compute_surface_vertices(
                t_values, theta_values, sin_t_values, cos_t_values,
                sin_theta_values, cos_theta_values, b, d, z, a, phi, psi,
                c_n, c_depth, n, n_depth, eps, h_0, inner=True
            )
            aperture = np.vstack((outer_surface[-1], inner_surface[-1]))
        else:
            inner_surface = None
            aperture = outer_surface[-1]

        shell = {
            "outer_surface": outer_surface,
            "inner_surface": inner_surface,
            "aperture": aperture
        }

        if length is not None:
            all_x_coords = []
            all_x_coords.extend(outer_surface[:, :, 0].flatten())
            if inner_surface is not None:
                all_x_coords.extend(inner_surface[:, :, 0].flatten())
            all_x_coords.extend(aperture[:, 0])

            x_length_current = max(all_x_coords) - min(all_x_coords)
            scale_factor = length / x_length_current if x_length_current != 0 else 1

            shell["outer_surface"] = outer_surface * scale_factor
            if inner_surface is not None:
                shell["inner_surface"] = inner_surface * scale_factor
            shell["aperture"] = shell["aperture"] * scale_factor

        return ShellMorphospaceSample(name=name, data=shell)
