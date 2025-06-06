"""
TraitBlender Setup Scene Operator

Operator for setting up the scene for trait blending operations.
"""

import bpy
from bpy.types import Operator
import os
from ...core.helpers import get_asset_path


class TRAITBLENDER_OT_setup_scene(Operator):
    """Load the TraitBlender museum scene for morphological imaging"""
    
    bl_idname = "traitblender.setup_scene"
    bl_label = "Load Museum Scene"
    bl_description = "Load the pre-configured museum scene with lighting and camera setup"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        """Execute the setup scene operation"""
        
        # Get museum scene path using utility function
        museum_scene_path = get_asset_path("scenes", "museum_scene.blend")
        
        if os.path.exists(museum_scene_path):
            try:
                # Open the museum scene blend file
                bpy.ops.wm.open_mainfile(filepath=museum_scene_path)
                self.report({'INFO'}, "Museum scene loaded successfully from TraitBlender assets.")
            except Exception as e:
                self.report({'ERROR'}, f"Failed to load museum scene: {str(e)}")
                return {'CANCELLED'}
        else:
            self.report({'WARNING'}, f"Museum scene not found at: {museum_scene_path}")
            self.report({'INFO'}, "Scene setup cancelled - museum scene file missing")
            return {'CANCELLED'}

        return {'FINISHED'}
    
    def invoke(self, context, event):
        """Called when the operator is invoked"""
        # Check if current file has unsaved changes
        if bpy.data.is_dirty:
            return context.window_manager.invoke_confirm(self, event)
        else:
            return self.execute(context)
    
    def draw(self, context):
        """Draw the confirmation dialog"""
        layout = self.layout
        layout.label(text="Loading the museum scene will replace your current work.")
        layout.label(text="Make sure to save any important changes first.")
        layout.separator()
        layout.label(text="Continue?", icon='QUESTION') 