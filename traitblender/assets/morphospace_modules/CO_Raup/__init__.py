import bpy
from .morphospace.contreras_morphospace import Contreras_MORPHOSPACE
from .morphospace_sample.contreras_morphospace_sample import Contreras_MORPHOSPACE_SAMPLE


def _orient_default(sample_obj):
    """Default orientation: center on table at (0, 0, 0)."""
    sample_obj.tb_coords = (0.0, 0.0, 0.0)
    bpy.context.view_layer.update()


ORIENTATIONS = {
    "Default": _orient_default,
}

# Hyperparameters: Non-biological parameters needed for morphospace generation
HYPERPARAMETERS = {
    'points_in_circle': 40,      # Number of points around each shell ring (discretization)
    'time_step': 1/30,            # Time step for shell generation (discretization)
    'use_inner_surface': True,    # Whether to generate inner surface with thickness
    'eps': 0.8,                   # Thickness parameter (allometric exponent)
    'h_0': 0.1,                   # Base thickness parameter
    'length': 0.015               # Desired final shell length in meters (scaling)
}

def sample(name="Shell", b=0.1, d=4, z=0, a=1, phi=0, psi=0, 
           c_depth=0, c_n=0, n_depth=0, n=0, t=10, 
           hyperparameters=None):
    """
    Generate a shell sample using the Contreras morphospace model.
    
    Args:
        name (str): Name for the generated shell object
        b (float): Growth rate parameter
        d (float): Distance from axis parameter
        z (float): Vertical offset parameter
        a (float): Aperture shape parameter
        phi (float): Rotation angle phi
        psi (float): Rotation angle psi
        c_depth (float): Axial rib depth
        c_n (float): Axial rib frequency
        n_depth (float): Spiral rib depth
        n (float): Spiral rib frequency
        t (float): Time parameter (shell length)
        hyperparameters (dict, optional): Dictionary of hyperparameters. If None, uses defaults from HYPERPARAMETERS.
            Available hyperparameters:
            - points_in_circle (int): Number of points around each shell ring
            - time_step (float): Time step for shell generation
            - use_inner_surface (bool): Whether to generate inner surface with thickness
            - eps (float): Thickness parameter (allometric exponent)
            - h_0 (float): Base thickness parameter
            - length (float): Desired length of the shell in meters
    
    Returns:
        Contreras_MORPHOSPACE_SAMPLE: A shell sample object that can be converted to Blender
    """
    # Merge provided hyperparameters with defaults
    if hyperparameters is None:
        hyperparameters = {}
    merged_hyperparams = {**HYPERPARAMETERS, **hyperparameters}
    
    morphospace = Contreras_MORPHOSPACE()
    return morphospace.generate_sample(
        name=name, b=b, d=d, z=z, a=a, phi=phi, psi=psi,
        c_depth=c_depth, c_n=c_n, n_depth=n_depth, n=n, t=t,
        **merged_hyperparams
    )

__all__ = ['sample', 'HYPERPARAMETERS', 'ORIENTATIONS']
