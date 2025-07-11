import bpy
from bpy.types import Operator
import importlib
import sys
import os
import inspect
from ...core.helpers import get_asset_path
import traceback

class TRAITBLENDER_OT_generate_morphospace_sample(Operator):
    """Generate a morphospace sample using the selected morphospace and dataset row"""
    
    bl_idname = "traitblender.generate_morphospace_sample"
    bl_label = "Generate Morphospace Sample"
    bl_description = "Generate a morphospace sample using selected morphospace and dataset row"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        setup = context.scene.traitblender_setup
        dataset = context.scene.traitblender_dataset
        
        if not setup.available_morphospaces:
            self.report({'ERROR'}, "No morphospace selected")
            return {'CANCELLED'}
        if not dataset.sample:
            self.report({'ERROR'}, "No dataset sample selected")
            return {'CANCELLED'}
        try:
            morphospace_name = setup.available_morphospaces
            morphospace_modules_path = get_asset_path("morphospace_modules")
            morphospace_path = os.path.join(morphospace_modules_path, morphospace_name)
            if not os.path.exists(morphospace_path):
                self.report({'ERROR'}, f"Morphospace module not found: {morphospace_path}")
                return {'CANCELLED'}
            
            # Create a proper module spec that handles the package structure
            spec = importlib.util.spec_from_file_location(
                morphospace_name, 
                os.path.join(morphospace_path, "__init__.py"),
                submodule_search_locations=[morphospace_path]
            )
            if spec is None or spec.loader is None:
                self.report({'ERROR'}, f"Failed to create module spec for {morphospace_name}")
                return {'CANCELLED'}
            
            try:
                morphospace_module = importlib.util.module_from_spec(spec)
                sys.modules[morphospace_name] = morphospace_module
                spec.loader.exec_module(morphospace_module)
                sample_func = getattr(morphospace_module, 'sample')
            except (ImportError, AttributeError) as e:
                traceback.print_exc()
                self.report({'ERROR'}, f"Failed to import morphospace module: {e}")
                return {'CANCELLED'}
            
            selected_sample_name = dataset.sample
            row_data = dataset.loc(selected_sample_name)
            # Get the argument names for the sample function (excluding 'name')
            sig = inspect.signature(sample_func)
            valid_params = set(sig.parameters.keys()) - {'name'}
            params = {}
            for column_name, value in row_data.items():
                param_name = column_name.lower().replace(' ', '_')
                if param_name in valid_params:
                    params[param_name] = value
            # Debug: show what will be passed
            print(f"Calling {morphospace_name}.sample with name={selected_sample_name} and params={params}")
            try:
                sample_obj = sample_func(name=selected_sample_name, **params)
                sample_obj.to_blender(length=0.015, smooth=True)
                
                # Get the generated object
                generated_obj = bpy.data.objects.get(selected_sample_name)
                if generated_obj:
                    # Check if both Table and Mat objects exist
                    table_obj = bpy.data.objects.get("Table")
                    mat_obj = bpy.data.objects.get("Mat")
                    
                    if table_obj and mat_obj and hasattr(mat_obj, 'table_coords'):
                        # Parent the generated object to the table
                        generated_obj.parent = table_obj
                        generated_obj.matrix_parent_inverse = table_obj.matrix_world.inverted()
                        
                        # Set the generated object's table coordinates to match the Mat
                        generated_obj.table_coords = mat_obj.table_coords
                        print(f"Positioned {selected_sample_name} at table coordinates: {mat_obj.table_coords}")
                    else:
                        # Fallback: position at world origin
                        generated_obj.location = (0.0, 0.0, 0.0)
                        print(f"Positioned {selected_sample_name} at world origin (0, 0, 0)")
                        
                        # Warn user if museum scene objects are missing
                        if not table_obj or not mat_obj:
                            missing_objects = []
                            if not table_obj:
                                missing_objects.append("Table")
                            if not mat_obj:
                                missing_objects.append("Mat")
                            
                            warning_msg = f"Missing museum scene objects: {', '.join(missing_objects)}. "
                            warning_msg += "Run 'Import Museum' in the TraitBlender -> Museum Setup panel to set up the scene properly."
                            self.report({'WARNING'}, warning_msg)
                            print(f"Warning: {warning_msg}")
                else:
                    print(f"Warning: Generated object {selected_sample_name} not found")
                
                self.report({'INFO'}, f"Generated morphospace sample: {selected_sample_name}")
            except Exception as e:
                traceback.print_exc()
                self.report({'ERROR'}, f"Failed to generate morphospace sample: {str(e)}")
                return {'CANCELLED'}
        except Exception as e:
            traceback.print_exc()
            self.report({'ERROR'}, f"Failed to generate morphospace sample: {str(e)}")
            return {'CANCELLED'}
        return {'FINISHED'} 