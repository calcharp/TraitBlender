import yaml
from . import CONFIG

def register_config(yaml_path):
    """
    Loads a YAML file and updates the CONFIG dictionary in the config module.
    Supports python-specific YAML tags (e.g., !!python/tuple).
    """
    with open(yaml_path, 'r') as f:
        config_data = yaml.load(f, Loader=yaml.UnsafeLoader)
        if isinstance(config_data, dict):
            CONFIG.clear()
            CONFIG.update(config_data)
        else:
            raise ValueError('YAML file must contain a dictionary at the top level.') 