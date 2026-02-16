import bpy
from mathutils import Vector, Matrix
from .morphospace.contreras_morphospace import Contreras_MORPHOSPACE
from .morphospace_sample.contreras_morphospace_sample import Contreras_MORPHOSPACE_SAMPLE


def _orient_default(sample_obj):
    """
    Default orientation: center on table at (0,0), rotate so the aperture face
    (last ring of outer_surface_vg) is orthogonal to the table's Y axis.
    """
    # 0. Reset rotation: tb_rotation.x and tb_rotation.y to 0 (keep z)
    x, y, z = sample_obj.tb_rotation
    sample_obj.tb_rotation = (0.0, 0.0, z)

    # 1. Center on table: tb_coords = (0, 0, 0)
    sample_obj.tb_coords = (0.0, 0.0, 0.0)

    # 2. Get last ring vertices from outer_surface_vg
    vg = sample_obj.vertex_groups.get("outer_surface_vg")
    if not vg:
        return  # No vertex group, skip rotation

    num_rings = sample_obj.get("raup_num_rings")
    points_per_ring = sample_obj.get("raup_points_per_ring")
    if num_rings is None or points_per_ring is None:
        return

    depsgraph = bpy.context.evaluated_depsgraph_get()
    obj_eval = sample_obj.evaluated_get(depsgraph)
    mesh = obj_eval.data
    mw = obj_eval.matrix_world

    # Last ring vertex indices (outer_surface verts are first in joined mesh)
    last_ring_start = (num_rings - 1) * points_per_ring
    last_ring_indices = range(last_ring_start, last_ring_start + points_per_ring)

    # Get world-space positions of last ring vertices
    last_ring_world = [mw @ mesh.vertices[i].co for i in last_ring_indices]

    # 3. Compute aperture plane normal from the ring (cross product of adjacent edges)
    # Use centroid and sum of cross products for stable normal
    centroid = sum(last_ring_world, Vector()) / len(last_ring_world)
    normal = Vector((0, 0, 0))
    n_pts = len(last_ring_world)
    for i in range(n_pts):
        v0 = last_ring_world[i] - centroid
        v1 = last_ring_world[(i + 1) % n_pts] - centroid
        normal += v0.cross(v1)
    if normal.length_squared < 1e-12:
        return
    normal.normalize()

    # Aperture opens "out" from the shell - normal should point away from shell base.
    # The first ring is at the base; last ring is at the aperture. The shell grows
    # from base toward aperture. So normal should point from base toward aperture.
    # Centroid of first ring vs last ring gives growth direction.
    first_ring_start = 0
    first_ring_world = [mw @ mesh.vertices[i].co for i in range(first_ring_start, points_per_ring)]
    base_centroid = sum(first_ring_world, Vector()) / len(first_ring_world)
    growth_dir = centroid - base_centroid
    if growth_dir.length_squared > 1e-12:
        growth_dir.normalize()
        if normal.dot(growth_dir) < 0:
            normal = -normal  # Flip so normal points out of aperture

    # 4. Get table's Y axis - aperture face (plane) should be orthogonal to it
    table = bpy.data.objects.get("Table")
    if not table:
        return
    table_eval = table.evaluated_get(depsgraph)
    table_rot = table_eval.matrix_world.to_quaternion().to_matrix()
    table_y = Vector(table_rot.col[1]).normalized()

    # 5. Target: aperture normal must be orthogonal to table Y (normal in XZ plane)
    # Project current normal onto the plane perpendicular to table Y
    current = normal.normalized()
    target = current - (current.dot(table_y) * table_y)
    if target.length_squared < 1e-12:
        # Normal already parallel to table Y → aperture face already orthogonal to Y. Done.
        return
    target.normalize()
    dot = current.dot(target)
    # Clamp for numerical safety
    dot = max(-1.0, min(1.0, dot))
    if dot > 0.9999:
        return  # Already aligned
    if dot < -0.9999:
        # 180° flip - pick an axis
        axis = current.cross(Vector((1, 0, 0)))
        if axis.length_squared < 1e-12:
            axis = current.cross(Vector((0, 1, 0)))
        axis.normalize()
        angle = 3.14159265359
    else:
        axis = current.cross(target)
        if axis.length_squared < 1e-12:
            return
        axis.normalize()
        angle = current.angle(target)

    # 6. Apply rotation around object's origin (in world space)
    pivot = mw.translation
    to_origin = Matrix.Translation(-pivot)
    rot_mat = Matrix.Rotation(angle, 4, axis)
    from_origin = Matrix.Translation(pivot)
    sample_obj.matrix_world = from_origin @ rot_mat @ to_origin @ sample_obj.matrix_world

    # Sync rotation_euler for consistency
    sample_obj.rotation_euler = sample_obj.matrix_world.to_euler(sample_obj.rotation_mode)
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
