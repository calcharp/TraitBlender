"""
Camera Property Groups for TraitBlender

Defines property groups for organizing camera settings in a more structured way.
"""

import bpy
from bpy.props import (
    EnumProperty,
    FloatProperty,
    StringProperty,
    BoolProperty,
    IntProperty,
)

class CameraSettings(bpy.types.PropertyGroup):
    """All camera settings grouped together"""
    
    # Camera Type
    type: EnumProperty(
        name="Camera Type",
        items=[
            ('PERSP', "Perspective", "Perspective camera"),
            ('ORTHO', "Orthographic", "Orthographic camera"),
            ('PANO', "Panoramic", "Panoramic camera"),
        ],
        default='PERSP',
    )

    # Lens Settings
    lens: FloatProperty(
        name="Focal Length",
        default=50.0,
        min=1.0,
    )
    lens_unit: EnumProperty(
        name="Lens Unit",
        items=[
            ('MILLIMETERS', "Millimeters", "Focal length in millimeters"),
            ('FOV', "Field of View", "Field of view in degrees"),
        ],
        default='MILLIMETERS',
    )

    # Shift Settings
    shift_x: FloatProperty(
        name="Shift X",
        default=0.0,
    )
    shift_y: FloatProperty(
        name="Shift Y",
        default=0.0,
    )

    # Clipping Settings
    clip_start: FloatProperty(
        name="Clip Start",
        default=0.1,
        min=0.001,
    )
    clip_end: FloatProperty(
        name="Clip End",
        default=1000.0,
        min=0.001,
    )

    # Sensor Settings
    sensor_fit: EnumProperty(
        name="Sensor Fit",
        items=[
            ('AUTO', "Auto", "Automatic sensor fit"),
            ('HORIZONTAL', "Horizontal", "Fit to horizontal"),
            ('VERTICAL', "Vertical", "Fit to vertical"),
        ],
        default='AUTO',
    )
    sensor_width: FloatProperty(
        name="Sensor Width",
        default=36.0,
        min=0.1,
    )

    # Output Settings
    output_path: StringProperty(
        name="Output Path",
        default="/tmp/",
    )
    file_format: EnumProperty(
        name="File Format",
        items=[
            ('PNG', 'PNG', ''),
            ('JPEG', 'JPEG', ''),
            ('TIFF', 'TIFF', ''),
            ('OPEN_EXR', 'OpenEXR', ''),
        ],
        default='PNG',
    )
    color_mode: EnumProperty(
        name="Color Mode",
        items=[
            ('BW', 'BW', ''),
            ('RGB', 'RGB', ''),
            ('RGBA', 'RGBA', ''),
        ],
        default='RGBA',
    )
    color_depth: EnumProperty(
        name="Color Depth",
        items=[
            ('8', '8', ''),
            ('16', '16', ''),
        ],
        default='8',
    )
    compression: IntProperty(
        name="Compression",
        default=15,
        min=0,
        max=100,
    )
    overwrite: BoolProperty(
        name="Overwrite",
        default=True,
    )
    render_filename: StringProperty(
        name="Filename",
        default="",
    )
    render_extension: StringProperty(
        name="Extension",
        default="png",
    )

    # Metadata Settings
    METADATA_OPTIONS = [
        "Date", "Time", "Render Time", "Frame", "Frame Range", "Memory",
        "Hostname", "Camera", "Lens", "Scene", "Marker", "Filename", "Strip Name"
    ]

    METADATA_KEY_MAP = {
        "Date": "stamp_date",
        "Time": "stamp_time",
        "Render Time": "stamp_rendertime",
        "Frame": "stamp_frame",
        "Frame Range": "stamp_frame_range",
        "Memory": "stamp_memory",
        "Hostname": "stamp_hostname",
        "Camera": "stamp_camera",
        "Lens": "stamp_lens",
        "Scene": "stamp_scene",
        "Marker": "stamp_marker",
        "Filename": "stamp_filename",
        "Strip Name": "stamp_stripname",
    }

    def _get_metadata_props(self):
        """Generate metadata properties dynamically"""
        props = {}
        for label in self.METADATA_OPTIONS:
            prop_name = f"metadata_{label.replace(' ', '_').lower()}"
            props[prop_name] = BoolProperty(
                name=label,
                default=label in ["Date", "Time", "Render Time", "Frame", "Camera", "Scene", "Filename"],
            )
        return props

    # Dynamically add metadata properties
    locals().update(_get_metadata_props.__get__(None, type(None))())

classes = (CameraSettings,)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls) 