from .morphospace.contreras_morphospace import Contreras_MORPHOSPACE
from .morphospace_sample.contreras_morphospace_sample import Contreras_MORPHOSPACE_SAMPLE

def sample(name="Shell", b=0.1, d=4, z=0, a=1, phi=0, psi=0, 
           c_depth=0.1, c_n=70, n_depth=0, n=0, t=20, time_step=0.25/30, 
           points_in_circle=40, eps=0.8, h_0=0.1, length=0.015):
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
        time_step (float): Time step for shell generation
        points_in_circle (int): Number of points around each shell ring
        eps (float): Thickness parameter
        h_0 (float): Base thickness parameter
        length (float): Desired length of the shell in meters
    
    Returns:
        Contreras_MORPHOSPACE_SAMPLE: A shell sample object that can be converted to Blender
    """
    morphospace = Contreras_MORPHOSPACE()
    return morphospace.generate_sample(
        name=name, b=b, d=d, z=z, a=a, phi=phi, psi=psi,
        c_depth=c_depth, c_n=c_n, n_depth=n_depth, n=n, t=t, 
        time_step=time_step, points_in_circle=points_in_circle, 
        eps=eps, h_0=h_0, length=length
    )

__all__ = ['sample'] 