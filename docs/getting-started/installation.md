# Installation Guide

## System Requirements

### Minimum Requirements
- **Blender**: Version 4.3.0 or higher
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **RAM**: 8GB minimum, 16GB recommended
- **GPU**: CUDA-compatible NVIDIA GPU recommended for faster rendering
- **Storage**: 2GB free space for the add-on and dependencies

### Recommended Requirements
- **Blender**: Latest stable version (4.3+)
- **RAM**: 32GB for large datasets
- **GPU**: RTX 3060 or higher with 8GB+ VRAM
- **CPU**: Multi-core processor (8+ cores recommended)

## Installation Methods

### Method 1: Install from Blender Add-ons Panel (Recommended)

1. **Download TraitBlender**
   - Download the latest release from [GitHub Releases](https://github.com/Imageomics/TraitBlender/releases)
   - Save the `.zip` file to your computer

2. **Install in Blender**
   - Open Blender
   - Go to `Edit > Preferences` (or `Blender > Preferences` on macOS)
   - Navigate to the `Add-ons` tab
   - Click `Install...` button
   - Browse and select the downloaded TraitBlender `.zip` file
   - Click `Install Add-on`

3. **Enable the Add-on**
   - In the Add-ons list, search for "TraitBlender"
   - Check the box next to "TraitBlender" to enable it
   - The add-on should now appear in the 3D Viewport sidebar (press `N` to show/hide)

### Method 2: Manual Installation

1. **Extract the Add-on**
   - Extract the TraitBlender `.zip` file
   - Locate your Blender add-ons directory:
     - **Windows**: `%APPDATA%\Blender Foundation\Blender\4.x\scripts\addons\`
     - **macOS**: `~/Library/Application Support/Blender/4.x/scripts/addons/`
     - **Linux**: `~/.config/blender/4.x/scripts/addons/`

2. **Copy Files**
   - Copy the extracted `traitblender` folder to the add-ons directory
   - Restart Blender

3. **Enable the Add-on**
   - Follow step 3 from Method 1 above

## Dependency Installation

### Included Dependencies
TraitBlender automatically includes all required Python dependencies as wheel files. These include:

- pandas (data manipulation)
- numpy (numerical computing)
- Additional supporting libraries

No additional manual dependency installation is required.

## Verification

### How to Verify Installation

To verify that TraitBlender is properly installed:

1. **Check the UI Panel**
   - In the 3D Viewport, press `N` to open the sidebar
   - Look for the "TraitBlender" tab

2. **Test Basic Functionality**
   - Create a simple object (cube or sphere)
   - Open the TraitBlender panel
   - Try basic operations to ensure everything works

## Troubleshooting Installation

### Common Issues

**Add-on doesn't appear after installation:**

- Ensure you're using Blender 4.3.0 or higher
- Check that the add-on is enabled in Preferences
- Restart Blender completely

**Import errors or missing dependencies:**

- Re-download the add-on to ensure all wheel files are included
- Check Blender's console for specific error messages

**Performance issues:**

- Ensure your GPU drivers are up to date
- Enable GPU acceleration in Blender preferences
- Check available system memory

For additional help, see the [Troubleshooting section](../troubleshooting/common-issues.md) or report issues on our [GitHub repository](https://github.com/Imageomics/TraitBlender/issues).

## Next Steps

After successful installation, proceed to the [Quick Start Tutorial](./quick-start.md) to begin using TraitBlender. 