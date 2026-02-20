"""
UV mapping for grid-based shell meshes.
"""

import bpy
import bmesh


def create_uv_map_from_grid(obj, cols):
    """
    Generates a UV map for the given object based on its grid layout.

    Each row (aperture) has a number of vertices equal to 'cols'. The function assumes
    the mesh vertices are arranged in row-major order. UV coordinates are assigned based
    on the cumulative edge lengths in each row (for U) and each column (for V).
    The bottom-left vertex is set to (0, 0) and the top-right vertex becomes (1, 1).

    Parameters:
        obj (bpy.types.Object): The Blender object to apply the UV mapping to.
        cols (int): The number of vertices per row.
    """
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bpy.ops.object.mode_set(mode='EDIT')
    mesh = obj.data
    bm = bmesh.from_edit_mesh(mesh)

    bm.verts.ensure_lookup_table()

    uv_layer = bm.loops.layers.uv.get("uv")
    if uv_layer is None:
        uv_layer = bm.loops.layers.uv.new("uv")

    total_verts = len(bm.verts)
    num_rows = total_verts // cols

    uv_dict = {}

    # --- Calculate U-coordinates (row-wise) ---
    for row in range(num_rows):
        base_idx = row * cols
        row_coords = [bm.verts[base_idx + col].co.copy() for col in range(cols)]
        cum_dist = [0.0]
        for col in range(1, cols):
            seg_length = (row_coords[col] - row_coords[col - 1]).length
            cum_dist.append(cum_dist[-1] + seg_length)
        total_length = cum_dist[-1]
        if total_length > 0:
            new_us = [d / total_length for d in cum_dist]
        else:
            new_us = [col / (cols - 1) for col in range(cols)]
        for col in range(cols):
            idx = base_idx + col
            if idx not in uv_dict:
                uv_dict[idx] = {}
            uv_dict[idx]['u'] = new_us[col]

    # --- Calculate V-coordinates (column-wise) ---
    for col in range(cols):
        col_coords = [bm.verts[row * cols + col].co.copy() for row in range(num_rows)]
        cum_dist = [0.0]
        for row in range(1, num_rows):
            seg_length = (col_coords[row] - col_coords[row - 1]).length
            cum_dist.append(cum_dist[-1] + seg_length)
        total_length = cum_dist[-1]
        if total_length > 0:
            new_vs = [d / total_length for d in cum_dist]
        else:
            new_vs = [row / (num_rows - 1) for row in range(num_rows)]
        for row in range(num_rows):
            idx = row * cols + col
            if idx not in uv_dict:
                uv_dict[idx] = {}
            uv_dict[idx]['v'] = new_vs[row]

    # --- Assign UV coordinates to each face loop ---
    for face in bm.faces:
        for loop in face.loops:
            idx = loop.vert.index
            u = uv_dict[idx].get('u', 0.0)
            v = uv_dict[idx].get('v', 0.0)
            loop[uv_layer].uv = (u, v)

    bmesh.update_edit_mesh(mesh)
