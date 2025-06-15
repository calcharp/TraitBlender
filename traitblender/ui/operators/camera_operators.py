"""
TraitBlender Camera Operators

Operators for managing camera settings in TraitBlender.
"""

import bpy
from bpy.types import Operator
from bpy.props import (
    FloatProperty,
    EnumProperty,
    StringProperty,
)
from ...core.scene_assets.asset_helpers import scene_asset

class TRAITBLENDER_OT_set_camera_type(Operator):
    """Set the camera type (PERSP, ORTHO, or PANO)"""
    bl_idname = "traitblender.set_camera_type"
    bl_label = "Set Camera Type"
    bl_options = {'REGISTER', 'UNDO'}

    camera_type: EnumProperty(
        name="Type",
        description="Camera type",
        items=[
            ('PERSP', "Perspective", "Perspective camera"),
            ('ORTHO', "Orthographic", "Orthographic camera"),
            ('PANO', "Panoramic", "Panoramic camera"),
        ],
        default='PERSP',
    )

    def execute(self, context):
        with scene_asset("Camera", "CameraAsset") as active_asset:
            active_asset.type = self.camera_type
        return {'FINISHED'}

class TRAITBLENDER_OT_set_camera_lens(Operator):
    """Set the camera lens focal length"""
    bl_idname = "traitblender.set_camera_lens"
    bl_label = "Set Camera Lens"
    bl_options = {'REGISTER', 'UNDO'}

    lens: FloatProperty(
        name="Lens",
        description="Camera lens focal length",
        min=1.0,
        default=50.0,
    )

    def execute(self, context):
        with scene_asset("Camera", "CameraAsset") as active_asset:
            active_asset.lens = self.lens
        return {'FINISHED'}

class TRAITBLENDER_OT_set_camera_lens_unit(Operator):
    """Set the camera lens unit (MILLIMETERS or FOV)"""
    bl_idname = "traitblender.set_camera_lens_unit"
    bl_label = "Set Camera Lens Unit"
    bl_options = {'REGISTER', 'UNDO'}

    lens_unit: EnumProperty(
        name="Lens Unit",
        description="Camera lens unit",
        items=[
            ('MILLIMETERS', "Millimeters", "Focal length in millimeters"),
            ('FOV', "Field of View", "Field of view in degrees"),
        ],
        default='MILLIMETERS',
    )

    def execute(self, context):
        with scene_asset("Camera", "CameraAsset") as active_asset:
            active_asset.lens_unit = self.lens_unit
        return {'FINISHED'}

class TRAITBLENDER_OT_set_camera_shift(Operator):
    """Set the camera shift values"""
    bl_idname = "traitblender.set_camera_shift"
    bl_label = "Set Camera Shift"
    bl_options = {'REGISTER', 'UNDO'}

    shift_x: FloatProperty(
        name="Shift X",
        description="Horizontal shift",
        default=0.0,
    )

    shift_y: FloatProperty(
        name="Shift Y",
        description="Vertical shift",
        default=0.0,
    )

    def execute(self, context):
        with scene_asset("Camera", "CameraAsset") as active_asset:
            active_asset.shift_x = self.shift_x
            active_asset.shift_y = self.shift_y
        return {'FINISHED'}

class TRAITBLENDER_OT_set_camera_clip(Operator):
    """Set the camera clip start and end values"""
    bl_idname = "traitblender.set_camera_clip"
    bl_label = "Set Camera Clip"
    bl_options = {'REGISTER', 'UNDO'}

    clip_start: FloatProperty(
        name="Clip Start",
        description="Near clipping distance",
        min=0.001,
        default=0.1,
    )

    clip_end: FloatProperty(
        name="Clip End",
        description="Far clipping distance",
        min=0.001,
        default=1000.0,
    )

    def execute(self, context):
        with scene_asset("Camera", "CameraAsset") as active_asset:
            active_asset.clip_start = self.clip_start
            active_asset.clip_end = self.clip_end
        return {'FINISHED'}

class TRAITBLENDER_OT_set_camera_sensor(Operator):
    """Set the camera sensor fit and width"""
    bl_idname = "traitblender.set_camera_sensor"
    bl_label = "Set Camera Sensor"
    bl_options = {'REGISTER', 'UNDO'}

    sensor_fit: EnumProperty(
        name="Sensor Fit",
        description="Camera sensor fit",
        items=[
            ('AUTO', "Auto", "Automatic sensor fit"),
            ('HORIZONTAL', "Horizontal", "Fit to horizontal"),
            ('VERTICAL', "Vertical", "Fit to vertical"),
        ],
        default='AUTO',
    )

    sensor_width: FloatProperty(
        name="Sensor Width",
        description="Camera sensor width in millimeters",
        min=0.1,
        default=36.0,
    )

    def execute(self, context):
        with scene_asset("Camera", "CameraAsset") as active_asset:
            active_asset.sensor_fit = self.sensor_fit
            active_asset.sensor_width = self.sensor_width
        return {'FINISHED'}

class TRAITBLENDER_OT_camera_render(Operator):
    """Render using the specified camera"""
    bl_idname = "traitblender.camera_render"
    bl_label = "Render Camera"
    bl_options = {'REGISTER'}

    filename: StringProperty(
        name="Filename",
        description="Output filename (without extension)",
        default="",
    )

    extension: StringProperty(
        name="Extension",
        description="Output file extension",
        default="png",
    )

    def execute(self, context):
        try:
            with scene_asset("Camera", "CameraAsset") as active_asset:
                active_asset.render(
                    filename=self.filename if self.filename else None,
                    extension=self.extension
                )
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'} 