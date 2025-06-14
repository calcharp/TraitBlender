from .scene_asset import GenericAsset
from .camera_asset import CameraAsset
from .mat_asset import MatAsset
from .table_asset import TableAsset
from .lamp_asset import LampAsset

ASSET_TYPES = {
    "GenericAsset": GenericAsset,
    "CameraAsset": CameraAsset,
    "MatAsset": MatAsset,
    "TableAsset": TableAsset,
    "LampAsset": LampAsset,
} 