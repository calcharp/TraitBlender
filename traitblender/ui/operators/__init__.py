"""
TraitBlender UI Operators

Contains all operator classes for the TraitBlender add-on.
Operators handle user actions and commands.
"""

import bpy

from . import (
    setup_scene_operator,
    clear_scene_operator,
    configure_traitblender,
    import_dataset_operator,
    edit_dataset_operator,
    transforms_operators,
    generate_morphospace_sample_operator,
)

classes = [
    setup_scene_operator.TRAITBLENDER_OT_setup_scene,
    clear_scene_operator.TRAITBLENDER_OT_clear_scene,
    configure_traitblender.TRAITBLENDER_OT_configure_scene,
    configure_traitblender.TRAITBLENDER_OT_show_configuration,
    configure_traitblender.TRAITBLENDER_OT_export_config,
    import_dataset_operator.TRAITBLENDER_OT_import_dataset,
    edit_dataset_operator.TRAITBLENDER_OT_edit_dataset,
    transforms_operators.TRAITBLENDER_OT_run_pipeline,
    transforms_operators.TRAITBLENDER_OT_undo_pipeline,
    generate_morphospace_sample_operator.TRAITBLENDER_OT_generate_morphospace_sample,
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