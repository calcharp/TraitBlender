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
    _image_index = 0
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
            
            # Get images_per_view from output config
            output_config = context.scene.traitblender_config.output
            images_per_view = output_config.images_per_view
            
            # Apply transforms for this image
            transforms_config = context.scene.traitblender_config.transforms
            if len(transforms_config) > 0:
                try:
                    transforms_config.run()
                    print(f"Applied transforms for sample {self._sample_index + 1}, image {self._image_index + 1}")
                except Exception as e:
                    print(f"Error applying transforms: {e}")
            
            # Update the sample value (only on first image of each specimen)
            if self._image_index == 0:
                dataset.sample = rownames[self._sample_index]
                # Refresh the UI
                for window in context.window_manager.windows:
                    for area in window.screen.areas:
                        if area.type == 'VIEW_3D':
                            area.tag_redraw()
            
            # Undo transforms before moving to next image/specimen
            if len(transforms_config) > 0:
                try:
                    transforms_config.undo()
                    print(f"Undid transforms for sample {self._sample_index + 1}, image {self._image_index + 1}")
                except Exception as e:
                    print(f"Error undoing transforms: {e}")
            
            # Move to next image or specimen
            self._image_index += 1
            if self._image_index >= images_per_view:
                # Move to next specimen
                self._sample_index += 1
                self._image_index = 0
                
        return {'PASS_THROUGH'}

    def execute(self, context):
        if self._running:
            self.report({'WARNING'}, "Imaging pipeline is already running.")
            return {'CANCELLED'}
        self._sample_index = 0
        self._image_index = 0
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
        self._image_index = 0
        self.report({'INFO'}, "Imaging pipeline cancelled.")
        return {'CANCELLED'} 