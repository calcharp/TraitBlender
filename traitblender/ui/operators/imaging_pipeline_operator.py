import bpy
from bpy.types import Operator

class TRAITBLENDER_OT_imaging_pipeline(Operator):
    """Iterate through the dataset and update the sample value on a timer"""
    bl_idname = "traitblender.imaging_pipeline"
    bl_label = "Run Imaging Pipeline"
    bl_description = "Iterate through the dataset, updating the sample value in the dropdown"
    bl_options = {'REGISTER', 'UNDO'}

    _timer = None
    _sample_index = 0
    _running = False

    def modal(self, context, event):
        if not self._running:
            return {'CANCELLED'}
        if event.type == 'TIMER':
            dataset = context.scene.traitblender_dataset
            rownames = dataset.rownames
            if not rownames:
                self.report({'WARNING'}, "No dataset loaded or dataset is empty.")
                self.cancel(context)
                return {'CANCELLED'}
            if self._sample_index >= len(rownames):
                self.report({'INFO'}, "Finished iterating through all samples.")
                self.cancel(context)
                return {'FINISHED'}
            
            # Apply all transforms at the start of the cycle
            transforms_config = context.scene.traitblender_config.transforms
            if len(transforms_config) > 0:
                try:
                    transforms_config.run()
                    transforms_config.run_pipeline()
                    print(f"Applied transforms for sample {self._sample_index + 1}")
                except Exception as e:
                    print(f"Error applying transforms: {e}")
            
            # Update the sample value
            dataset.sample = rownames[self._sample_index]
            # Refresh the UI
            for window in context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
            
            # Undo all transforms before moving to the next sample
            if len(transforms_config) > 0:
                try:
                    transforms_config.undo_pipeline()
                    print(f"Undid transforms for sample {self._sample_index + 1}")
                except Exception as e:
                    print(f"Error undoing transforms: {e}")
            
            self._sample_index += 1
        return {'PASS_THROUGH'}

    def execute(self, context):
        if self._running:
            self.report({'WARNING'}, "Imaging pipeline is already running.")
            return {'CANCELLED'}
        self._sample_index = 0
        self._running = True
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.5, window=context.window)  # 0.5 seconds per sample
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        if self._timer is not None:
            wm.event_timer_remove(self._timer)
        self._running = False
        self._timer = None
        self._sample_index = 0
        self.report({'INFO'}, "Imaging pipeline cancelled.")
        return {'CANCELLED'} 