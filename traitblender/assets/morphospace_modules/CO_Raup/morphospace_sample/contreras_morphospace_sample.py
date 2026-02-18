import bpy
import numpy as np
import bmesh
from pathlib import Path
from mathutils import Vector

class Contreras_MORPHOSPACE_SAMPLE():

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def to_blender(self):

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
            # Ensure the object is active and selected.
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            
            # Switch to EDIT mode to allow bmesh operations.
            bpy.ops.object.mode_set(mode='EDIT')
            mesh = obj.data
            bm = bmesh.from_edit_mesh(mesh)
            
            # Ensure that the bmesh index surface is up-to-date.
            bm.verts.ensure_lookup_table()
            
            uv_layer = bm.loops.layers.uv.get("uv")
            if uv_layer is None:
                uv_layer = bm.loops.layers.uv.new("uv")
            
            total_verts = len(bm.verts)
            num_rows = total_verts // cols  # Assumes total vertices is an exact multiple of cols.
            
            uv_dict = {}

            # --- Calculate U-coordinates (row-wise) ---
            for row in range(num_rows):
                base_idx = row * cols
                # Gather the coordinates for each vertex in the row.
                row_coords = [bm.verts[base_idx + col].co.copy() for col in range(cols)]
                # Compute cumulative distances for the row.
                cum_dist = [0.0]
                for col in range(1, cols):
                    seg_length = (row_coords[col] - row_coords[col - 1]).length
                    cum_dist.append(cum_dist[-1] + seg_length)
                total_length = cum_dist[-1]
                # Normalize cumulative distances to [0,1].
                if total_length > 0:
                    new_us = [d / total_length for d in cum_dist]
                else:
                    new_us = [col / (cols - 1) for col in range(cols)]
                # Store the U coordinates in the dictionary.
                for col in range(cols):
                    idx = base_idx + col
                    if idx not in uv_dict:
                        uv_dict[idx] = {}
                    uv_dict[idx]['u'] = new_us[col]

            # --- Calculate V-coordinates (column-wise) ---
            for col in range(cols):
                # Gather the vertex coordinates for this column.
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
                # Store the V coordinates.
                for row in range(num_rows):
                    idx = row * cols + col
                    if idx not in uv_dict:
                        uv_dict[idx] = {}
                    uv_dict[idx]['v'] = new_vs[row]

            # --- Assign the new UV coordinates to each face loop ---
            for face in bm.faces:
                for loop in face.loops:
                    idx = loop.vert.index
                    u = uv_dict[idx].get('u', 0.0)
                    v = uv_dict[idx].get('v', 0.0)
                    loop[uv_layer].uv = (u, v)
            
            # Push the updated UVs back to the mesh.
            bmesh.update_edit_mesh(mesh)

        ap = self.data["aperture"]
        inner_surface = self.data.get("inner_surface")
        use_inner = inner_surface is not None
        
        # Only create aperture mesh if we have inner surface (aperture connects outer to inner)
        aperture_obj = None
        if use_inner:
            # Aperture connects outer and inner surfaces
            points_around_aperture = ap.shape[0] // 2  
            outer = ap[:points_around_aperture]
            inner = ap[points_around_aperture:]
            aperture_vertices = np.vstack((outer, inner))  

            aperture_faces = []
            for i in range(points_around_aperture):
                # wrap around to 0 after the last index
                next_i = (i + 1) % points_around_aperture
                
                outer_i = i
                outer_next = next_i
                inner_i = i + points_around_aperture
                inner_next = next_i + points_around_aperture

                # define quad face as (outer_i, outer_next, inner_next, inner_i)
                aperture_faces.append((outer_i, outer_next, inner_next, inner_i))
            
            # Create aperture mesh
            aperture_mesh = bpy.data.meshes.new(name=f"{self.name}_aperture")
            aperture_mesh.from_pydata(aperture_vertices.tolist(), [], aperture_faces)
            aperture_mesh.update()

            aperture_obj = bpy.data.objects.new(f"{self.name}_aperture", aperture_mesh)
            bpy.context.collection.objects.link(aperture_obj)
            vg = aperture_obj.vertex_groups.new(name="aperture_vg")
            all_vert_indices = [v.index for v in aperture_obj.data.vertices]
            vg.add(all_vert_indices, 1.0, 'REPLACE')

            aperture_obj.data.uv_layers.new(name="uv")
            aperture_obj.data.uv_layers.active = aperture_obj.data.uv_layers["uv"]
            bpy.context.view_layer.objects.active = aperture_obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.uv.unwrap(method='ANGLE_BASED')
            bpy.ops.object.mode_set(mode='OBJECT')

        surfaces = ["outer_surface"]
        if use_inner:
            surfaces.append("inner_surface")
        objs = []

        for surface_name in surfaces:
            points = self.data[surface_name]

            temp_mesh = bpy.data.meshes.new(name=f"{surface_name}")

            vertices = points.reshape(-1, 3)
            faces = []

            num_rings = len(points)
            points_per_ring = len(points[0])

            for ring in range(num_rings - 1):
                for pt in range(points_per_ring):
                    p1 = ring * points_per_ring + pt
                    p2 = ring * points_per_ring + (pt + 1) % points_per_ring
                    p3 = (ring + 1) * points_per_ring + (pt + 1) % points_per_ring
                    p4 = (ring + 1) * points_per_ring + pt

                    faces.append((p1, p2, p3, p4))

            temp_mesh.from_pydata(vertices, [], faces)
            temp_mesh.update()

            obj = bpy.data.objects.new(f"{surface_name}", temp_mesh)
            bpy.context.collection.objects.link(obj)

            vg = obj.vertex_groups.new(name=f"{surface_name}_vg")
            all_vert_indices = [v.index for v in obj.data.vertices]
            vg.add(all_vert_indices, 1.0, 'REPLACE')

            create_uv_map_from_grid(obj, points_per_ring)

            objs.append(obj)

        surface_names = [f"{surface_name}" for surface_name in surfaces]
        if aperture_obj is not None:
            surface_names.append(f"{self.name}_aperture")

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        for name in surface_names:
            obj = bpy.data.objects.get(name)
            if obj:
                obj.select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[surface_names[0]]
        bpy.ops.object.join()

        obj = bpy.context.active_object
        obj.name = self.name

        # Store mesh structure for orientation (last ring of outer_surface = aperture)
        outer_points = self.data["outer_surface"]
        num_rings = len(outer_points)
        points_per_ring = len(outer_points[0])
        obj["raup_num_rings"] = num_rings
        obj["raup_points_per_ring"] = points_per_ring

        # Origin is set by orientation (apex) when apply_orientation runs
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.shade_smooth()
        

        # Update the scene
        bpy.context.view_layer.update() 