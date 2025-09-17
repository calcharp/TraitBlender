import bpy
from bpy.types import Operator

class TRAITBLENDER_OT_imaging_pipeline(Operator):
    """Iterate through the dataset and update the sample value on a timer"""
    bl_idname = "traitblender.imaging_pipeline"
    bl_label = "Run Imaging Pipeline"
    bl_description = "Iterate through the dataset, updating the sample value in the dropdown"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        pass

    def execute(self, context):
        pass

    def cancel(self, context):
        pass 