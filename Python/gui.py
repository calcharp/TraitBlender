import bpy
import json



class LoadObjectOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "traitblender.load_object_operator"
    bl_label = "Load Object"

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        try: 
            active_mesh = get_setting(bpy.context, "active_mesh")
            active_mesh_path = get_setting(bpy.context, "predefined_meshes")[active_mesh][0]
            bpy.ops.import_scene.obj(filepath=active_mesh_path)
        except Exception as e:
            print("Failed to import active object. Error:", e)
        return {'FINISHED'}

class ImportTraitBlenderSettings(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "traitblender.import_traitblender_settings"
    bl_label = "Import TraitBlender Settings"

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        # Load the active mesh from the JSON file
        try:
            with open("../data/settings/settings.json", "r") as f:
                data = json.load(f)
                context.scene.traitblender_settings = json.dumps(data)
        except Exception as e:
            print("Failed to load mesh from JSON file. Error:", e)
            context.view_layer.objects.active = context.object

        return {'FINISHED'}

def get_setting(context, key):
    settings_string = context.scene.traitblender_settings
    settings_dict = json.loads(settings_string)
    return settings_dict.get(key, None)

def register():
    bpy.utils.register_class(ImportTraitBlenderSettings)
    bpy.utils.register_class(LoadObjectOperator)
    
    bpy.types.Scene.traitblender_settings = bpy.props.StringProperty(
        name="Active Mesh Data",
        description="JSON data for the active mesh",
        default="",
    )

def unregister():
    bpy.utils.unregister_class(ImportTraitBlenderSettings)
    bpy.utils.register_class(LoadObjectOperator)
    del bpy.types.Scene.traitblender_settings

if __name__ == "__main__":
    register()
        # Load the object
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.ops.traitblender.import_traitblender_settings()
    bpy.ops.traitblender.load_object_operator()

