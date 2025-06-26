"""
TraitBlender Setup Scene Operator

Operator for setting up the scene for trait blending operations.
"""

import bpy
from bpy.types import Operator
import os
from ...core.helpers import get_asset_path
from bpy.app.handlers import persistent

@persistent
def set_rendered_view(dummy):
    # Remove the handler so it only runs once
    if set_rendered_view in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(set_rendered_view)
    # Set all 3D viewports to rendered
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'RENDERED'

class TRAITBLENDER_OT_setup_scene(Operator):
    """Load the TraitBlender museum scene for morphological imaging"""
    
    bl_idname = "traitblender.setup_scene"
    bl_label = "Load Museum Scene"
    bl_description = "Load the pre-configured museum scene with lighting and camera setup"
    bl_options = {'REGISTER', 'UNDO'}
    
    _old_mouse_pos = None
    
    def execute(self, context):
        """Execute the setup scene operation"""
        
        # Get museum scene path using utility function
        museum_scene_path = get_asset_path("scenes", "museum_scene.blend")
        
        if os.path.exists(museum_scene_path):
            try:
                # Clear existing objects
                for obj in bpy.data.objects:
                    bpy.data.objects.remove(obj, do_unlink=True)
                
                # Set world to black
                if not context.scene.world:
                    context.scene.world = bpy.data.worlds.new("World")
                context.scene.world.use_nodes = True
                context.scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
                
                # Append objects and materials
                with bpy.data.libraries.load(museum_scene_path) as (data_from, data_to):
                    # Get all objects and materials
                    data_to.objects = data_from.objects
                    data_to.materials = data_from.materials
                
                # Link objects to scene
                for obj in data_to.objects:
                    if obj is not None:  # Skip None objects
                        bpy.context.scene.collection.objects.link(obj)
                
                # Set rendered view
                set_rendered_view(None)
                
                self.report({'INFO'}, "Museum scene objects and materials appended successfully.")
            except Exception as e:
                self.report({'ERROR'}, f"Failed to append museum scene: {str(e)}")
                return {'CANCELLED'}
        else:
            self.report({'WARNING'}, f"Museum scene not found at: {museum_scene_path}")
            self.report({'INFO'}, "Scene setup cancelled - museum scene file missing")
            return {'CANCELLED'}

        return {'FINISHED'}
    
    def invoke(self, context, event):
        """Called when the operator is invoked"""
        if bpy.data.is_dirty:
            window = context.window_manager.windows[0]
            center_x = window.width // 2
            center_y = window.height // 2
            window.cursor_warp(center_x, center_y)
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