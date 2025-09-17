import bpy
from bpy.types import Panel

class TRAITBLENDER_PT_main_panel(Panel):
    bl_label = "1 Museum Setup"
    bl_idname = "TRAITBLENDER_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TraitBlender'

    def draw(self, context):
        layout = self.layout
        # Setup Museum Scene and Clear Scene buttons
        row = layout.row(align=True)
        row.operator("traitblender.setup_scene", text="Import Museum")
        row.operator("traitblender.clear_scene", text="Clear Scene", icon='TRASH')
        layout.separator()
        # Config file path row
        row = layout.row(align=True)
        row.prop(context.scene.traitblender_setup, "config_file", text="Config File")
        # Configure Scene button row
        row = layout.row(align=True)
        row.operator("traitblender.configure_scene", text="Configure Scene")

    # Helper methods for config panel
    def _draw_config_section(self, layout, section_name, section_obj):
        box = layout.box()
        row = box.row()
        has_show_prop = hasattr(section_obj, 'show')
        if has_show_prop:
            row.prop(section_obj, 'show', text="", icon='DISCLOSURE_TRI_DOWN' if section_obj.show else 'DISCLOSURE_TRI_RIGHT')
            row.label(text=section_name.replace('_', ' ').title())
            if section_obj.show:
                self._draw_section_content(box, section_obj)
        else:
            row.label(text=section_name.replace('_', ' ').title())
            self._draw_section_content(box, section_obj)

    def _draw_section_content(self, layout, section_obj):
        for prop_name in section_obj.__class__.__annotations__.keys():
            if prop_name == "show":
                continue
            try:
                prop_value = getattr(section_obj, prop_name)
                if isinstance(prop_value, type(section_obj)):
                    sub_box = layout.box()
                    sub_box.label(text=prop_name.replace('_', ' ').title())
                    self._draw_config_section(sub_box, prop_name, prop_value)
                else:
                    layout.prop(section_obj, prop_name)
            except Exception as e:
                prop_row = layout.row()
                prop_row.label(text=f"{prop_name.replace('_', ' ').title()}: # Error - {str(e)}")

class TRAITBLENDER_PT_config_panel(Panel):
    bl_label = "2 Configuration"
    bl_idname = "TRAITBLENDER_PT_config_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TraitBlender'

    def draw(self, context):
        layout = self.layout
        config = context.scene.traitblender_config
        config_sections = config.get_config_sections()
        if config_sections:
            for section_name, section_obj in config_sections.items():
                if section_name in ["transforms", "sample", "orientations"]:
                    continue
                self._draw_config_section(layout, section_name, section_obj)
        else:
            layout.label(text="No configuration sections found", icon='INFO')
        layout.separator()
        row = layout.row(align=True)
        row.operator("traitblender.show_configuration", text="Show Configuration")
        row.operator("traitblender.export_config", text="Export Config as YAML")

    def _draw_config_section(self, layout, section_name, section_obj):
        TRAITBLENDER_PT_main_panel._draw_config_section(self, layout, section_name, section_obj)

    def _draw_section_content(self, layout, section_obj):
        TRAITBLENDER_PT_main_panel._draw_section_content(self, layout, section_obj)

class TRAITBLENDER_PT_morphospaces_panel(Panel):
    bl_label = "3 Morphospaces"
    bl_idname = "TRAITBLENDER_PT_morphospaces_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TraitBlender'

    def draw(self, context):
        layout = self.layout
        setup = context.scene.traitblender_setup
        
        # Morphospace selection dropdown
        row = layout.row(align=True)
        row.prop(setup, "available_morphospaces", text="Morphospace")

class TRAITBLENDER_PT_datasets_panel(Panel):
    bl_label = "4 Datasets"
    bl_idname = "TRAITBLENDER_PT_datasets_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TraitBlender'

    def draw(self, context):
        layout = self.layout
        dataset = context.scene.traitblender_dataset
        setup = context.scene.traitblender_setup
        
        # Dataset file path row
        row = layout.row(align=True)
        row.prop(dataset, "filepath", text="Dataset File")
        
        # Edit dataset button
        row = layout.row(align=True)
        row.operator("traitblender.edit_dataset", text="Edit Dataset")
        
        # Sample selection dropdown
        row = layout.row(align=True)
        row.prop(dataset, "sample", text="Sample")
        
        # Generate sample button
        row = layout.row(align=True)
        row.operator("traitblender.generate_morphospace_sample", text="Generate Sample", icon='ADD')
        
        # Sample controls (only show if a sample is selected and exists)
        if dataset.sample and dataset.sample in bpy.data.objects:
            layout.separator()
            box = layout.box()
            box.label(text="Sample Controls", icon='OBJECT_DATA')

            sample_config = context.scene.traitblender_config.sample
            sample_obj = bpy.data.objects[dataset.sample]
            # Use table coordinates location and rotation
            box.prop(sample_obj, "tb_coords", text="Location")
            box.prop(sample_obj, "tb_rotation", text="Rotation")

class TRAITBLENDER_PT_orientations_panel(Panel):
    bl_label = "5 Orientations"
    bl_idname = "TRAITBLENDER_PT_orientations_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TraitBlender'

    def draw(self, context):
        layout = self.layout
        config = context.scene.traitblender_config
        
        # Object Location Origin dropdown
        row = layout.row(align=True)
        row.prop(config.orientations, "object_location_origin", text="Object Location Origin")
        
        # Object Rotation Origin dropdown
        row = layout.row(align=True)
        row.prop(config.orientations, "object_rotation_origin", text="Object Rotation Origin")
        
        # Location Shift Axes dropdown
        row = layout.row(align=True)
        row.prop(config.orientations, "location_shift_axes", text="Location Shift Axes")
        
        # Shift Sample Origin button
        row = layout.row(align=True)
        row.operator("traitblender.sample_origin_shift", text="Shift Sample Origin", icon='ARROW_LEFTRIGHT')

class TRAITBLENDER_PT_transforms_panel(Panel):
    bl_label = "6 Transforms"
    bl_idname = "TRAITBLENDER_PT_transforms_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TraitBlender'

    def draw(self, context):
        layout = self.layout
        config = context.scene.traitblender_config
        layout.separator()
        box = layout.box()
        transforms_config = config.transforms

        # Property selection row: [Property:][Section][Property]
        row = box.row(align=True)
        row.label(text="Property:")
        row.prop(transforms_config, "selected_section", text="", emboss=True)
        row.prop(transforms_config, "selected_property", text="", emboss=True)

        # Sampler selection row: [Sampler:][Sampler Dropdown]
        row = box.row(align=True)
        row.label(text="Sampler:")
        row.prop(transforms_config, "selected_sampler", text="", emboss=True)

        # Pipeline control buttons
        row = box.row(align=True)
        row.operator("traitblender.run_pipeline", text="Run Pipeline", icon='PLAY')
        row.operator("traitblender.undo_pipeline", text="Undo Pipeline", icon='LOOP_BACK')

        # Transform count
        row = box.row(align=True)
        row.label(text=f"Transforms in pipeline: {len(transforms_config)}")

class TRAITBLENDER_PT_imaging_panel(Panel):
    bl_label = "7 Imaging"
    bl_idname = "TRAITBLENDER_PT_imaging_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TraitBlender'

    def draw(self, context):
        layout = self.layout
        # Imaging pipeline button
        row = layout.row(align=True)
        row.operator("traitblender.imaging_pipeline", text="Run Imaging Pipeline", icon='PLAY') 