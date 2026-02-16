"""
TraitBlender Apply Orientation Operator

Applies the selected orientation function from the morphospace's ORIENTATIONS dict
to the current sample object.
"""

import bpy
from bpy.types import Operator
from ...core.morphospaces import get_orientations_for_morphospace


class TRAITBLENDER_OT_apply_orientation(Operator):
    """Apply the selected orientation function to the current sample"""

    bl_idname = "traitblender.apply_orientation"
    bl_label = "Apply Orientation"
    bl_description = "Apply the selected orientation function to the specimen"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        dataset = context.scene.traitblender_dataset
        config = context.scene.traitblender_config
        setup = context.scene.traitblender_setup

        if not dataset.sample:
            self.report({'ERROR'}, "No sample selected in dataset")
            return {'CANCELLED'}

        sample_name = dataset.sample
        if sample_name not in bpy.data.objects:
            self.report({'ERROR'}, f"Sample object '{sample_name}' not found in scene")
            return {'CANCELLED'}

        orientation_key = config.orientations.orientation
        orientations = get_orientations_for_morphospace(setup.available_morphospaces)
        if not orientation_key or orientation_key not in orientations:
            return {'FINISHED'}  # No orientation to apply

        orient_func = orientations[orientation_key]
        if not callable(orient_func):
            self.report({'ERROR'}, f"Orientation '{orientation_key}' is not callable")
            return {'CANCELLED'}

        sample_obj = bpy.data.objects[sample_name]
        try:
            orient_func(sample_obj)
            bpy.context.view_layer.update()
            self.report({'INFO'}, f"Applied orientation: {orientation_key}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to apply orientation: {str(e)}")
            return {'CANCELLED'}

        return {'FINISHED'}
