# Quick Start Guide (GUI)

Get up and running with TraitBlender's graphical interface in just a few minutes! This guide will walk you through creating your first museum-style specimen image using Blender's user interface.

!!! note "Alternative Access Methods"
    This guide covers the GUI interface. TraitBlender operators can also be accessed programmatically via Python API. See the [Quick Start (API)](./quick-start-api.md) guide for code-based workflows.

## Prerequisites

Before starting, ensure you have:

- ✅ Blender 4.3.0+ installed
- ✅ TraitBlender add-on installed ([Installation Guide](./installation.md))

## Step 1: Enable TraitBlender

1. Open Blender
2. Go to **Edit → Preferences → Add-ons**
3. Search for "TraitBlender" 
4. Enable the checkbox next to **TraitBlender**
5. The TraitBlender panel should now appear in the **3D Viewport sidebar** (press `N` if hidden)

## Step 2: Load Your Specimen

1. In the TraitBlender panel, click **Load Specimen**
2. Browse and select your 3D model file
3. Your specimen will appear in the scene with automatic scaling and centering

## Step 3: Choose a Scene Preset

TraitBlender includes several museum-style presets:

- **Museum Standard**: Clean white background with professional lighting
- **Scientific**: Grid background with measurement references  
- **Artistic**: Dramatic lighting with subtle shadows
- **Comparative**: Multi-specimen layout for comparisons

1. In the **Scene Assets** section, select a preset from the dropdown
2. Click **Apply Scene** to load the lighting and background

## Step 4: Configure Basic Settings

### Camera Settings
- **View**: Choose from dorsal, ventral, lateral, or frontal views
- **Zoom**: Adjust to frame your specimen appropriately

### Lighting
- **Intensity**: Control overall brightness (default: 80%)
- **Temperature**: Adjust color temperature (5500K for daylight)

### Background
- **Color**: Pure white (#FFFFFF) for museum standard
- **Transparency**: Enable for images with transparent backgrounds

## Step 5: Render Your Image

1. Click **Generate Image** in the TraitBlender panel
2. Choose your desired resolution:
   - **Standard**: 1920×1080 (good for web)
   - **High**: 4096×4096 (print quality)
   - **Custom**: Set specific dimensions
3. Click **Render** and wait for processing
4. Your image will be saved to the designated output folder

## Step 6: Review and Export

1. The rendered image opens automatically in Blender's Image Editor
2. Review the image quality and composition
3. **Save** to export in your preferred format (PNG, JPEG, TIFF)
4. Add metadata tags for specimen information

## Next Steps

Ready to explore programmatic workflows? Check out the **[Quick Start (API)](./quick-start-api.md)** guide to learn how to use TraitBlender operators directly from Python scripts.

### Explore More:
- **[Basic Imaging Tutorial](../tutorials/basic-imaging.md)**: Learn advanced techniques
- **[Configuration Guide](../configuration/config-files.md)**: Customize default settings
- **[CLI Usage](../cli/usage.md)**: Automate batch processing

### Tips for Better Results:
- Use high-quality 3D models for best output
- Experiment with different lighting presets
- Consider your intended use (web, print, publication) when choosing resolution
- Save scene configurations for consistent results across specimens

## Troubleshooting

Having issues? Check our [troubleshooting guide](../troubleshooting/common-issues.md) for solutions to common problems.

---

**Estimated time**: 5-10 minutes for your first image  
**Skill level**: Beginner  
**Output**: High-quality museum-style specimen image 