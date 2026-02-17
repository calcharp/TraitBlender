import bpy
import numpy as np
import bmesh
from pathlib import Path
from ..morphospace_sample.contreras_morphospace_sample import Contreras_MORPHOSPACE_SAMPLE

class Contreras_MORPHOSPACE():

    def __init__(self):
        pass

    def generate_sample(self, name="Shell", b = .1, d = 4, z = 0, a = 1, phi = 0, psi = 0, 
                         c_depth=0.1, c_n = 70, n_depth = 0, n = 0, t = 20, 
                         points_in_circle=40, time_step=1/30, use_inner_surface=True, 
                         eps=0.8, h_0=0.1, length=0.015):

        t_values = np.arange(0, t, time_step)
        theta_values = np.linspace(0, 2*np.pi, points_in_circle, endpoint=False)

        sin_t_values = np.sin(t_values)
        cos_t_values = np.cos(t_values)
        sin_theta_values = np.sin(theta_values)
        cos_theta_values = np.cos(theta_values)

        def gamma(t, sin_t, cos_t, b, d, z):
            return np.array([d * sin_t, d * cos_t, z]) * np.exp(b * t)

        def N(t, sin_t, cos_t, b):
            numerator = np.array([b * cos_t - sin_t, -b * sin_t - cos_t, 0])
            denominator = np.sqrt(b**2 + 1)
            return numerator / denominator

        def B(t, sin_t, cos_t, b, d, z):
            numerator = np.array([b * z * (b * sin_t + cos_t), b * z * (b * cos_t - sin_t), d * (b**2 + 1)])
            denominator = np.sqrt((b**2 + 1) * (d**2 * (b**2 + 1) + b**2 * z**2))
            return numerator / denominator

        def R_b(psi):
            return np.array([[np.cos(psi), -np.sin(psi), 0],
                            [np.sin(psi), np.cos(psi), 0],
                            [0, 0, 1]])

        def C(t, theta, sin_t, cos_t, sin_theta, cos_theta, b, a, d, z, phi, psi, c_n, c_depth, n, n_depth):
            aperture_size = np.exp(b * t) - (1 / (t + 1))
            axial_ribs = (1 + c_depth * np.sin(c_n * t))
            rotation_matrix = R_b(psi)
            spiral_ribs = (1 + (n_depth*(np.sin(n*theta))))

            vector_N = ((a * sin_theta * np.cos(phi)) + (cos_theta * np.sin(phi))) * N(t, sin_t, cos_t, b)
            vector_B = ((a * sin_theta * np.sin(phi)) - (cos_theta * np.cos(phi))) * B(t, sin_t, cos_t, b, d, z)

            aperture_shape = np.dot(rotation_matrix, vector_N + vector_B)
            return (axial_ribs*spiral_ribs), aperture_size, aperture_shape

        def lambda_(t, theta, sin_t, cos_t, sin_theta, cos_theta, b, d, z, a, phi, psi, c_n, c_depth, n, n_depth, inner=False, eps=eps, h_0=h_0):
            surface = C(t, theta, sin_t, cos_t, sin_theta, cos_theta, b, a, d, z, phi, psi, c_n, c_depth, n, n_depth)
            
            if inner:
                surface = surface[1] * surface[2]
                surface_norm = np.linalg.norm(surface)
                thickness = ((np.exp(b*t) - (1 / (t + 1)))**eps)*h_0
                
                # NUMERICAL SAFEGUARDS FOR INNER SURFACE THICKNESS CALCULATION
                # 
                # ISSUE: The inner surface calculation can produce NaN/infinite coordinates at the 
                # beginning and end of the shell due to numerical instability in the thickness formula.
                # 
                # ROOT CAUSES:
                # 1. Division by zero: When surface_norm ≈ 0, thickness/surface_norm → ∞
                # 2. Small t values: At shell start (t ≈ 0), np.exp(b*t) - (1/(t+1)) can be negative/small
                #    When raised to power eps, this can produce NaN or extreme values
                # 3. Thickness ratio: If thickness > surface_norm, the subtraction creates negative/infinite results
                #
                # SOLUTION: Add checks to detect problematic cases and use safe fallbacks:
                # - Skip thickness for very small surface norms (prevents division by zero)
                # - Detect NaN/inf thickness and use 90% surface reduction
                # - Cap thickness at 90% of surface norm to prevent extreme ratios
                # - Use 10% reduction as safe fallback for large thickness ratios
                #
                # This ensures the inner surface remains numerically stable while preserving
                # the shell's visual appearance and geometric properties.
                
                # Add numerical safeguards to prevent NaN/Inf
                if surface_norm < 1e-10:  # Very small norm - don't apply thickness
                    surface_product = surface
                elif np.isnan(thickness) or np.isinf(thickness) or thickness < 0:
                    # Invalid thickness - use small reduction
                    surface_product = surface * 0.9
                elif thickness > surface_norm * 0.9:  # Thickness too large relative to surface
                    surface_product = surface * 0.1  # Apply small reduction
                else:
                    surface_product = surface * (1 - thickness/surface_norm)
            else:
                surface_product = surface[0] * surface[1] * surface[2]
            
            return gamma(t, sin_t, cos_t, b, d, z) + surface_product

        def compute_surface_vertices(inner=False, eps=eps, h_0=h_0):
            return np.array([
                [lambda_(t, theta, sin_t, cos_t, sin_theta, cos_theta, b, d, z, a, phi, psi, c_n, c_depth, n, n_depth, inner, eps, h_0)
                for theta, sin_theta, cos_theta in zip(theta_values, sin_theta_values, cos_theta_values)]
                for t, sin_t, cos_t in zip(t_values, sin_t_values, cos_t_values)
            ])

        outer_surface = compute_surface_vertices(inner=False)
        
        # Conditionally generate inner surface based on hyperparameter
        if use_inner_surface:
            inner_surface = compute_surface_vertices(inner=True, eps=eps, h_0=h_0)
            aperture = np.vstack((outer_surface[-1], inner_surface[-1]))
        else:
            inner_surface = None
            # Aperture is just the outer surface at the end
            aperture = outer_surface[-1]

        shell = {
            "outer_surface": outer_surface,
            "inner_surface": inner_surface,
            "aperture": aperture
        }

        # Calculate the current length along the x-axis and apply scaling
        if length is not None:
            # Get all x coordinates from the shell data
            all_x_coords = []
            all_x_coords.extend(outer_surface[:, :, 0].flatten())
            if inner_surface is not None:
                all_x_coords.extend(inner_surface[:, :, 0].flatten())
            all_x_coords.extend(aperture[:, 0])
            
            x_length_current = max(all_x_coords) - min(all_x_coords)
            
            # Calculate the scale factor
            scale_factor = length / x_length_current if x_length_current != 0 else 1
            
            # Apply scaling to all shell data
            shell["outer_surface"] = outer_surface * scale_factor
            if inner_surface is not None:
                shell["inner_surface"] = inner_surface * scale_factor
            shell["aperture"] = shell["aperture"] * scale_factor

        return Contreras_MORPHOSPACE_SAMPLE(
            name = name,
            data = shell
        ) 