"""Circle Grid sample: builds Blender mesh (white cube + 16 black circles on top)."""

import bpy


# Cube: 0.29 m x 0.29 m x 0.01 m (1 cm deep in z), centered at origin
_CUBE_HALF_XY = 0.29 / 2.0
_CUBE_HALF_Z = 0.005

# 4x4 grid on top face
_CELL_SIZE = 0.29 / 4.0
_TOP_Z = _CUBE_HALF_Z
_CIRCLE_VERTICES = 64  # vertices for Add Mesh > Circle (smooth look)
# Avoid coplanar z-fighting artifacts with transparency/Cycles by nudging circles up a bit.
_CIRCLE_Z_EPS = 1e-4
# Default circle diameter in Blender (meters). Diameter trait: 0 = this size, 1 = 2×, 2 = 4× (scale = 2^trait).
# Values in (0, 0.01) are treated as 0 so old CSVs with 0.03 in the column still get default size.
_DEFAULT_DIAMETER_M = 0.03
_TRAIT_AS_DEFAULT_THRESHOLD = 0.01


def _cube_vertices_and_faces():
    """Cube vertices and quad faces (8 verts, 6 quads)."""
    hx, hy, hz = _CUBE_HALF_XY, _CUBE_HALF_XY, _CUBE_HALF_Z
    verts = [
        (-hx, -hy, -hz), (hx, -hy, -hz), (hx, hy, -hz), (-hx, hy, -hz),
        (-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz),
    ]
    faces = [
        (0, 1, 2, 3),  # bottom
        (4, 5, 6, 7),  # top
        (0, 1, 5, 4),  # front
        (1, 2, 6, 5),  # right
        (2, 3, 7, 6),  # back
        (3, 0, 4, 7),  # left
    ]
    return verts, faces


def _grid_centers_4x4():
    """Row-major (0..15) centers for 4x4 grid on top face."""
    centers = []
    start = -_CUBE_HALF_XY + _CELL_SIZE / 2
    for row in range(4):
        for col in range(4):
            x = start + col * _CELL_SIZE
            y = start + row * _CELL_SIZE
            centers.append((x, y, _TOP_Z))
    return centers


class CircleGridMorphospaceSample:
    """Sample: white cube with 16 black circles; data['opacities'] and data['diameters'] = 16 floats each."""

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def to_blender(self):
        opacities = self.data.get("opacities", [1.0] * 16)
        while len(opacities) < 16:
            opacities.append(1.0)
        opacities = opacities[:16]

        # Diameter traits: 0 = default, 1 = 2×, 2 = 4× (scale = 2^trait). Treat values in (0, 0.01) as 0 so 0.03 from old CSV = default.
        diameter_traits = self.data.get("diameters", [0.0] * 16)
        while len(diameter_traits) < 16:
            diameter_traits.append(0.0)
        diameter_traits = [float(d) for d in diameter_traits[:16]]
        scales = []
        for t in diameter_traits:
            if -_TRAIT_AS_DEFAULT_THRESHOLD < t < _TRAIT_AS_DEFAULT_THRESHOLD:
                t = 0.0
            scales.append(2.0 ** t)
        diameters_blender = [max(0.0, _DEFAULT_DIAMETER_M * s) for s in scales]

        # White material for cube
        white_mat = bpy.data.materials.get(f"{self.name}_white")
        if white_mat is None:
            white_mat = bpy.data.materials.new(name=f"{self.name}_white")
            white_mat.use_nodes = True
            bsdf = white_mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = (1, 1, 1, 1)
                bsdf.inputs["Roughness"].default_value = 1.0
                if "Specular IOR Level" in bsdf.inputs:
                    bsdf.inputs["Specular IOR Level"].default_value = 0.0
                elif "Specular" in bsdf.inputs:
                    bsdf.inputs["Specular"].default_value = 0.0

        # Cube
        verts, faces = _cube_vertices_and_faces()
        cube_mesh = bpy.data.meshes.new(name="cube")
        cube_mesh.from_pydata(verts, [], faces)
        cube_mesh.update()
        cube_obj = bpy.data.objects.new("cube", cube_mesh)
        bpy.context.collection.objects.link(cube_obj)
        if not cube_obj.data.materials:
            cube_obj.data.materials.append(white_mat)
        else:
            cube_obj.data.materials[0] = white_mat
        bpy.context.view_layer.objects.active = cube_obj
        cube_obj.select_set(True)

        # 16 circles: Add Mesh > Circle (same as Shift+A > Mesh > Circle)
        if bpy.context.view_layer.objects.active:
            bpy.ops.object.mode_set(mode="OBJECT")
        circle_objs = []
        centers = _grid_centers_4x4()
        for i in range(16):
            mat_name = f"{self.name}_circle_{i}"
            mat = bpy.data.materials.get(mat_name)
            if mat is None:
                mat = bpy.data.materials.new(name=mat_name)
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                # User-facing meaning: opacity controls perceived darkness on a white cube,
                # but we intentionally avoid transparency so Cycles doesn't produce
                # stochastic alpha artifacts.
                opacity = max(0.0, min(1.0, float(opacities[i])))
                intensity = 1.0 - opacity  # opacity=0 -> white (invisible); opacity=1 -> black
                bsdf.inputs["Base Color"].default_value = (intensity, intensity, intensity, 1.0)
                bsdf.inputs["Alpha"].default_value = 1.0
                bsdf.inputs["Roughness"].default_value = 1.0
                if "Specular IOR Level" in bsdf.inputs:
                    bsdf.inputs["Specular IOR Level"].default_value = 0.0
                elif "Specular" in bsdf.inputs:
                    bsdf.inputs["Specular"].default_value = 0.0
            mat.blend_method = "OPAQUE"

            cx, cy, cz = centers[i]
            cz = cz + _CIRCLE_Z_EPS
            radius_i = diameters_blender[i] / 2.0
            if radius_i <= 0:
                radius_i = 1e-9
            bpy.ops.object.select_all(action="DESELECT")
            bpy.ops.mesh.primitive_circle_add(
                vertices=_CIRCLE_VERTICES,
                radius=radius_i,
                fill_type="NGON",
                location=(cx, cy, cz),
            )
            obj = bpy.context.view_layer.objects.active
            obj.name = f"circle_{i}"
            if not obj.data.materials:
                obj.data.materials.append(mat)
            else:
                obj.data.materials[0] = mat
            circle_objs.append(obj)

        # Join: cube active, then select circles, join
        bpy.ops.object.select_all(action="DESELECT")
        cube_obj.select_set(True)
        bpy.context.view_layer.objects.active = cube_obj
        for obj in circle_objs:
            obj.select_set(True)
        bpy.ops.object.join()

        result = bpy.context.view_layer.objects.active
        result.name = self.name
        bpy.ops.object.select_all(action="DESELECT")
        result.select_set(True)
        bpy.context.view_layer.objects.active = result
