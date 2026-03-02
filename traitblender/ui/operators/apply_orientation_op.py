"""
TraitBlender Apply Orientation Operator

Applies the selected orientation function from the morphospace's ORIENTATIONS dict
to the current sample object. Resets to rest state (from traitblender_sample) first,
then applies the orientation and bakes rotation.
"""

import bpy
from bpy.types import Operator
from mathutils import Euler
from ...core.morphospaces import get_orientations_for_morphospace
from ...core.helpers import bake_rotation_to_mesh


class TRAITBLENDER_OT_apply_orientation(Operator):
    """Apply the selected orientation function to the current sample"""

    bl_idname = "traitblender.apply_orientation"
    bl_label = "Apply Orientation"
    bl_description = "Apply the selected orientation function to the specimen"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        dataset = context.scene.traitblender_dataset
        setup = context.scene.traitblender_setup

        if not dataset.sample:
            self.report({'ERROR'}, "No sample selected in dataset")
            return {'CANCELLED'}

        sample_name = dataset.sample
        if sample_name not in bpy.data.objects:
            self.report({'ERROR'}, f"Sample object '{sample_name}' not found in scene")
            return {'CANCELLED'}

        orientation_key = context.scene.traitblender_orientation.orientation
        orientations = get_orientations_for_morphospace(setup.available_morphospaces)
        if not orientation_key or orientation_key not in orientations:
            return {'FINISHED'}  # No orientation to apply

        orient_func = orientations[orientation_key]
        if not callable(orient_func):
            self.report({'ERROR'}, f"Orientation '{orientation_key}' is not callable")
            return {'CANCELLED'}

        sample_obj = bpy.data.objects[sample_name]
        scene = context.scene
        sample_data = scene.traitblender_sample

        try:
            # Reset to rest state (as when sample was created) before applying orientation
            if bpy.context.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            sample_obj.select_set(True)
            bpy.context.view_layer.objects.active = sample_obj

            last_baked = sample_data.last_baked_rotation
            if (last_baked[0], last_baked[1], last_baked[2]) != (0.0, 0.0, 0.0):
                # Use rotation matrix inverse so Flipped (and any combined rotation) undoes correctly
                eul = Euler(last_baked)
                inv_rot = eul.to_matrix().inverted()
                sample_obj.rotation_euler = inv_rot.to_euler(eul.order)
                bpy.ops.object.transform_apply(rotation=True)
                sample_data.last_baked_rotation = (0.0, 0.0, 0.0)

            # Restore baseline rotation (do NOT change origin or location here)
            sample_obj.rotation_euler = Euler(sample_data.rest_rotation)
            bpy.context.view_layer.update()

            orient_func(sample_obj)
            bpy.context.view_layer.update()

            sample_data.last_baked_rotation = tuple(sample_obj.rotation_euler)
            bake_rotation_to_mesh(sample_name)
            # Ensure origin is always the geometry bounds center (not world origin)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
            bpy.context.view_layer.update()

            self.report({'INFO'}, f"Applied orientation: {orientation_key}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to apply orientation: {str(e)}")
            return {'CANCELLED'}

        return {'FINISHED'}
