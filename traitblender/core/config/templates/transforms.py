import bpy
from bpy.props import StringProperty
from ...transforms.transform_pipeline import TransformPipeline
import yaml
from .. import config_subsection_register, TraitBlenderConfig

@config_subsection_register("transforms")
class TransformPipelineConfig(TraitBlenderConfig):
    pipeline_state: StringProperty(
        name="Pipeline State",
        description="Serialized pipeline with undo history",
        default=""
    )

    def _get_pipeline(self):
        """Deserialize pipeline from YAML string."""
        if self.pipeline_state:
            try:
                data = yaml.safe_load(self.pipeline_state)
                return TransformPipeline.from_dict(data)
            except Exception as e:
                print(f"Error loading pipeline: {e}")
                return TransformPipeline()
        return TransformPipeline()

    def _set_pipeline(self, pipeline_obj):
        """Serialize pipeline to YAML string (includes undo history)."""
        self.pipeline_state = yaml.dump(pipeline_obj.to_dict())

    @property
    def pipeline(self):
        return self._get_pipeline()

    @pipeline.setter
    def pipeline(self, pipeline_obj):
        self._set_pipeline(pipeline_obj)

    # --- Pipeline interface delegation ---
    def add_transform(self, *args, **kwargs):
        pipeline = self._get_pipeline()
        result = pipeline.add_transform(*args, **kwargs)
        self._set_pipeline(pipeline)
        return result

    def remove_transform(self, index):
        pipeline = self._get_pipeline()
        try:
            removed = pipeline._transforms.pop(index)
            self._set_pipeline(pipeline)
            print(f"Removed transform #{index + 1}: {removed}")
            return True
        except Exception as e:
            print(f"Error removing transform: {e}")
            return False

    def clear(self):
        pipeline = self._get_pipeline()
        result = pipeline.clear()
        self._set_pipeline(pipeline)
        return result

    def run(self, *args, **kwargs):
        pipeline = self._get_pipeline()
        result = pipeline.run(*args, **kwargs)
        self._set_pipeline(pipeline)
        return result

    def undo(self, *args, **kwargs):
        pipeline = self._get_pipeline()
        result = pipeline.undo(*args, **kwargs)
        self._set_pipeline(pipeline)
        return result
    
    def reset(self, *args, **kwargs):
        pipeline = self._get_pipeline()
        result = pipeline.reset(*args, **kwargs)
        self._set_pipeline(pipeline)
        return result

    def __iter__(self):
        return iter(self._get_pipeline())

    def __getitem__(self, index):
        return self._get_pipeline()[index]

    def __setitem__(self, index, value):
        pipeline = self._get_pipeline()
        pipeline[index] = value
        self._set_pipeline(pipeline)

    def __len__(self):
        return len(self._get_pipeline())

    def _to_yaml(self, indent_level=0, parent_path=""):
        """Format transforms for display in config export (clean, no history)"""
        indent = "  " * indent_level
        if not self.pipeline_state:
            return f"{indent}[]"
        try:
            data = yaml.safe_load(self.pipeline_state)
            if not data:
                return f"{indent}[]"
            
            # Extract transforms (new format is dict with 'transforms' key)
            if isinstance(data, dict):
                transforms_list = data.get('transforms', [])
            elif isinstance(data, list):
                transforms_list = data  # Old format compatibility
            else:
                return f"{indent}[]"
            
            if not transforms_list:
                return f"{indent}[]"
            
            result = []
            for transform in transforms_list:
                result.append(f"{indent}- property_path: {transform['property_path']}")
                result.append(f"{indent}  sampler_name: {transform['sampler_name']}")
                # Only show params, not _cache_stack or other internal fields
                params = transform.get('params', {})
                if params:
                    result.append(f"{indent}  params:")
                    for key, value in params.items():
                        # Skip internal fields if any
                        if not key.startswith('_'):
                            result.append(f"{indent}    {key}: {value}")
            return '\n'.join(result)
        except Exception as e:
            print(f"Error formatting transforms YAML: {e}")
            return f"{indent}[]"

    def to_dict(self):
        """Return transforms list for config export (clean, no history)"""
        try:
            data = yaml.safe_load(self.pipeline_state) if self.pipeline_state else None
            if not data:
                return []
            
            # Extract transforms without internal state
            if isinstance(data, dict):
                transforms_list = data.get('transforms', [])
            elif isinstance(data, list):
                transforms_list = data  # Old format
            else:
                return []
            
            # Clean up transforms - remove _cache_stack and internal fields
            clean_transforms = []
            for t in transforms_list:
                clean_t = {
                    'property_path': t['property_path'],
                    'sampler_name': t['sampler_name'],
                    'params': {k: v for k, v in t.get('params', {}).items()}
                }
                clean_transforms.append(clean_t)
            return clean_transforms
        except Exception as e:
            print(f"Error converting transforms to dict: {e}")
            return []

    def from_dict(self, data_dict):
        """Load transforms from a list (config import)"""
        if not data_dict:
            self.pipeline_state = ""
            return
        try:
            # data_dict is a list of transforms - load as fresh pipeline
            pipeline = TransformPipeline.from_dict(data_dict)
            self.pipeline_state = yaml.dump(pipeline.to_dict())
        except Exception as e:
            print(f"Error loading transforms from dict: {e}")
            self.pipeline_state = "" 