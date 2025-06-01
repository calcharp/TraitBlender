# Blender Optimization

Optimize your Blender setup for the best TraitBlender experience. These configuration changes will improve performance, enable useful features, and make your workflow smoother.

## Essential Settings

??? tip "Enable Python Tooltips"
    Python tooltips show you the exact Python commands for UI operations, which is helpful when transitioning between GUI and API workflows.

    **Steps:**
    1. Go to **Edit → Preferences** (or **Blender → Preferences** on macOS)
    2. Navigate to **Interface** tab
    3. Under **Display**, check **Python Tooltips**
    4. Click **Save Preferences**

    **Benefits:**
    - See Python commands when hovering over buttons
    - Learn the API while using the GUI
    - Easy transition from GUI to scripting workflows

??? tip "Allow Online Access"
    Enable web connections for add-on updates, asset downloads, and documentation access.

    **Steps:**
    1. Go to **Edit → Preferences → Network**
    2. Check **Allow Online Access**
    3. Optionally configure proxy settings if needed
    4. Click **Save Preferences**

    **Benefits:**
    - Automatic add-on updates
    - Access to online asset libraries
    - Direct documentation links work properly

## Performance Optimization

??? success "GPU Acceleration"
    Enable GPU rendering for significantly faster performance.

    **For NVIDIA GPUs:**
    1. Go to **Edit → Preferences → System**
    2. Under **Cycles Render Devices**, select **CUDA** or **OptiX**
    3. Check your GPU device(s)
    4. Click **Save Preferences**

    **For AMD GPUs:**
    1. Select **HIP** instead of CUDA
    2. Check your GPU device(s)

    **For Apple Silicon:**
    1. Select **Metal** 
    2. Enable GPU acceleration

??? success "Memory & Performance"
    Optimize memory usage for large datasets and models.

    **Memory Settings:**
    1. Go to **Edit → Preferences → System**
    2. **Undo Steps**: Reduce to 32 (default: 64) for large models
    3. **Memory Cache Limit**: Set to 50-75% of your RAM
    4. **Sequencer Cache Limit**: 1024MB for image processing

    **Viewport Performance:**
    1. **Edit → Preferences → Viewport**
    2. **Quality**: Set to "Medium" for better performance
    3. **Textures**: Enable "Limit Size" and set to 1024px for large datasets

## Development Features

??? info "Developer Extras"
    Enable advanced features useful for TraitBlender development and debugging.

    **Steps:**
    1. **Edit → Preferences → Interface**
    2. Under **Display**, check **Developer Extras**
    3. **Save Preferences**

    **New Features Available:**
    - Python console auto-complete
    - Operator search (F3) shows Python commands
    - Advanced debugging options
    - Additional UI panels for development

??? info "Console Logging"
    Enable detailed logging for troubleshooting TraitBlender issues.

    **Steps:**
    1. **Window → Toggle System Console** (Windows) or run Blender from terminal (Mac/Linux)
    2. **Edit → Preferences → System**
    3. Set **Console Logging Level** to **Info** or **Debug**
    4. Check **Log to File** to save logs

## Workspace Optimization

??? abstract "Custom Workspace for TraitBlender"
    Create a dedicated workspace optimized for specimen processing.

    **Setup:**
    1. Switch to **Scripting** workspace
    2. Add a **3D Viewport** for specimen preview
    3. Add **Properties** panel for material settings
    4. Add **Outliner** for scene management
    5. Save as new workspace: **+** → **Duplicate Current** → Rename to "TraitBlender"

    **Benefits:**
    - Optimized layout for specimen processing
    - Quick access to Python console and 3D preview
    - Consistent workflow environment

??? abstract "Hotkey Customization"
    Set up convenient hotkeys for common TraitBlender operations.

    **Recommended Hotkeys:**
    1. **Edit → Preferences → Keymap**
    2. **Add New** entries:
       - `Ctrl+Shift+T`: Toggle TraitBlender panel
       - `Ctrl+R`: Quick render specimen
       - `F12`: Full render with current settings

## File Management

??? note "Auto-Save Configuration"
    Configure automatic saving to prevent data loss during long processing sessions.

    **Settings:**
    1. **Edit → Preferences → Save & Load**
    2. **Auto Save**: Enable and set to 2-5 minutes
    3. **File Browser**: Show hidden files for better file management
    4. **Blend Files**: Save preview images for easy identification

??? note "Default Scene Setup"
    Create a default scene optimized for TraitBlender workflows.

    **Steps:**
    1. Delete default cube, light, and camera
    2. Add TraitBlender-specific scene elements
    3. Set render engine to Cycles
    4. Configure basic lighting setup
    5. **File → Defaults → Save Startup File**

## Troubleshooting Performance Issues

??? warning "Common Performance Problems"

    **Slow Viewport:**
    - Reduce subdivision levels on high-poly models
    - Use "Wireframe" or "Solid" shading modes during positioning
    - Enable "Fast Navigate" in viewport gizmos

    **Memory Issues:**
    - Close unnecessary applications
    - Reduce texture resolution in material properties
    - Use "Simplify" render settings for preview renders

    **Render Crashes:**
    - Reduce tile size for GPU rendering
    - Lower sample count for test renders
    - Check GPU memory usage in Task Manager/Activity Monitor

## Verification

After applying these optimizations, verify everything works:

1. **Test GPU Rendering**: Create a simple scene and render with Cycles
2. **Check Python Tooltips**: Hover over UI elements to see Python commands
3. **Test Online Access**: Try accessing online documentation links
4. **Performance Check**: Load a medium-complexity specimen model

---

**Estimated setup time**: 10-15 minutes  
**Performance improvement**: 2-5x faster rendering with proper GPU setup  
**Skill level**: Beginner to Intermediate

## Next Steps

With Blender optimized, proceed to:
- **[Quick Start (GUI)](./quick-start.md)**: Learn the TraitBlender interface
- **[Quick Start (API)](./quick-start-api.md)**: Explore programmatic workflows 