import bpy
import yaml
import os
from bpy.types import Operator
from bpy.props import StringProperty


class TRAITBLENDER_OT_configure_scene(Operator):
    """Configure TraitBlender scene from YAML file"""
    
    bl_idname = "traitblender.configure_scene"
    bl_label = "Configure Scene"
    bl_description = "Load and apply configuration from YAML file"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: StringProperty(
        name="Config File Path",
        description="Path to the YAML configuration file (optional - uses default if not provided)",
        default="",
        subtype='FILE_PATH'
    )
    
    def execute(self, context):
        """Execute the configure scene operation"""
        
        # Use provided filepath or default to the stored config file path
        config_file_path = self.filepath if self.filepath else context.scene.traitblender_setup.config_file
        
        if not config_file_path:
            self.report({'ERROR'}, "No configuration file specified")
            return {'CANCELLED'}
        
        if not os.path.exists(config_file_path):
            self.report({'ERROR'}, f"Configuration file not found: {config_file_path}")
            return {'CANCELLED'}
        
        try:
            # Read the YAML file
            with open(config_file_path, 'r') as file:
                config_data = yaml.safe_load(file)
            
            if not config_data:
                self.report({'ERROR'}, "Configuration file is empty or invalid")
                return {'CANCELLED'}
            
            # Apply the configuration using the from_dict method
            context.scene.traitblender_config.from_dict(config_data)
            
            self.report({'INFO'}, f"Configuration loaded successfully from {config_file_path}")
            return {'FINISHED'}
            
        except yaml.YAMLError as e:
            self.report({'ERROR'}, f"Invalid YAML format: {e}")
            return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error loading configuration: {e}")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        """Invoke file browser if no filepath is provided and no stored config file"""
        # If no filepath provided and no stored config file, open file browser
        if not self.filepath and not context.scene.traitblender_setup.config_file:
            context.window_manager.fileselect_add(self)
            return {'RUNNING_MODAL'}
        else:
            return self.execute(context)


class TRAITBLENDER_OT_show_configuration(Operator):
    """Show current TraitBlender configuration in YAML format"""
    
    bl_idname = "traitblender.show_configuration"
    bl_label = "Show Configuration"
    bl_description = "Display current configuration in YAML format"
    bl_options = {'REGISTER', 'UNDO'}
    
    _old_mouse_pos = None

    def execute(self, context):
        return {'FINISHED'}
    
    def invoke(self, context, event):
        window = context.window_manager.windows[0]
        self._old_mouse_pos = (event.mouse_x, event.mouse_y)
        center_x = window.width // 2
        center_y = window.height // 2
        window.cursor_warp(center_x, center_y)
        # Restore mouse after popup appears
        def restore_mouse():
            window.cursor_warp(*self._old_mouse_pos)
            self._old_mouse_pos = None
            return None  # Only run once
        bpy.app.timers.register(restore_mouse, first_interval=0.01)
        return context.window_manager.invoke_props_dialog(self, width=600)
    
    def draw(self, context):
        layout = self.layout
        config_yaml = str(context.scene.traitblender_config)
        for line in config_yaml.splitlines():
            layout.label(text=line)


class TRAITBLENDER_OT_export_config(Operator):
    """Export current TraitBlender configuration to a YAML file"""
    
    bl_idname = "traitblender.export_config"
    bl_label = "Export Config as YAML"
    bl_description = "Export the current configuration to a YAML file"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: StringProperty(
        name="File Path",
        description="Path to export YAML file",
        default="",
        subtype='FILE_PATH',
    )
    
    def execute(self, context):
        config_yaml = str(context.scene.traitblender_config)
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                f.write(config_yaml)
            self.report({'INFO'}, f"Configuration exported to {self.filepath}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export configuration: {e}")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

