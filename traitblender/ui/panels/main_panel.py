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
        
        # Setup Museum Scene and Clear Scene buttons
        row = layout.row(align=True)
        row.operator("traitblender.setup_scene", text="Import Museum")
        row.operator("traitblender.clear_scene", text="Clear Scene", icon='TRASH')
        
        # Configuration section
        layout.separator()
        
        # Config file path row
        row = layout.row(align=True)
        row.prop(context.scene.traitblender_setup, "config_file", text="Config File")

        # Configure Scene button row (keep here)
        row = layout.row(align=True)
        row.operator("traitblender.configure_scene", text="Configure Scene")

        # Display all config sections
        layout.separator()
        layout.label(text="Configuration:")
        
        config_sections = config.get_config_sections()
        if config_sections:
            for section_name, section_obj in config_sections.items():
                self._draw_config_section(layout, section_name, section_obj)
        else:
            layout.label(text="No configuration sections found", icon='INFO')

        # Show Configuration and Export Config as YAML buttons at the bottom
        layout.separator()
        row = layout.row(align=True)
        row.operator("traitblender.show_configuration", text="Show Configuration")
        row.operator("traitblender.export_config", text="Export Config as YAML")

    def _draw_config_section(self, layout, section_name, section_obj):
        box = layout.box()
        row = box.row()
        
        # Check if this section has a show property
        has_show_prop = hasattr(section_obj, 'show')
        
        if has_show_prop:
            # Create dropdown with toggle
            row.prop(section_obj, 'show', text="", icon='DISCLOSURE_TRI_DOWN' if section_obj.show else 'DISCLOSURE_TRI_RIGHT')
            row.label(text=section_name.replace('_', ' ').title())
            
            # Only show content if expanded
            if section_obj.show:
                self._draw_section_content(box, section_obj)
        else:
            # No show property - show always
            row.label(text=section_name.replace('_', ' ').title())
            self._draw_section_content(box, section_obj)
    
    def _draw_section_content(self, layout, section_obj):
        """Draw the content of a configuration section"""
        for prop_name in section_obj.__class__.__annotations__.keys():
            if prop_name == "show":
                continue  # Skip the show property
            try:
                prop_value = getattr(section_obj, prop_name)
                if isinstance(prop_value, type(section_obj)):
                    # Nested section - recurse
                    sub_box = layout.box()
                    sub_box.label(text=prop_name.replace('_', ' ').title())
                    self._draw_config_section(sub_box, prop_name, prop_value)
                else:
                    # Regular property - show as UI control
                    layout.prop(section_obj, prop_name)
            except Exception as e:
                prop_row = layout.row()
                prop_row.label(text=f"{prop_name.replace('_', ' ').title()}: # Error - {str(e)}") 