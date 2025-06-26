"""
TraitBlender - Blender Add-on for Generating Museum-Style Morphological Images

Main add-on initialization file.
"""
import os
import bpy


def _init_dir():
    """Initialize any necessary directories (simplified - no asset copying)"""
    # Create user data directory for configs, outputs, etc. (not assets)
    base_path = bpy.utils.extension_path_user(__package__, create=True)
    
    # Create subdirectories for user data (not assets)
    user_dirs = ['configs', 'outputs', 'cache']
    for dir_name in user_dirs:
        dir_path = os.path.join(base_path, dir_name)
        os.makedirs(dir_path, exist_ok=True)
    
    print(f"Initialized user directories at {base_path}")


def register():
    """Register all add-on classes"""

    from .core import configs
    print(f"configs: {configs}")
    from .core import configure_traitblender
    configure_traitblender()

    # Register UI components
    from .ui import register
    register()

    # Initialize user directories (no asset copying)
    _init_dir()

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
    # Unregister UI components
    from .ui import unregister
    unregister()
    
        
if __name__ == "__main__":
    import traceback
    try:
        register()
    except Exception:
        traceback.print_exc()