import bpy
from ..register_config import register, TraitBlenderConfig

@register("orientations")
class OrientationsConfig(TraitBlenderConfig):
    print_index = 1
    
    object_location_origin: bpy.props.EnumProperty(
        name="Object Location Origin",
        description="Select the origin type for object positioning",
        items=lambda self, context: self._get_origin_items(),
        default=0
    )
    
    location_shift_axes: bpy.props.EnumProperty(
        name="Location Shift Axes",
        description="Select which axes to apply location shifts to",
        items=lambda self, context: self._get_shift_axes_items(),
        default=0
    )
    
    def _get_origin_items(self):
        """Dynamically generate enum items from PLACEMENT_LOCAL_ORIGINS_TB keys"""
        items = []
        try:
            from ...positioning import PLACEMENT_LOCAL_ORIGINS_TB
            for i, origin_key in enumerate(sorted(PLACEMENT_LOCAL_ORIGINS_TB.keys())):
                # Convert key to display name (e.g., 'GEOM_BOUNDS' -> 'Geom Bounds')
                display_name = origin_key.replace('_', ' ').title()
                items.append((origin_key, display_name, f"Origin: {display_name}"))
        except Exception as e:
            print(f"Error getting origin items: {e}")
            # Fallback items if import fails
            items = [
                ('OBJECT', 'Object', 'Object origin'),
                ('GEOM_BOUNDS', 'Geom Bounds', 'Geometric bounds center'),
                ('MEAN', 'Mean', 'Mean vertex position'),
                ('MEDIAN', 'Median', 'Median vertex position'),
            ]
        return items
    
    def _get_shift_axes_items(self):
        """Dynamically generate enum items from LOCATION_SHIFT_AXES_TB set"""
        items = []
        try:
            from ...positioning import LOCATION_SHIFT_AXES_TB
            for i, axes_key in enumerate(sorted(LOCATION_SHIFT_AXES_TB)):
                # Convert key to display name (e.g., 'XY' -> 'X Y')
                display_name = ' '.join(axes_key)
                items.append((axes_key, display_name, f"Axes: {display_name}"))
        except Exception as e:
            print(f"Error getting shift axes items: {e}")
            # Fallback items if import fails
            items = [
                ('X', 'X', 'X axis only'),
                ('Y', 'Y', 'Y axis only'),
                ('Z', 'Z', 'Z axis only'),
                ('XY', 'X Y', 'X and Y axes'),
                ('XZ', 'X Z', 'X and Z axes'),
                ('YZ', 'Y Z', 'Y and Z axes'),
                ('XYZ', 'X Y Z', 'All axes'),
            ]
        return items 