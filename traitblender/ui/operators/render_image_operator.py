import bpy
from bpy.types import Operator

class TRAITBLENDER_OT_render_image(Operator):
    bl_idname = "traitblender.render_image"
    bl_label = "Render Image"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if 'Camera' not in bpy.data.objects:
            return {'CANCELLED'}
        
        camera = bpy.data.objects['Camera']
        context.scene.camera = camera
        bpy.ops.render.render(write_still=True)
        
        return {'FINISHED'}

