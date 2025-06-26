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
        """Invoke file browser if no filepath is provided"""
        if not self.filepath:
            context.window_manager.fileselect_add(self)
            return {'RUNNING_MODAL'}
        else:
            return self.execute(context)

