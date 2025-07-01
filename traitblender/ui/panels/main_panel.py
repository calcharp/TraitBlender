import bpy
from bpy.types import Panel


class TRAITBLENDER_PT_main_panel(Panel):
    bl_label = "TraitBlender"
    bl_idname = "TRAITBLENDER_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TraitBlender'

    def draw(self, context):
        layout = self.layout
        config = context.scene.traitblender_config
        
        # Setup Museum Scene button
        row = layout.row(align=True)
        row.operator("traitblender.setup_scene", text="Setup Museum Scene")
        
        # Configuration section
        layout.separator()
        
        # Config file path row
        row = layout.row(align=True)
        row.prop(context.scene.traitblender_setup, "config_file", text="Config File")
        
        # Configure and Show Configuration buttons row
        row = layout.row(align=True)
        row.operator("traitblender.configure_scene", text="Configure Scene")
        row.operator("traitblender.show_configuration", text="Show Configuration")
        
        # Export Config button row
        row = layout.row(align=True)
        row.operator("traitblender.export_config", text="Export Config as YAML")
        
        # Display all config sections
        layout.separator()
        layout.label(text="Configuration:", icon='SETTINGS')
        
        config_sections = config.get_config_sections()
        if config_sections:
            for section_name, section_obj in config_sections.items():
                self._draw_config_section(layout, section_name, section_obj)
        else:
            layout.label(text="No configuration sections found", icon='INFO')
    
    def _draw_config_section(self, layout, section_name, section_obj):
        """Draw a configuration section with its properties."""
        # Create a box for this section
        box = layout.box()
        
        # Section header
        row = box.row()
        row.label(text=section_name.replace('_', ' ').title(), icon='SETTINGS')
        
        # Display section properties
        for prop_name in section_obj.__class__.__annotations__.keys():
            try:
                prop_value = getattr(section_obj, prop_name)
                
                # If it's another TraitBlenderConfig, create a sub-section
                if isinstance(prop_value, type(section_obj)):
                    sub_box = box.box()
                    sub_box.label(text=prop_name.replace('_', ' ').title())
                    self._draw_config_section(sub_box, prop_name, prop_value)
                else:
                    # For simple properties, show as an interactive property
                    box.prop(section_obj, prop_name)
            except Exception as e:
                # If there's an error accessing the property, show it as missing
                prop_row = box.row()
                prop_row.label(text=f"{prop_name.replace('_', ' ').title()}: # Error - {str(e)}") 