"""
Operator for editing the transform pipeline using the DearPyGUI interface.
"""

import bpy
from bpy.types import Operator
import sys
import os


class TRAITBLENDER_OT_edit_transforms(Operator):
    """Edit the transform pipeline using DearPyGUI interface"""
    bl_idname = "traitblender.edit_transforms"
    bl_label = "Edit Transform Pipeline"
    bl_description = "Open the transform pipeline editor"
    
    def execute(self, context):
        try:
            # Add the transforms_gui directory to the path
            addon_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            transforms_gui_path = os.path.join(addon_dir, 'misc_testing', 'transforms_gui')
            
            if transforms_gui_path not in sys.path:
                sys.path.insert(0, transforms_gui_path)
            
            # Import the transforms editor
            from transforms_editor import launch_transform_editor
            
            # Get current pipeline state from config
            config = context.scene.traitblender_config
            current_state = config.transforms.pipeline_state
            
            # Launch editor (blocking call)
            self.report({'INFO'}, "Launching transform pipeline editor...")
            new_state = launch_transform_editor(current_state)
            
            # Update config if changes were exported
            if new_state is not None:
                config.transforms.pipeline_state = new_state
                self.report({'INFO'}, "Transform pipeline updated")
            else:
                self.report({'INFO'}, "Transform editing cancelled")
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to launch transform editor: {e}")
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(TRAITBLENDER_OT_edit_transforms)


def unregister():
    bpy.utils.unregister_class(TRAITBLENDER_OT_edit_transforms)

