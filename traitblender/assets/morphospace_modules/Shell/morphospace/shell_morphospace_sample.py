import bpy
import numpy as np

from ..helpers import create_uv_map_from_grid


class ShellMorphospaceSample():

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def to_blender(self):
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
