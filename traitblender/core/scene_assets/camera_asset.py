from .scene_asset import SceneAsset
import bpy
from ..config import CONFIG
import os

class CameraAsset(SceneAsset):
    """
    Specialized SceneAsset for managing camera objects in Blender.
    Provides convenient access to the camera data block and common camera settings.
    """
    @property
    def camera(self):
        obj = self.object
        if obj and obj.type == 'CAMERA':
            return obj.data
        raise TypeError(f"Object '{self.name}' is not a camera.")

    @property
    def type(self):
        return self.camera.type

    @type.setter
    def type(self, value):
        self.camera.type = value

    @property
    def lens(self):
        return self.camera.lens

    @lens.setter
    def lens(self, value):
        self.camera.lens = value

    @property
    def lens_unit(self):
        return self.camera.lens_unit

    @lens_unit.setter
    def lens_unit(self, value):
        self.camera.lens_unit = value

    @property
    def shift_x(self):
        return self.camera.shift_x

    @shift_x.setter
    def shift_x(self, value):
        self.camera.shift_x = value

    @property
    def shift_y(self):
        return self.camera.shift_y

    @shift_y.setter
    def shift_y(self, value):
        self.camera.shift_y = value

    @property
    def clip_start(self):
        return self.camera.clip_start

    @clip_start.setter
    def clip_start(self, value):
        self.camera.clip_start = value

    @property
    def clip_end(self):
        return self.camera.clip_end

    @clip_end.setter
    def clip_end(self, value):
        self.camera.clip_end = value

    @property
    def sensor_fit(self):
        return self.camera.sensor_fit

    @sensor_fit.setter
    def sensor_fit(self, value):
        self.camera.sensor_fit = value

    @property
    def sensor_width(self):
        return self.camera.sensor_width

    @sensor_width.setter
    def sensor_width(self, value):
        self.camera.sensor_width = value

    def render(self, filename=None, extension='png'):
        """
        Set this camera as the active scene camera and render an image.
        Uses the output render_dir from the global CONFIG dict, with optional filename and extension.
        If filename is not specified, uses Blender's default name. Default extension is 'png'.
        The full path is constructed and normalized for cross-platform compatibility.
        Raises FileNotFoundError if the render_dir does not exist.
        """
        scene = bpy.context.scene
        scene.camera = self.object
        render_dir = CONFIG.get('render_dir')
        if not render_dir or not os.path.exists(render_dir):
            raise FileNotFoundError(f"Render directory does not exist: {render_dir}")
        if filename is None:
            # Use Blender's default name for the scene
            filename = bpy.path.clean_name(scene.name)
        if not extension.startswith('.'):
            extension = '.' + extension
        full_path = os.path.normpath(os.path.join(render_dir, filename + extension))
        scene.render.filepath = full_path
        scene.render.image_settings.file_format = extension.lstrip('.').upper()
        bpy.ops.render.render(write_still=True)
