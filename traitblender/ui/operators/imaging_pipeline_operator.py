import bpy
from bpy.types import Operator
import os
from datetime import datetime

class TRAITBLENDER_OT_imaging_pipeline(Operator):
    bl_idname = "traitblender.imaging_pipeline"
    bl_label = "Run Imaging Pipeline"
    bl_options = {'REGISTER', 'UNDO'}
    
    _timer = None
    _idx = 0
    _img_idx = 0
    _specimens = []
    _total = 0
    _imgs_per = 1
    _render_dir = ""
    _log_file = None

    def modal(self, context, event):
        if event.type == 'TIMER':
            dataset = context.scene.traitblender_dataset
            if not dataset.csv or self._idx >= self._total:
                self._finish(context)
                return {'FINISHED'}
            
            name = self._specimens[self._idx]
            row = dataset.loc(name)
            config = context.scene.traitblender_config
            
            # Reset and run pipeline for each variation
            bpy.ops.traitblender.reset_pipeline()
            bpy.ops.traitblender.run_pipeline()
            
            # Create species subdirectory
            species_dir = os.path.join(self._render_dir, name)
            os.makedirs(species_dir, exist_ok=True)
            
            # Set render filepath
            img_format = config.output.image_format.lower()
            filename = f"{name}_{self._img_idx}.{img_format}"
            filepath = os.path.join(species_dir, filename)
            context.scene.render.filepath = filepath
            
            # Render image
            bpy.ops.traitblender.render_image()
            
            # Log info
            log_msg = f"[{self._idx + 1}/{self._total}] {name} (image {self._img_idx + 1}/{self._imgs_per}): {dict(row)}\n"
            print(log_msg.strip())
            if self._log_file:
                self._log_file.write(log_msg)
                self._log_file.flush()
            
            self._img_idx += 1
            if self._img_idx >= self._imgs_per:
                self._idx += 1
                self._img_idx = 0
        
        elif event.type == 'ESC':
            self._finish(context)
            return {'CANCELLED'}
        
        return {'PASS_THROUGH'}

    def execute(self, context):
        dataset = context.scene.traitblender_dataset
        config = context.scene.traitblender_config
        
        if not dataset.csv or len(dataset.rownames) == 0:
            self.report({'WARNING'}, "No dataset loaded")
            return {'CANCELLED'}
        
        # Validate rendering directory
        render_dir = config.output.rendering_directory
        if not render_dir:
            self.report({'ERROR'}, "No rendering directory specified")
            return {'CANCELLED'}
        
        # Create rendering directory
        try:
            os.makedirs(render_dir, exist_ok=True)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to create rendering directory: {e}")
            return {'CANCELLED'}
        
        self._specimens = dataset.rownames
        self._total = len(self._specimens)
        self._imgs_per = config.output.images_per_view
        self._render_dir = render_dir
        self._idx = 0
        self._img_idx = 0
        
        # Open log file
        log_path = os.path.join(render_dir, "rendering_log.txt")
        try:
            self._log_file = open(log_path, 'w')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._log_file.write(f"TraitBlender Rendering Log - {timestamp}\n")
            self._log_file.write(f"{'='*60}\n\n")
        except Exception as e:
            self.report({'WARNING'}, f"Failed to open log file: {e}")
            self._log_file = None
        
        total_imgs = self._total * self._imgs_per
        print(f"Rendering {self._total} specimens ({total_imgs} total images) to {render_dir}")
        
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
    def _finish(self, context):
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None
        
        # Close log file
        if self._log_file:
            if self._idx >= self._total:
                total_imgs = self._total * self._imgs_per
                self._log_file.write(f"\n{'='*60}\n")
                self._log_file.write(f"Rendering complete: {total_imgs} images rendered\n")
            self._log_file.close()
            self._log_file = None
        
        if self._idx >= self._total:
            total_imgs = self._total * self._imgs_per
            print(f"Complete: rendered {self._total} specimens ({total_imgs} total images)")
            self.report({'INFO'}, f"Rendered {total_imgs} images") 