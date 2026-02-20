import bpy
from bpy.types import Operator
import os
import csv
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
    _csv_file = None
    _csv_writer = None

    def modal(self, context, event):
        if event.type == 'TIMER':
            dataset = context.scene.traitblender_dataset
            if not dataset.csv or self._idx >= self._total:
                self._finish(context)
                return {'FINISHED'}
            
            name = self._specimens[self._idx]
            row = dataset.loc(name)
            config = context.scene.traitblender_config
            
            # Generate new specimen at start of each specimen
            if self._img_idx == 0:
                # Delete previous specimen (except first one)
                if self._idx > 0:
                    prev_name = self._specimens[self._idx - 1]
                    prev_obj = bpy.data.objects.get(prev_name)
                    if prev_obj:
                        bpy.data.objects.remove(prev_obj, do_unlink=True)
                
                # Generate new specimen (auto-applies Default orientation)
                dataset.sample = name
                bpy.ops.traitblender.generate_morphospace_sample()
            
            # Reset and run pipeline for each variation
            bpy.ops.traitblender.reset_pipeline()
            bpy.ops.traitblender.run_pipeline()
            
            # Create directory structure
            images_dir = os.path.join(self._render_dir, "images", name)
            configs_dir = os.path.join(self._render_dir, "configs", name)
            os.makedirs(images_dir, exist_ok=True)
            os.makedirs(configs_dir, exist_ok=True)
            
            # Export config after transforms
            img_format = config.output.image_format.lower()
            config_filename = f"{name}_{self._img_idx}.yaml"
            config_path = os.path.join(configs_dir, config_filename)
            
            # Use export_config operator
            bpy.ops.traitblender.export_config(filepath=config_path)
            
            # Set render filepath
            img_filename = f"{name}_{self._img_idx}.{img_format}"
            img_path = os.path.join(images_dir, img_filename)
            context.scene.render.filepath = img_path
            
            # Render image
            bpy.ops.traitblender.render_image()
            
            # Get absolute paths
            abs_img_path = os.path.abspath(img_path)
            abs_config_path = os.path.abspath(config_path)
            
            # Write to CSV
            if self._csv_writer:
                self._csv_writer.writerow([name, self._img_idx, abs_img_path, abs_config_path])
                self._csv_file.flush()
            
            # Log info with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_msg = f"[{timestamp}] [{self._idx + 1}/{self._total}] {name} (image {self._img_idx + 1}/{self._imgs_per}): {dict(row)}\n"
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
        
        # Open CSV file
        csv_path = os.path.join(render_dir, "rendering_log.csv")
        try:
            self._csv_file = open(csv_path, 'w', newline='')
            self._csv_writer = csv.writer(self._csv_file)
            self._csv_writer.writerow(['species', 'index', 'image_path', 'config_path'])
        except Exception as e:
            self.report({'WARNING'}, f"Failed to open CSV file: {e}")
            self._csv_file = None
            self._csv_writer = None
        
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
        
        # Clean up last specimen
        if self._specimens and self._idx > 0:
            last_idx = min(self._idx - 1, len(self._specimens) - 1)
            if last_idx >= 0:
                last_name = self._specimens[last_idx]
                last_obj = bpy.data.objects.get(last_name)
                if last_obj:
                    bpy.data.objects.remove(last_obj, do_unlink=True)
        
        # Close CSV file
        if self._csv_file:
            self._csv_file.close()
            self._csv_file = None
            self._csv_writer = None
        
        # Close log file
        if self._log_file:
            if self._idx >= self._total:
                total_imgs = self._total * self._imgs_per
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._log_file.write(f"\n{'='*60}\n")
                self._log_file.write(f"[{timestamp}] Rendering complete: {total_imgs} images rendered\n")
            self._log_file.close()
            self._log_file = None
        
        if self._idx >= self._total:
            total_imgs = self._total * self._imgs_per
            print(f"Complete: rendered {self._total} specimens ({total_imgs} total images)")
            self.report({'INFO'}, f"Rendered {total_imgs} images")
