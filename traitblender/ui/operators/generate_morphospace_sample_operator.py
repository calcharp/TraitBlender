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
                sample_obj.to_blender()

                # Ensure the object is properly created and positioned
                bpy.context.view_layer.update()
                
                # Get the generated object
                generated_obj = bpy.data.objects.get(selected_sample_name)
                if generated_obj is None:
                    self.report({'ERROR'}, f"Failed to find generated object: {selected_sample_name}")
                    return {'CANCELLED'}
                
                # Always set the object to a known good position first
                generated_obj.location = (0.0, 0.0, 0.0)
                
                try:
                    if bpy.data.objects.get("Table"):
                        # Set table coordinates - this will work now since we have a valid location
                        generated_obj.table_coords = (0.0, 0.0, 0.0)
                        print(f"Set table coordinates for {selected_sample_name} to {generated_obj.table_coords}")
                    else:
                        # No table, but we already set the location to (0,0,0)
                        print(f"Set location for {selected_sample_name} to {generated_obj.location}")
                except Exception as e:
                    print(f"Warning: Failed to set table coordinates for {selected_sample_name}: {e}")
                    # Location is already set to (0,0,0), so we're good
                
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