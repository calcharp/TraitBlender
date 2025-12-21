"""
Transforms Manager
Manages the transform pipeline data and operations.
"""

import yaml
import dearpygui.dearpygui as dpg
from .property_helper import (
    get_available_sections,
    get_properties_for_section,
    build_property_path,
    parse_property_path,
    get_available_samplers
)
from .sampler_helper import (
    get_sampler_signature,
    validate_parameter_value,
    format_parameter_value
)
from .property_dimension_helper import (
    get_property_dimension,
    should_auto_set_n_parameter
)


class TransformsManager:
    """Manages transform pipeline data and operations."""
    
    def __init__(self):
        self.transforms = []  # List of transform dicts
        self.last_moved_index = -1  # Track last moved transform for highlighting
    
    def load_from_yaml(self, yaml_string):
        """Load transforms from YAML string (handles both old list and new dict formats)"""
        try:
            if not yaml_string or yaml_string.strip() == "":
                self.transforms = []
                return True
            
            data = yaml.safe_load(yaml_string)
            
            if data is None:
                self.transforms = []
                return True
            
            # Handle both formats: old (list) and new (dict with 'transforms' key)
            if isinstance(data, dict):
                # New format: extract the transforms list, ignore history
                transforms_list = data.get('transforms', [])
            elif isinstance(data, list):
                # Old format: data is the transforms list
                transforms_list = data
            else:
                print(f"Invalid YAML format: expected list or dict, got {type(data)}")
                return False
            
            # Validate each transform
            for i, transform in enumerate(transforms_list):
                if not isinstance(transform, dict):
                    print(f"Invalid transform {i}: expected dict, got {type(transform)}")
                    return False
                
                required_keys = ['property_path', 'sampler_name']
                for key in required_keys:
                    if key not in transform:
                        print(f"Invalid transform {i}: missing required key '{key}'")
                        return False
            
            # Strip out _cache_stack and other internal fields for clean editing
            clean_transforms = []
            for t in transforms_list:
                clean_t = {
                    'property_path': t['property_path'],
                    'sampler_name': t['sampler_name'],
                    'params': t.get('params', {})
                }
                clean_transforms.append(clean_t)
            
            self.transforms = clean_transforms
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
    
    def move_transform(self, from_index, to_index):
        """Move a transform from one position to another"""
        if 0 <= from_index < len(self.transforms) and 0 <= to_index < len(self.transforms):
            if from_index != to_index:
                # Remove from old position
                transform = self.transforms.pop(from_index)
                # Insert at new position
                self.transforms.insert(to_index, transform)
                self.last_moved_index = to_index
                self.update_display()
    
    def clear_all(self):
        """Clear all transforms"""
        self.transforms = []
        self.last_moved_index = -1
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
        """Create a card using group with separator for auto-sizing"""
        property_path = transform.get('property_path', 'Unknown')
        sampler_name = transform.get('sampler_name', 'Unknown')
        params = transform.get('params', {})
        
        # Parse current property path
        current_section, current_property = parse_property_path(property_path)
        
        # Get available sections and properties
        sections = get_available_sections()
        section_names = [s[0] for s in sections]
        section_display = [s[1] for s in sections]
        
        # Get sampler signature for dynamic parameter inputs
        param_signature = get_sampler_signature(sampler_name)
        
        # Auto-set 'n' parameter based on property dimension
        should_auto_set, dimension = should_auto_set_n_parameter(property_path)
        if should_auto_set and dimension is not None:
            self.transforms[index]['params']['n'] = dimension
        
        # Highlight if this was just moved
        is_highlighted = (index == self.last_moved_index)
        title_color = (150, 220, 150) if is_highlighted else (100, 150, 200)
        
        card_tag = f"transform_card_{index}"
        content_group_tag = f"content_group_{index}"
        
        # Use group for auto-sizing - groups naturally size to content
        with dpg.group(
            tag=card_tag,
            parent="transforms_list",
            drop_callback=lambda s, a: self._handle_drop(index, a),
            payload_type="TRANSFORM_REORDER"
        ):
            # Create a group for content and make it draggable
            with dpg.group(tag=content_group_tag):
                # Header row with title and delete button
                with dpg.group(horizontal=True):
                    dpg.add_text(f"Transform {index + 1}", color=title_color)
                    dpg.add_spacer(width=395)
                    dpg.add_button(
                        label="Delete",
                        callback=lambda s, a, u: self.remove_transform(u),
                        width=60,
                        user_data=index
                    )
                
                dpg.add_spacer(height=3)
                
                # Property path selection row
                with dpg.group(horizontal=True):
                    dpg.add_text("Property:")
                    dpg.add_spacer(width=5)
                    
                    # Section combo
                    default_section_idx = section_names.index(current_section) if current_section in section_names else 0
                    section_combo_tag = f"section_combo_{index}"
                    dpg.add_combo(
                        tag=section_combo_tag,
                        items=section_display,
                        default_value=section_display[default_section_idx] if section_display else "",
                        width=120,
                        callback=lambda s, a, u: self._on_section_changed(u, a, s),
                        user_data=index
                    )
                    
                    dpg.add_spacer(width=5)
                    
                    # Property combo
                    properties = get_properties_for_section(current_section) if current_section else []
                    property_names = [p[0] for p in properties]
                    property_display = [p[1] for p in properties]
                    default_property_idx = property_names.index(current_property) if current_property in property_names else 0
                    
                    property_combo_tag = f"property_combo_{index}"
                    dpg.add_combo(
                        tag=property_combo_tag,
                        items=property_display,
                        default_value=property_display[default_property_idx] if property_display else "",
                        width=120,
                        callback=lambda s, a, u: self._on_property_changed(u, a),
                        user_data=index
                    )
                
                dpg.add_spacer(height=3)
                
                # Sampler selection row
                with dpg.group(horizontal=True):
                    dpg.add_text("Sampler:")
                    dpg.add_spacer(width=10)
                    
                    samplers = get_available_samplers()
                    sampler_names = [s[0] for s in samplers]
                    sampler_display = [s[1] for s in samplers]
                    default_sampler_idx = sampler_names.index(sampler_name) if sampler_name in sampler_names else 0
                    
                    sampler_combo_tag = f"sampler_combo_{index}"
                    dpg.add_combo(
                        tag=sampler_combo_tag,
                        items=sampler_display,
                        default_value=sampler_display[default_sampler_idx] if sampler_display else "",
                        width=150,
                        callback=lambda s, a, u: self._on_sampler_changed(u, a),
                        user_data=index
                    )
                
                dpg.add_spacer(height=3)
                
                # Dynamic parameter inputs
                visible_params = {k: v for k, v in param_signature.items() if k != 'n'}
                if visible_params:
                    dpg.add_text("Parameters:", color=(180, 180, 180))
                    dpg.add_spacer(height=2)
                    
                    for param_name, param_info in visible_params.items():
                        self._create_parameter_input(
                            index=index,
                            param_name=param_name,
                            param_info=param_info,
                            current_value=params.get(param_name)
                        )
            
            # Attach drag payload to the content group
            with dpg.drag_payload(parent=content_group_tag, drag_data=index, payload_type="TRANSFORM_REORDER"):
                dpg.add_text(f"Moving Transform {index + 1}: {property_path} ~ {sampler_name}", color=(150, 220, 150))
            
            # Separator between cards
            dpg.add_spacer(height=5)
            dpg.add_separator()
            dpg.add_spacer(height=5)
    
    def _create_parameter_input(self, index, param_name, param_info, current_value):
        """Create an input field for a parameter based on its type."""
        type_str = param_info['type_str']
        required = param_info['required']
        property_path = self.transforms[index].get('property_path', '')
        
        # Get property dimension for sizing vector/matrix inputs
        dimension = get_property_dimension(property_path)
        
        # Label with type hint and required indicator
        label_text = f"  {param_name} ({type_str})"
        if required:
            label_text += " *"
        
        dpg.add_text(label_text, color=(200, 200, 200) if required else (150, 150, 150))
        dpg.add_spacer(height=2)
        
        # Create appropriate input widget based on type
        if type_str == 'list[list[float]]':
            # Matrix input - grid of float inputs
            self._create_matrix_input(index, param_name, current_value, dimension)
        elif type_str == 'list[float]':
            # Vector input - row of float inputs
            self._create_vector_input(index, param_name, current_value, dimension)
        elif type_str == 'list[int]':
            # Vector input - row of int inputs
            self._create_vector_input(index, param_name, current_value, dimension, is_int=True)
        else:
            # Scalar input
            self._create_scalar_input(index, param_name, current_value, type_str)
    
    def _create_scalar_input(self, index, param_name, current_value, type_str):
        """Create a scalar input field."""
        value_str = format_parameter_value(current_value) if current_value is not None else ""
        input_tag = f"param_input_{index}_{param_name}"
        
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=10)
            dpg.add_input_text(
                tag=input_tag,
                default_value=value_str,
                width=100,
                callback=lambda s, a, u: self._on_scalar_changed(u['index'], u['param_name'], a, u['type_str']),
                user_data={'index': index, 'param_name': param_name, 'type_str': type_str}
            )
    
    def _create_vector_input(self, index, param_name, current_value, dimension, is_int=False):
        """Create a vector input as a row of input boxes."""
        # Determine vector size
        if current_value and isinstance(current_value, (list, tuple)):
            size = len(current_value)
        elif dimension:
            size = dimension
        else:
            size = 3  # Default
        
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=10)
            
            for i in range(size):
                input_tag = f"param_input_{index}_{param_name}_{i}"
                value = current_value[i] if current_value and i < len(current_value) else (0 if is_int else 0.0)
                
                dpg.add_input_text(
                    tag=input_tag,
                    default_value=str(value),
                    width=60,
                    callback=lambda s, a, u: self._on_vector_element_changed(
                        u['index'], u['param_name'], u['element_idx'], a, u['is_int']
                    ),
                    user_data={'index': index, 'param_name': param_name, 'element_idx': i, 'is_int': is_int}
                )
                
                if i < size - 1:
                    dpg.add_spacer(width=3)
    
    def _create_matrix_input(self, index, param_name, current_value, dimension):
        """Create a matrix input as a grid of input boxes."""
        # Determine matrix size (assume square matrix based on dimension)
        if current_value and isinstance(current_value, (list, tuple)) and current_value:
            rows = len(current_value)
            cols = len(current_value[0]) if isinstance(current_value[0], (list, tuple)) else rows
        elif dimension:
            rows = cols = dimension
        else:
            rows = cols = 3  # Default 3×3
        
        dpg.add_spacer(width=10, height=2)
        
        for row_idx in range(rows):
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=10)
                
                for col_idx in range(cols):
                    input_tag = f"param_input_{index}_{param_name}_{row_idx}_{col_idx}"
                    
                    # Get value from current_value if available
                    if (current_value and isinstance(current_value, (list, tuple)) and 
                        row_idx < len(current_value) and 
                        isinstance(current_value[row_idx], (list, tuple)) and 
                        col_idx < len(current_value[row_idx])):
                        value = current_value[row_idx][col_idx]
                    else:
                        # Default: identity matrix
                        value = 1.0 if row_idx == col_idx else 0.0
                    
                    dpg.add_input_text(
                        tag=input_tag,
                        default_value=str(value),
                        width=60,
                        callback=lambda s, a, u: self._on_matrix_element_changed(
                            u['index'], u['param_name'], u['row_idx'], u['col_idx'], a
                        ),
                        user_data={'index': index, 'param_name': param_name, 'row_idx': row_idx, 'col_idx': col_idx}
                    )
                    
                    if col_idx < cols - 1:
                        dpg.add_spacer(width=3)
            
            if row_idx < rows - 1:
                dpg.add_spacer(height=3)
    
    def _on_scalar_changed(self, index, param_name, value_str, type_str):
        """Handle scalar parameter value change with validation."""
        if not (0 <= index < len(self.transforms)):
            return
        
        # Validate and convert the value
        success, result = validate_parameter_value(value_str, type_str)
        
        input_tag = f"param_input_{index}_{param_name}"
        
        if success:
            # Update the transform's params
            self.transforms[index]['params'][param_name] = result
            # Set input field to normal color (white text)
            if dpg.does_item_exist(input_tag):
                dpg.configure_item(input_tag, color=(255, 255, 255, 255))
            print(f"Updated transform {index + 1} parameter '{param_name}' = {result}")
        else:
            # Show validation error with red text
            if dpg.does_item_exist(input_tag):
                dpg.configure_item(input_tag, color=(255, 100, 100, 255))
            print(f"Invalid value for '{param_name}': {result}")
    
    def _on_vector_element_changed(self, index, param_name, element_idx, value_str, is_int):
        """Handle vector element change."""
        if not (0 <= index < len(self.transforms)):
            return
        
        input_tag = f"param_input_{index}_{param_name}_{element_idx}"
        
        try:
            # Convert value
            value = int(value_str) if is_int else float(value_str)
            
            # Get or create the vector
            if param_name not in self.transforms[index]['params']:
                # Determine size from property dimension
                property_path = self.transforms[index].get('property_path', '')
                dimension = get_property_dimension(property_path) or 3
                self.transforms[index]['params'][param_name] = [0] * dimension if is_int else [0.0] * dimension
            
            # Update the specific element
            current_vector = self.transforms[index]['params'][param_name]
            if element_idx < len(current_vector):
                current_vector[element_idx] = value
                
                # Set input field to normal color
                if dpg.does_item_exist(input_tag):
                    dpg.configure_item(input_tag, color=(255, 255, 255, 255))
                
                print(f"Updated transform {index + 1} parameter '{param_name}'[{element_idx}] = {value}")
        except ValueError:
            # Show validation error with red text
            if dpg.does_item_exist(input_tag):
                dpg.configure_item(input_tag, color=(255, 100, 100, 255))
            print(f"Invalid value for '{param_name}'[{element_idx}]: must be {'int' if is_int else 'float'}")
    
    def _on_matrix_element_changed(self, index, param_name, row_idx, col_idx, value_str):
        """Handle matrix element change."""
        if not (0 <= index < len(self.transforms)):
            return
        
        input_tag = f"param_input_{index}_{param_name}_{row_idx}_{col_idx}"
        
        try:
            # Convert value
            value = float(value_str)
            
            # Get or create the matrix
            if param_name not in self.transforms[index]['params']:
                # Determine size from property dimension
                property_path = self.transforms[index].get('property_path', '')
                dimension = get_property_dimension(property_path) or 3
                # Initialize identity matrix
                self.transforms[index]['params'][param_name] = [
                    [1.0 if i == j else 0.0 for j in range(dimension)]
                    for i in range(dimension)
                ]
            
            # Update the specific element
            current_matrix = self.transforms[index]['params'][param_name]
            if row_idx < len(current_matrix) and col_idx < len(current_matrix[row_idx]):
                current_matrix[row_idx][col_idx] = value
                
                # Set input field to normal color
                if dpg.does_item_exist(input_tag):
                    dpg.configure_item(input_tag, color=(255, 255, 255, 255))
                
                print(f"Updated transform {index + 1} parameter '{param_name}'[{row_idx}][{col_idx}] = {value}")
        except ValueError:
            # Show validation error with red text
            if dpg.does_item_exist(input_tag):
                dpg.configure_item(input_tag, color=(255, 100, 100, 255))
            print(f"Invalid value for '{param_name}'[{row_idx}][{col_idx}]: must be float")
    
    def _on_section_changed(self, index, display_value, sender):
        """Handle section selection change"""
        # Convert display value back to section name
        sections = get_available_sections()
        section_name = None
        for sect_name, sect_display in sections:
            if sect_display == display_value:
                section_name = sect_name
                break
        
        if section_name is None:
            return
        
        # Update property combo with new section's properties
        properties = get_properties_for_section(section_name)
        property_names = [p[0] for p in properties]
        property_display = [p[1] for p in properties]
        
        property_combo_tag = f"property_combo_{index}"
        if dpg.does_item_exist(property_combo_tag):
            dpg.configure_item(property_combo_tag, items=property_display)
            if property_display:
                dpg.set_value(property_combo_tag, property_display[0])
                # Update the transform with the new path
                self._update_property_path(index, section_name, property_names[0])
    
    def _on_property_changed(self, index, display_value):
        """Handle property selection change"""
        # Get current section
        section_combo_tag = f"section_combo_{index}"
        if not dpg.does_item_exist(section_combo_tag):
            return
        
        section_display = dpg.get_value(section_combo_tag)
        sections = get_available_sections()
        section_name = None
        for sect_name, sect_display in sections:
            if sect_display == section_display:
                section_name = sect_name
                break
        
        if section_name is None:
            return
        
        # Convert display value back to property name
        properties = get_properties_for_section(section_name)
        property_name = None
        for prop_name, prop_display in properties:
            if prop_display == display_value:
                property_name = prop_name
                break
        
        if property_name:
            self._update_property_path(index, section_name, property_name)
    
    def _update_property_path(self, index, section, property_name):
        """Update the property path for a transform and auto-set 'n' parameter"""
        if 0 <= index < len(self.transforms):
            new_path = build_property_path(section, property_name)
            old_path = self.transforms[index]['property_path']
            self.transforms[index]['property_path'] = new_path
            
            # Auto-set 'n' parameter based on new property dimension
            should_auto_set, dimension = should_auto_set_n_parameter(new_path)
            if should_auto_set and dimension is not None:
                self.transforms[index]['params']['n'] = dimension
                print(f"Updated transform {index + 1} property path to: {new_path} (n={dimension})")
            else:
                # Scalar property - remove 'n' if it exists
                if 'n' in self.transforms[index]['params']:
                    del self.transforms[index]['params']['n']
                print(f"Updated transform {index + 1} property path to: {new_path} (scalar)")
            
            # Check if dimension changed - if so, regenerate display
            old_dimension = get_property_dimension(old_path)
            new_dimension = get_property_dimension(new_path)
            if old_dimension != new_dimension:
                # Dimension changed - need to regenerate parameter inputs
                print(f"  Dimension changed: {old_dimension} → {new_dimension}, regenerating display...")
                self.update_display()
    
    def _on_sampler_changed(self, index, display_value):
        """Handle sampler selection change"""
        # Convert display value back to sampler name
        samplers = get_available_samplers()
        sampler_name = None
        for samp_name, samp_display in samplers:
            if samp_display == display_value:
                sampler_name = samp_name
                break
        
        if sampler_name and 0 <= index < len(self.transforms):
            self.transforms[index]['sampler_name'] = sampler_name
            print(f"Updated transform {index + 1} sampler to: {sampler_name}")
            # Clear params when sampler changes (new sampler has different parameters)
            self.transforms[index]['params'] = {}
            # Regenerate the display to show new parameter inputs
            self.update_display()
    
    def _handle_drop(self, drop_target_index, app_data):
        """Handle dropping a transform onto another card"""
        # app_data contains the drag_data (source index)
        if isinstance(app_data, int) and app_data != drop_target_index:
            self.move_transform(app_data, drop_target_index)

