"""
TraitBlender Sample Origin Shift Operator

Operator for shifting a sample object's origin to (0,0,0) in table coordinates
based on the selected origin type and shift axes.
"""

import bpy
from bpy.types import Operator
from mathutils import Vector
from ...core.positioning import PLACEMENT_LOCAL_ORIGINS_TB


class TRAITBLENDER_OT_sample_origin_shift(Operator):
    """Shift the sample object's origin to (0,0,0) in table coordinates along specified axes"""
    
    bl_idname = "traitblender.sample_origin_shift"
    bl_label = "Shift Sample Origin"
    bl_description = "Shift the sample object's origin to (0,0,0) in table coordinates"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        """Execute the sample origin shift operation"""
        
        # Get the dataset and sample name
        dataset = context.scene.traitblender_dataset
        if not dataset.sample:
            self.report({'ERROR'}, "No sample selected in dataset")
            return {'CANCELLED'}
        
        sample_name = dataset.sample
        
        # Get the sample object
        if sample_name not in bpy.data.objects:
            self.report({'ERROR'}, f"Sample object '{sample_name}' not found in scene")
            return {'CANCELLED'}
        
        sample_obj = bpy.data.objects[sample_name]
        
        # Get orientation settings
        orientations_config = context.scene.traitblender_config.orientations
        origin_type = orientations_config.object_location_origin
        shift_axes = orientations_config.location_shift_axes
        
        try:
            # Calculate the object's origin in table coordinates
            origin_func = PLACEMENT_LOCAL_ORIGINS_TB.get(origin_type)
            if not origin_func:
                self.report({'ERROR'}, f"Unknown origin type: {origin_type}")
                return {'CANCELLED'}
            
            # Get the current origin in table coordinates
            current_origin_tb = origin_func(sample_obj)
            current_origin_tb = Vector(current_origin_tb)
            
            # Calculate the new position in table coordinates
            # Move the calculated origin to (0,0,0) but only along specified axes
            new_tb_coords = list(sample_obj.tb_coords)  # Get current tb_coords
            
            if 'X' in shift_axes:
                new_tb_coords[0] = -current_origin_tb.x
            if 'Y' in shift_axes:
                new_tb_coords[1] = -current_origin_tb.y
            if 'Z' in shift_axes:
                new_tb_coords[2] = -current_origin_tb.z
            
            # Set the object's position using the existing tb_coords property
            sample_obj.tb_coords = tuple(new_tb_coords)
            
            # Update the scene
            bpy.context.view_layer.update()
            
            # Report success
            self.report({'INFO'}, f"Shifted {sample_name} origin to (0,0,0) along axes: {shift_axes}")
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to shift sample origin: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'} 