import bpy
from bpy.props import StringProperty
from ...transforms.pipeline import TransformPipeline

from ..register_config import register, TraitBlenderConfig

@register("transforms")
class TransformPipelineConfig(TraitBlenderConfig):
    pipeline_yaml: StringProperty(
        name="Pipeline YAML",
        description="Serialized TransformPipeline (YAML or JSON)",
        default=""
    )
    
    # Dynamic enums for building transforms
    selected_section: bpy.props.EnumProperty(
        name="Section",
        description="Select a configuration section",
        items=lambda self, context: self._get_section_items(),
        default=0
    )
    
    selected_property: bpy.props.EnumProperty(
        name="Property",
        description="Select a property within the section",
        items=lambda self, context: self._get_property_items(),
        default=0
    )
    
    def _get_section_items(self):
        """Get available config sections for the enum."""
        items = []
        try:
            config = bpy.context.scene.traitblender_config
            sections = config.get_config_sections()
            for i, section_name in enumerate(sections.keys()):
                items.append((section_name, section_name.replace('_', ' ').title(), f"Section {i+1}"))
        except Exception as e:
            print(f"Error getting section items: {e}")
        return items
    
    def _get_property_items(self):
        """Get available properties within the selected section."""
        items = []
        try:
            if not self.selected_section:
                return items
                
            config = bpy.context.scene.traitblender_config
            section_obj = getattr(config, self.selected_section, None)
            if section_obj and hasattr(section_obj, '__class__') and hasattr(section_obj.__class__, '__annotations__'):
                for prop_name in section_obj.__class__.__annotations__.keys():
                    if prop_name != "show":  # Skip the show property
                        items.append((prop_name, prop_name.replace('_', ' ').title(), f"Property: {prop_name}"))
        except Exception as e:
            print(f"Error getting property items: {e}")
        return items

    @property
    def pipeline(self):
        import yaml
        if self.pipeline_yaml:
            try:
                return TransformPipeline.from_dict(yaml.safe_load(self.pipeline_yaml))
            except Exception as e:
                print(f"Error loading pipeline from YAML: {e}")
                return TransformPipeline()
        return TransformPipeline()

    @pipeline.setter
    def pipeline(self, pipeline_obj):
        import yaml
        try:
            self.pipeline_yaml = yaml.dump(pipeline_obj.to_dict())
        except Exception as e:
            print(f"Error saving pipeline to YAML: {e}")

    def _to_yaml(self, indent_level=0, parent_path=""):
        """Override to provide custom YAML formatting for transforms."""
        import yaml
        indent = "  " * indent_level
        
        if not self.pipeline_yaml:
            return f"{indent}[]"
        
        try:
            transforms_list = yaml.safe_load(self.pipeline_yaml)
            if not transforms_list:
                return f"{indent}[]"
            
            # Build custom YAML with specific ordering
            result = []
            for transform in transforms_list:
                result.append(f"{indent}- property_path: {transform['property_path']}")
                result.append(f"{indent}  sampler_name: {transform['sampler_name']}")
                if transform.get('params'):
                    result.append(f"{indent}  params:")
                    for key, value in transform['params'].items():
                        result.append(f"{indent}    {key}: {value}")
            
            return '\n'.join(result)
        except Exception as e:
            print(f"Error formatting transforms YAML: {e}")
            return f"{indent}[]"

    def to_dict(self):
        """Override to provide custom dict conversion for transforms."""
        try:
            if self.pipeline_yaml:
                import yaml
                return yaml.safe_load(self.pipeline_yaml)
            return []
        except Exception as e:
            print(f"Error converting transforms to dict: {e}")
            return []

    def from_dict(self, data_dict):
        """Override to provide custom dict loading for transforms."""
        if not data_dict:
            self.pipeline_yaml = ""
            return
        
        try:
            import yaml
            self.pipeline_yaml = yaml.dump(data_dict)
        except Exception as e:
            print(f"Error loading transforms from dict: {e}")
            self.pipeline_yaml = ""

    def add_transform(self, property_path: str, sampler_name: str, params: dict = None):
        """
        Add a transform to the pipeline.
        
        Args:
            property_path (str): Relative property path (e.g., 'world.color')
            sampler_name (str): Name of the sampler function
            params (dict): Parameters for the sampler
            
        Example:
            config.add_transform("world.color", "uniform", {"low": 0, "high": 1})
        """
        try:
            # Get current pipeline
            current_pipeline = self.pipeline
            
            # Add the transform
            current_pipeline.add_transform(property_path, sampler_name, params)
            
            # Update the YAML storage
            self.pipeline = current_pipeline
            
            print(f"Added transform: {property_path} ~ {sampler_name}")
            return True
        except Exception as e:
            print(f"Error adding transform: {e}")
            return False

    def remove_transform(self, index: int):
        """
        Remove a transform from the pipeline by index.
        
        Args:
            index (int): Index of the transform to remove (0-based)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            config.remove_transform(0)  # Remove first transform
        """
        try:
            # Get current pipeline
            current_pipeline = self.pipeline
            
            if index < 0 or index >= len(current_pipeline._transforms):
                print(f"Invalid transform index: {index}")
                return False
            
            # Remove the transform
            removed_transform = current_pipeline._transforms.pop(index)
            print(f"Removed transform #{index + 1}: {removed_transform}")
            
            # Update the YAML storage
            self.pipeline = current_pipeline
            
            return True
        except Exception as e:
            print(f"Error removing transform: {e}")
            return False

    def clear_transforms(self):
        """
        Clear all transforms from the pipeline.
        
        Example:
            config.clear_transforms()
        """
        try:
            # Get current pipeline
            current_pipeline = self.pipeline
            
            # Clear all transforms
            count = len(current_pipeline._transforms)
            current_pipeline.clear()
            
            # Update the YAML storage
            self.pipeline = current_pipeline
            
            print(f"Cleared {count} transforms from pipeline")
            return True
        except Exception as e:
            print(f"Error clearing transforms: {e}")
            return False

    def get_transform_count(self):
        """Get the number of transforms in the pipeline."""
        return len(self.pipeline._transforms)

    def get_transform_info(self, index: int = None):
        """
        Get information about transforms in the pipeline.
        
        Args:
            index (int, optional): Specific transform index. If None, returns all transforms.
            
        Returns:
            dict or list: Transform information
        """
        try:
            current_pipeline = self.pipeline
            
            if index is not None:
                if index < 0 or index >= len(current_pipeline._transforms):
                    return None
                transform = current_pipeline._transforms[index]
                return {
                    'index': index,
                    'property_path': transform.property_path.replace('bpy.context.scene.traitblender_config.', ''),
                    'sampler_name': transform.sampler_name,
                    'params': transform.params.copy()
                }
            else:
                # Return all transforms
                transforms_info = []
                for i, transform in enumerate(current_pipeline._transforms):
                    transforms_info.append({
                        'index': i,
                        'property_path': transform.property_path.replace('bpy.context.scene.traitblender_config.', ''),
                        'sampler_name': transform.sampler_name,
                        'params': transform.params.copy()
                    })
                return transforms_info
        except Exception as e:
            print(f"Error getting transform info: {e}")
            return None

    def run_pipeline(self):
        """
        Execute all transforms in the pipeline.
        
        Returns:
            list: Results from each transform execution
        """
        try:
            return self.pipeline.run()
        except Exception as e:
            print(f"Error running pipeline: {e}")
            return []

    def undo_pipeline(self):
        """
        Undo all transforms in the pipeline.
        
        Returns:
            list: Results from each transform undo operation
        """
        try:
            return self.pipeline.undo()
        except Exception as e:
            print(f"Error undoing pipeline: {e}")
            return [] 