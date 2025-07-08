import bpy
import numpy as np
import bmesh
from pathlib import Path
from ..morphospace_sample.contreras_morphospace_sample import Contreras_MORPHOSPACE_SAMPLE

class Contreras_MORPHOSPACE():

    def __init__(self):
        pass

    def generate_sample(self, name="Shell", b = .1, d = 4, z = 0, a = 1, phi = 0, psi = 0, 
                         c_depth=0.1, c_n = 70, n_depth = 0, n = 0, t = 20, time_step = .25/30, 
                         points_in_circle=40, eps=0.8, h_0=0.1):

        t_values = np.arange(0, t, time_step)
        theta_values = np.arange(0, 2*np.pi, np.pi/points_in_circle)

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
        inner_surface = compute_surface_vertices(inner=True, eps=eps, h_0=h_0)

        shell = {
            "outer_surface": outer_surface,
            "inner_surface": inner_surface,
            "aperture": np.vstack((outer_surface[-1], inner_surface[-1]))
        }

        return Contreras_MORPHOSPACE_SAMPLE(
            name = name,
            data = shell
        ) 