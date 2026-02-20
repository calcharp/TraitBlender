import bpy
from bpy.types import Operator
import os
import re
import csv
from datetime import datetime

from ...core.morphospaces import get_orientation_names


def _sanitize_orientation_for_path(name):
    """Make orientation name safe for directory/file names."""
    s = name.replace(" ", "_").replace(",", "")
    return re.sub(r"[^\w\-]", "", s) or "orientation"


class TRAITBLENDER_OT_imaging_pipeline(Operator):
    bl_idname = "traitblender.imaging_pipeline"
    bl_label = "Run Imaging Pipeline"
    bl_options = {'REGISTER', 'UNDO'}

    _timer = None
    _specimen_idx = 0
    _orientation_idx = 0
    _img_idx = 0
    _specimens = []
    _orientations = []
    _total_specimens = 0
    _images_per_orientation = 1
    _render_dir = ""
    _log_file = None
    _csv_file = None
    _csv_writer = None

    def modal(self, context, event):
        if event.type == 'TIMER':
            dataset = context.scene.traitblender_dataset
            config = context.scene.traitblender_config

            if not dataset.csv or self._specimen_idx >= self._total_specimens:
                self._finish(context)
                return {'FINISHED'}

            name = self._specimens[self._specimen_idx]
            row = dataset.loc(name)
            orientation_name = self._orientations[self._orientation_idx]

            # Generate new specimen only at start of each specimen (first orientation, first image)
            if self._orientation_idx == 0 and self._img_idx == 0:
                if self._specimen_idx > 0:
                    prev_name = self._specimens[self._specimen_idx - 1]
                    prev_obj = bpy.data.objects.get(prev_name)
                    if prev_obj:
                        bpy.data.objects.remove(prev_obj, do_unlink=True)

                dataset.sample = name
                bpy.ops.traitblender.generate_morphospace_sample()

            # Set and apply this orientation at start of each orientation block
            if self._img_idx == 0:
                context.scene.traitblender_orientation.orientation = orientation_name
                bpy.ops.traitblender.apply_orientation()

            # Reset and run pipeline for this image
            bpy.ops.traitblender.reset_pipeline()
            bpy.ops.traitblender.run_pipeline()

            # Directory structure: render_dir / images|configs / specimen_name / orientation_sanitized /
            orient_subdir = _sanitize_orientation_for_path(orientation_name)
            images_dir = os.path.join(self._render_dir, "images", name, orient_subdir)
            configs_dir = os.path.join(self._render_dir, "configs", name, orient_subdir)
            os.makedirs(images_dir, exist_ok=True)
            os.makedirs(configs_dir, exist_ok=True)

            img_format = config.output.image_format.lower()
            config_filename = f"{name}_{self._img_idx}.yaml"
            config_path = os.path.join(configs_dir, config_filename)

            bpy.ops.traitblender.export_config(filepath=config_path)

            img_filename = f"{name}_{self._img_idx}.{img_format}"
            img_path = os.path.join(images_dir, img_filename)
            context.scene.render.filepath = img_path

            bpy.ops.traitblender.render_image()

            abs_img_path = os.path.abspath(img_path)
            abs_config_path = os.path.abspath(config_path)

            if self._csv_writer:
                self._csv_writer.writerow([name, orientation_name, self._img_idx, abs_img_path, abs_config_path])
                self._csv_file.flush()

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_msg = (
                f"[{timestamp}] [{self._specimen_idx + 1}/{self._total_specimens}] {name} "
                f"| {orientation_name} | image {self._img_idx + 1}/{self._images_per_orientation}: {dict(row)}\n"
            )
            print(log_msg.strip())
            if self._log_file:
                self._log_file.write(log_msg)
                self._log_file.flush()

            self._img_idx += 1
            if self._img_idx >= self._images_per_orientation:
                self._img_idx = 0
                self._orientation_idx += 1
                if self._orientation_idx >= len(self._orientations):
                    self._orientation_idx = 0
                    self._specimen_idx += 1

        elif event.type == 'ESC':
            self._finish(context)
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def execute(self, context):
        dataset = context.scene.traitblender_dataset
        config = context.scene.traitblender_config
        setup = context.scene.traitblender_setup

        if not dataset.csv or len(dataset.rownames) == 0:
            self.report({'WARNING'}, "No dataset loaded")
            return {'CANCELLED'}

        render_dir = config.output.rendering_directory
        if not render_dir:
            self.report({'ERROR'}, "No rendering directory specified")
            return {'CANCELLED'}

        morphospace_name = setup.available_morphospaces
        allowed = set(get_orientation_names(morphospace_name)) if morphospace_name else set()
        self._orientations = [
            item.name for item in config.imaging.orientation_options
            if item.enabled and item.name in allowed
        ]
        if not self._orientations:
            self.report({'ERROR'}, "No orientations selected for imaging. Enable at least one in the Imaging panel.")
            return {'CANCELLED'}

        try:
            os.makedirs(render_dir, exist_ok=True)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to create rendering directory: {e}")
            return {'CANCELLED'}

        self._specimens = dataset.rownames
        self._total_specimens = len(self._specimens)
        self._images_per_orientation = config.imaging.images_per_orientation
        self._render_dir = render_dir
        self._specimen_idx = 0
        self._orientation_idx = 0
        self._img_idx = 0

        log_path = os.path.join(render_dir, "rendering_log.txt")
        try:
            self._log_file = open(log_path, 'w')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._log_file.write(f"TraitBlender Rendering Log - {timestamp}\n")
            self._log_file.write(f"{'='*60}\n\n")
        except Exception as e:
            self.report({'WARNING'}, f"Failed to open log file: {e}")
            self._log_file = None

        csv_path = os.path.join(render_dir, "rendering_log.csv")
        try:
            self._csv_file = open(csv_path, 'w', newline='')
            self._csv_writer = csv.writer(self._csv_file)
            self._csv_writer.writerow(['species', 'orientation', 'index', 'image_path', 'config_path'])
        except Exception as e:
            self.report({'WARNING'}, f"Failed to open CSV file: {e}")
            self._csv_file = None
            self._csv_writer = None

        total_imgs = self._total_specimens * len(self._orientations) * self._images_per_orientation
        print(f"Rendering {self._total_specimens} specimens × {len(self._orientations)} orientations × {self._images_per_orientation} images = {total_imgs} total to {render_dir}")

        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def _finish(self, context):
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None

        if self._specimens and self._specimen_idx > 0:
            last_idx = min(self._specimen_idx - 1, len(self._specimens) - 1)
            if last_idx >= 0:
                last_name = self._specimens[last_idx]
                last_obj = bpy.data.objects.get(last_name)
                if last_obj:
                    bpy.data.objects.remove(last_obj, do_unlink=True)

        if self._csv_file:
            self._csv_file.close()
            self._csv_file = None
            self._csv_writer = None

        if self._log_file:
            if self._specimen_idx >= self._total_specimens:
                total_imgs = self._total_specimens * len(self._orientations) * self._images_per_orientation
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._log_file.write(f"\n{'='*60}\n")
                self._log_file.write(f"[{timestamp}] Rendering complete: {total_imgs} images rendered\n")
            self._log_file.close()
            self._log_file = None

        if self._specimen_idx >= self._total_specimens:
            total_imgs = self._total_specimens * len(self._orientations) * self._images_per_orientation
            print(f"Complete: rendered {total_imgs} images")
            self.report({'INFO'}, f"Rendered {total_imgs} images")
