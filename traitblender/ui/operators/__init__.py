"""
TraitBlender UI Operators

Contains all operator classes for the TraitBlender add-on.
Operators handle user actions and commands.
"""

import bpy

from . import (
    setup_scene_op,
    clear_scene_op,
    config_ops,
    import_dataset_op,
    edit_dataset_op,
    transforms_ops,
    edit_transforms_op,
    generate_morphospace_sample_op,
    imaging_pipeline_op,
    apply_orientation_op,
    render_image_op,
)

classes = [
    setup_scene_op.TRAITBLENDER_OT_setup_scene,
    clear_scene_op.TRAITBLENDER_OT_clear_scene,
    config_ops.TRAITBLENDER_OT_configure_scene,
    config_ops.TRAITBLENDER_OT_show_configuration,
    config_ops.TRAITBLENDER_OT_export_config,
    import_dataset_op.TRAITBLENDER_OT_import_dataset,
    edit_dataset_op.TRAITBLENDER_OT_edit_dataset,
    transforms_ops.TRAITBLENDER_OT_run_pipeline,
    transforms_ops.TRAITBLENDER_OT_undo_pipeline,
    transforms_ops.TRAITBLENDER_OT_reset_pipeline,
    edit_transforms_op.TRAITBLENDER_OT_edit_transforms,
    generate_morphospace_sample_op.TRAITBLENDER_OT_generate_morphospace_sample,
    imaging_pipeline_op.TRAITBLENDER_OT_imaging_pipeline,
    apply_orientation_op.TRAITBLENDER_OT_apply_orientation,
    render_image_op.TRAITBLENDER_OT_render_image,
]


def register():
    r_classes = classes
    for cls in r_classes:
        bpy.utils.register_class(cls)


def unregister():
    r_classes = classes
    for cls in r_classes:
        bpy.utils.unregister_class(cls)

__all__ = ["register", "unregister"] 