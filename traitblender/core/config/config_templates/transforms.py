import bpy
from bpy.props import StringProperty
from ...transforms.pipeline import TransformPipeline
import yaml
from ..register_config import register, TraitBlenderConfig

@register("transforms")
class TransformPipelineConfig(TraitBlenderConfig):
    pipeline_state: StringProperty(
        name="Pipeline State",
        description="Serialized state of the pipeline (including undo history)",
        default=""
    )

    def _get_pipeline(self):
        if self.pipeline_state:
            try:
                data = yaml.safe_load(self.pipeline_state)
                return TransformPipeline.from_dict(data)
            except Exception as e:
                print(f"Error loading pipeline from state: {e}")
                return TransformPipeline()
        return TransformPipeline()

    def _set_pipeline(self, pipeline_obj):
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
        indent = "  " * indent_level
        if not self.pipeline_state:
            return f"{indent}[]"
        try:
            transforms_list = yaml.safe_load(self.pipeline_state)
            if not transforms_list:
                return f"{indent}[]"
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
        try:
            return self._get_pipeline().to_dict()
        except Exception as e:
            print(f"Error converting transforms to dict: {e}")
            return []

    def from_dict(self, data_dict):
        if not data_dict:
            self.pipeline_state = ""
            return
        try:
            self.pipeline_state = yaml.dump(data_dict)
        except Exception as e:
            print(f"Error loading transforms from dict: {e}")
            self.pipeline_state = "" 