"""
Morphospace hyperparameters configuration.

Hyperparameters are per-morphospace and stored as YAML: {morphospace_name: {param: value}}.
The selected morphospace comes from bpy.data.scenes["Scene"].traitblender_setup.available_morphospaces.
Defaults are defined by each morphospace module's HYPERPARAMETERS export.
"""

import bpy
from bpy.props import StringProperty
import yaml
from ..register_config import register, TraitBlenderConfig
from ...morphospaces import get_hyperparameters_for_morphospace


@register("morphospace")
class MorphospaceConfig(TraitBlenderConfig):
    """Stores hyperparameter overrides per morphospace. Merged with module defaults."""

    print_index = -1  # Put near start of config

    hyperparams_state: StringProperty(
        name="Hyperparameters State",
        description="YAML: per-morphospace hyperparameter overrides {morphospace_name: {param: value}}",
        default="",
    )

    def _get_hyperparams_dict(self):
        """Parse hyperparams_state to dict."""
        if not self.hyperparams_state or not self.hyperparams_state.strip():
            return {}
        try:
            data = yaml.safe_load(self.hyperparams_state)
            return data if isinstance(data, dict) else {}
        except Exception as e:
            print(f"TraitBlender: Error parsing morphospace hyperparams: {e}")
            return {}

    def _set_hyperparams_dict(self, data):
        """Serialize dict to hyperparams_state."""
        if not data:
            self.hyperparams_state = ""
            return
        try:
            self.hyperparams_state = yaml.dump(data, default_flow_style=False, sort_keys=False)
        except Exception as e:
            print(f"TraitBlender: Error serializing morphospace hyperparams: {e}")

    def get_hyperparams_for(self, morphospace_name):
        """
        Get merged hyperparameters for a morphospace.
        Module defaults + config overrides.
        """
        module_defaults = get_hyperparameters_for_morphospace(morphospace_name)
        overrides = self._get_hyperparams_dict().get(morphospace_name, {})
        return {**module_defaults, **overrides}

    def set_hyperparam(self, morphospace_name, key, value):
        """Set one hyperparameter for a morphospace."""
        data = self._get_hyperparams_dict()
        if morphospace_name not in data:
            data[morphospace_name] = {}
        data[morphospace_name][key] = value
        self._set_hyperparams_dict(data)

    def get_hyperparam(self, morphospace_name, key):
        """Get one hyperparameter (merged with module defaults)."""
        merged = self.get_hyperparams_for(morphospace_name)
        return merged.get(key)

    def _to_yaml(self, indent_level=0, parent_path=""):
        """Format morphospace section for YAML export (called as nested section)."""
        indent = "  " * indent_level
        result = []
        data = self._get_hyperparams_dict()
        if not data:
            result.append(f"{indent}hyperparams: {{}}")
            return "\n".join(result)
        result.append(f"{indent}hyperparams:")
        for morphospace_name, params in sorted(data.items()):
            if not params:
                continue
            result.append(f"{indent}  {morphospace_name}:")
            for k, v in sorted(params.items()):
                if isinstance(v, bool):
                    result.append(f"{indent}    {k}: {str(v).lower()}")
                else:
                    result.append(f"{indent}    {k}: {v}")
        return "\n".join(result)

    def to_dict(self):
        """Return morphospace config for config export."""
        data = self._get_hyperparams_dict()
        if not data:
            return {}
        return {"hyperparams": data}

    def from_dict(self, data_dict):
        """Load morphospace config from dict (YAML import)."""
        if not data_dict or not isinstance(data_dict, dict):
            return
        # Support both {hyperparams: {CO_Raup: {...}}} and {CO_Raup: {...}} directly
        hyperparams = data_dict.get("hyperparams", data_dict)
        if isinstance(hyperparams, dict):
            self._set_hyperparams_dict(hyperparams)
