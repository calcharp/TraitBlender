import bpy
from .. import config_subsection_register, TraitBlenderConfig


@config_subsection_register("sample")
class SampleConfig(TraitBlenderConfig):
    print_index = 8
    
    # This configuration should not appear in the config file
    # It's only for UI controls in the datasets panel
    
    def _get_sample_object_name(self):
        """Get the current sample object name from the dataset."""
        try:
            return bpy.context.scene.traitblender_dataset.sample
        except:
            return None
    
    def _get_rotation(self):
        """Get the rotation of the current sample object."""
        obj_name = self._get_sample_object_name()
        if obj_name and obj_name in bpy.data.objects:
            return bpy.data.objects[obj_name].rotation_euler
        return (0.0, 0.0, 0.0)
    
    def _set_rotation(self, value):
        """Set the rotation of the current sample object."""
        obj_name = self._get_sample_object_name()
        if obj_name and obj_name in bpy.data.objects:
            bpy.data.objects[obj_name].rotation_euler = value
    
    rotation: bpy.props.FloatVectorProperty(
        name="Sample Rotation",
        description="The rotation of the generated sample object",
        default=(0.0, 0.0, 0.0),
        subtype='EULER',
        get=lambda self: self._get_rotation(),
        set=lambda self, value: self._set_rotation(value)
    )
    
    def _to_yaml(self, indent_level=0, parent_path=""):
        """Override to prevent this configuration from appearing in YAML output."""
        return ""  # Return empty string so it doesn't appear in config file 