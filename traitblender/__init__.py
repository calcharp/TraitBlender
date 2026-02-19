"""
TraitBlender - Blender Add-on for Generating Museum-Style Morphological Images

Main add-on initialization file.
"""

def register():
    """Register all add-on classes"""
    import os
    import bpy
    from .core.helpers import init_user_dirs
    from .core import configs, config_register
    from .core.datasets import register as datasets_register
    from .ui import register as ui_register

    print(f"configs: {configs}")
    config_register()

    # Register datasets
    datasets_register()

    # Register UI components
    ui_register()

    # Initialize user directories and copy assets if needed
    init_user_dirs(copy_assets=True)

    # Note: Asset library registration is handled automatically by the extension system in Blender 4.3+
    # The assets directory will be accessible through the addon's package structure
    addon_dir = os.path.dirname(os.path.abspath(__file__))
    assets_path = os.path.join(addon_dir, "assets")
    
    if os.path.exists(assets_path):
        print(f"TraitBlender assets available at: {assets_path}")
    else:
        print("Warning: TraitBlender assets directory not found")


def unregister():
    """Unregister all add-on classes"""
    from .ui import unregister as ui_unregister
    from .core.datasets import unregister as datasets_unregister
    
    ui_unregister()
    datasets_unregister()
    
        
if __name__ == "__main__":
    import traceback
    try:
        register()
    except Exception:
        traceback.print_exc()