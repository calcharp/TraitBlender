import bpy
import math
from mathutils import Vector
from .morphospace.contreras_morphospace import Contreras_MORPHOSPACE
from .morphospace_sample.contreras_morphospace_sample import Contreras_MORPHOSPACE_SAMPLE


def get_raup_apex(shell):
    """
    World-space centroid of the first ring (apex) for a CO_Raup shell.
    The apex is the tip of the spiral; use as rotation pivot. Updates with object transform.

    Args:
        shell: Blender object or object name (str)

    Returns:
        tuple: (x, y, z) in world space, or (0, 0, 0) if not a valid shell
    """
    obj = bpy.data.objects.get(shell) if isinstance(shell, str) else shell
    if not obj:
        return (0.0, 0.0, 0.0)
    ppb = obj.get("raup_points_per_ring")
    if not ppb or not hasattr(obj, "data") or obj.type != "MESH":
        return (0.0, 0.0, 0.0)
    mw = obj.matrix_world
    verts = obj.data.vertices
    if len(verts) < ppb:
        return (0.0, 0.0, 0.0)
    world_centroid = sum((mw @ verts[i].co for i in range(ppb)), Vector()) / ppb
    return (world_centroid.x, world_centroid.y, world_centroid.z)


def _orient_default(sample_obj):
    """
    Default orientation: center on table, rotate by -t so all apertures align.
    t is the spiral parameter (radians) from the morphospace; the aperture
    position correlates with t, so rotating by -t brings them to a common orientation.
    """
    sample_obj.tb_coords = (0.0, 0.0, 0.0)

    t_val = 0
    try:
        dataset = bpy.context.scene.traitblender_dataset
        row = dataset.loc(sample_obj.name)
        for col in row.index:
            if str(col).lower().strip() == "t":
                t_val = float(row[col])
                break
    except (KeyError, TypeError, ValueError, AttributeError):
        pass

    # Use modulo 2π so apertures align regardless of how many whorls (t can be 20+ radians)
    rotation_z = t_val % (2 * math.pi)
    sample_obj.tb_rotation = (0.0, 0.0, rotation_z)
    bpy.context.view_layer.update()

    # Ensure centered on table after rotation
    sample_obj.tb_coords = (0.0, 0.0, 0.0)


ORIENTATIONS = {
    "Default": _orient_default,
}

# Hyperparameters: Non-biological parameters (discretization, surface options). From config, not dataset.
# Regular traits (eps, h_0, length) are passed as sample() params from the dataset.
HYPERPARAMETERS = {
    'points_in_circle': 40,      # Number of points around each shell ring (discretization)
    'time_step': 1/30,           # Time step for shell generation (discretization)
    'use_inner_surface': True,   # Whether to generate inner surface with thickness
}

def sample(name="Shell", b=0.1, d=4, z=0, a=1, phi=0, psi=0, 
           c_depth=0, c_n=0, n_depth=0, n=0, t=10, 
           eps=0.8, h_0=0.1, length=0.015,
           hyperparameters=None):
    """
    Generate a shell sample using the Contreras morphospace model.
    
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
    
    morphospace = Contreras_MORPHOSPACE()
    return morphospace.generate_sample(
        name=name, b=b, d=d, z=z, a=a, phi=phi, psi=psi,
        c_depth=c_depth, c_n=c_n, n_depth=n_depth, n=n, t=t,
        eps=eps, h_0=h_0, length=length,
        **merged_hyperparams
    )

__all__ = ['sample', 'HYPERPARAMETERS', 'ORIENTATIONS', 'get_raup_apex']
