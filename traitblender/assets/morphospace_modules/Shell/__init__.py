from .helpers import get_raup_apex
from .morphospace import ShellMorphospace, ShellMorphospaceSample
from .orientations import ORIENTATIONS

# Display name for GUI and config references. Folder name remains the internal identifier.
NAME = "Shell (Default)"

# Hyperparameters: Non-biological parameters (discretization, surface options). From config, not dataset.
# Regular traits (eps, h_0, length) are passed as sample() params from the dataset.
HYPERPARAMETERS = {
    'points_in_circle': 10,      # Number of points around each shell ring (discretization)
    'time_step': 0.15,           # Time step for shell generation (discretization)
    'use_inner_surface': False,   # Whether to generate inner surface with thickness
}

# The sampling function. It is called by the generate_morphospace_sample_operator.
def sample(name="Shell", b = 0.2, d = 1.65, z = 0, a = 1, phi = 0, psi = 0, 
                         c_depth=0.1, c_n = 70, n_depth = 0, n = 0, t = 100,
                         eps=0.8, h_0=0.1, length=0.15, hyperparameters=None):
    """
    Generate a shell sample using the Shell morphospace model.
    
    Args:
        name (str): Name for the generated shell object
        b, d, z, a, phi, psi, c_depth, c_n, n_depth, n, t (float): Biological traits (from dataset)
        eps (float): Thickness parameter (allometric exponent) - trait
        h_0 (float): Base thickness parameter - trait
        length (float): Desired shell length in meters (scaling) - trait
        hyperparameters (dict, optional): From config. points_in_circle, time_step, use_inner_surface.
    """
    if hyperparameters is None:
        hyperparameters = {}
    merged_hyperparams = {**HYPERPARAMETERS, **hyperparameters}
    
    morphospace = ShellMorphospace()
    return morphospace.generate_sample(
        name=name, b=b, d=d, z=z, a=a, phi=phi, psi=psi,
        c_depth=c_depth, c_n=c_n, n_depth=n_depth, n=n, t=t,
        eps=eps, h_0=h_0, length=length,
        **merged_hyperparams
    )

__all__ = ['NAME', 'sample', 'HYPERPARAMETERS', 'ORIENTATIONS', 'get_raup_apex']
