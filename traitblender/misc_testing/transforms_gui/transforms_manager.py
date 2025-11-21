"""
Transforms Manager
Manages the transform pipeline data and operations.
"""

import yaml
import dearpygui.dearpygui as dpg


class TransformsManager:
    """Manages transform pipeline data and operations."""
    
    def __init__(self):
        self.transforms = []  # List of transform dicts
    
    def load_from_yaml(self, yaml_string):
        """Load transforms from YAML string"""
        try:
            if not yaml_string or yaml_string.strip() == "":
                self.transforms = []
                return True
            
            data = yaml.safe_load(yaml_string)
            
            if data is None:
                self.transforms = []
                return True
            
            if not isinstance(data, list):
                print(f"Invalid YAML format: expected list, got {type(data)}")
                return False
            
            # Validate each transform
            for i, transform in enumerate(data):
                if not isinstance(transform, dict):
                    print(f"Invalid transform {i}: expected dict, got {type(transform)}")
                    return False
                
                required_keys = ['property_path', 'sampler_name']
                for key in required_keys:
                    if key not in transform:
                        print(f"Invalid transform {i}: missing required key '{key}'")
                        return False
            
            self.transforms = data
            return True
            
        except yaml.YAMLError as e:
            print(f"YAML parsing error: {e}")
            return False
        except Exception as e:
            print(f"Error loading transforms: {e}")
            return False
    
    def get_yaml_string(self):
        """Export transforms to YAML string"""
        try:
            if not self.transforms:
                return ""
            return yaml.dump(self.transforms, default_flow_style=False, sort_keys=False)
        except Exception as e:
            print(f"Error exporting to YAML: {e}")
            return ""
    
    def has_transforms(self):
        """Check if there are any transforms"""
        return len(self.transforms) > 0
    
    def add_transform(self, property_path, sampler_name, params=None):
        """Add a new transform to the pipeline"""
        transform = {
            'property_path': property_path,
            'sampler_name': sampler_name
        }
        if params:
            transform['params'] = params
        
        self.transforms.append(transform)
        self.update_display()
    
    def remove_transform(self, index):
        """Remove a transform by index"""
        if 0 <= index < len(self.transforms):
            self.transforms.pop(index)
            self.update_display()
    
    def clear_all(self):
        """Clear all transforms"""
        self.transforms = []
        self.update_display()
    
    def update_display(self):
        """Update the display of transforms in the GUI"""
        if not dpg.does_item_exist("transforms_list"):
            return
        
        # Clear existing transforms display
        dpg.delete_item("transforms_list", children_only=True)
        
        # Add transforms to display
        for i, transform in enumerate(self.transforms):
            self._create_transform_card(i, transform)
    
    def _create_transform_card(self, index, transform):
        """Create a card/rectangle for displaying a transform"""
        property_path = transform.get('property_path', 'Unknown')
        sampler_name = transform.get('sampler_name', 'Unknown')
        params = transform.get('params', {})
        
        # Create a child window for the card
        card_tag = f"transform_card_{index}"
        with dpg.child_window(
            tag=card_tag,
            parent="transforms_list",
            width=-1,
            height=100,
            border=True,
            no_scrollbar=True
        ):
            # Header row with delete button
            with dpg.group(horizontal=True):
                dpg.add_text(f"Transform {index + 1}", color=(100, 150, 200))
                dpg.add_spacer(width=5)
                # Push delete button to the right
                dpg.add_button(
                    label="Delete",
                    callback=lambda: self.remove_transform(index),
                    width=60,
                    height=20
                )
            
            dpg.add_spacer(height=5)
            
            # Property path
            dpg.add_text(f"Property: {property_path}")
            
            # Sampler name
            dpg.add_text(f"Sampler: {sampler_name}")
            
            # Parameters (if any)
            if params:
                params_str = ", ".join([f"{k}={v}" for k, v in params.items()])
                dpg.add_text(f"Params: {params_str}", wrap=500)
            
            dpg.add_spacer(height=5)

