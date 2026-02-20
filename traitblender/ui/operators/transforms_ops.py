import bpy
from bpy.types import Operator

class TRAITBLENDER_OT_run_pipeline(Operator):
    """Run the transform pipeline"""
    
    bl_idname = "traitblender.run_pipeline"
    bl_label = "Run Pipeline"
    bl_description = "Execute all transforms in the pipeline"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        """Execute the run pipeline operation"""
        try:
            transforms_config = context.scene.traitblender_config.transforms
            results = transforms_config.run()
            
            if results:
                self.report({'INFO'}, f"Pipeline executed successfully with {len(results)} transforms")
            else:
                self.report({'WARNING'}, "Pipeline is empty - no transforms to run")
                
        except Exception as e:
            self.report({'ERROR'}, f"Failed to run pipeline: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'}


class TRAITBLENDER_OT_undo_pipeline(Operator):
    """Undo the last run of the transform pipeline"""
    
    bl_idname = "traitblender.undo_pipeline"
    bl_label = "Undo Pipeline"
    bl_description = "Undo the last run of the pipeline (step-by-step)"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        """Execute the undo pipeline operation"""
        try:
            transforms_config = context.scene.traitblender_config.transforms
            results = transforms_config.undo()
            
            if results:
                self.report({'INFO'}, f"Pipeline undone successfully with {len(results)} transforms")
            else:
                self.report({'WARNING'}, "Pipeline is empty - no transforms to undo")
                
        except Exception as e:
            self.report({'ERROR'}, f"Failed to undo pipeline: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'}


class TRAITBLENDER_OT_reset_pipeline(Operator):
    """Reset the transform pipeline to original values"""
    
    bl_idname = "traitblender.reset_pipeline"
    bl_label = "Reset Pipeline"
    bl_description = "Reset all transforms to their original values (before any runs)"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        """Execute the reset pipeline operation"""
        try:
            transforms_config = context.scene.traitblender_config.transforms
            results = transforms_config.reset()
            
            if results:
                self.report({'INFO'}, f"Pipeline reset successfully with {len(results)} transforms")
            else:
                self.report({'WARNING'}, "Pipeline is empty - no transforms to reset")
                
        except Exception as e:
            self.report({'ERROR'}, f"Failed to reset pipeline: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'}
