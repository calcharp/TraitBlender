"""
TraitBlender Clear Scene Operator

Operator for clearing the current scene with confirmation dialog.
"""

import bpy
from bpy.types import Operator
from ...core.helpers import clear_scene


class TRAITBLENDER_OT_clear_scene(Operator):
    """Clear all objects and data from the current scene"""
    
    bl_idname = "traitblender.clear_scene"
    bl_label = "Clear Scene"
    bl_description = "Remove all objects, materials, and data from the current scene"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        """Execute the clear scene operation"""
        try:
            # Clear the scene
            removed_counts = clear_scene()
            
            # Report success
            total_removed = sum(removed_counts.values())
            if total_removed > 0:
                self.report({'INFO'}, f"Scene cleared: {total_removed} items removed")
            else:
                self.report({'INFO'}, "Scene was already empty")
                
        except Exception as e:
            self.report({'ERROR'}, f"Failed to clear scene: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        """Called when the operator is invoked - shows confirmation dialog"""
        return context.window_manager.invoke_confirm(self, event)
    
    def draw(self, context):
        """Draw the confirmation dialog"""
        layout = self.layout
        layout.label(text="This will remove ALL objects, materials, and data from the scene.")
        layout.label(text="This action cannot be undone.")
        layout.separator()
        layout.label(text="Are you sure you want to clear the scene?", icon='ERROR') 