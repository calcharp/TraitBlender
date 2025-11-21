# Installation Guide

??? note "System Requirements"
    ### Minimum Requirements
    - **Blender**: Version 4.3.0 or higher
    - **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
    - **RAM**: 8GB minimum, 16GB recommended
    - **Storage**: 2GB free space for the add-on and dependencies

    ### Recommended Requirements
    - **Blender**: Latest stable version (4.3+)
    - **RAM**: 32GB for large datasets
    - **CPU**: Multi-core processor (8+ cores recommended)

??? note "Installation"
    <!-- TODO: Add command-line installation instructions for advanced users -->

    **Step 1: Download TraitBlender**

    - Download the latest release from [GitHub Releases](https://github.com/Imageomics/TraitBlender/releases)
    - Save the `.zip` file to your computer

    **Step 2: Install in Blender**

    - Open Blender
    - Go to `Edit > Preferences` (or `Blender > Preferences` on macOS)
    - Navigate to the `Add-ons` tab
    - Click `Install...` button
    - Browse and select the downloaded TraitBlender `.zip` file
    - Click `Install Add-on`

    **Step 3: Enable the Add-on**

    - In the Add-ons list, search for "TraitBlender"
    - Check the box next to "TraitBlender" to enable it
    - The add-on should now appear in the 3D Viewport sidebar (press `N` to show/hide)

    ### Dependency Installation

    TraitBlender automatically includes all required Python dependencies as wheel files. These include:

    - **pandas** - Dataset management and CSV/Excel handling
    - **numpy** - Numerical computing and mathematical operations
    - **scipy** - Statistical functions for transforms
    - **PyYAML** - Configuration file parsing
    - **Pillow** - Image processing
    - **dearpygui** - CSV viewer interface
    - **openpyxl** - Excel file support

    All dependencies are bundled as wheel files in the `wheels/` directory. No additional manual dependency installation is required.

??? note "Verify Installation"
    ### How to Verify Installation

    To verify that TraitBlender is properly installed:

    **Check the UI Panel**

    - In the 3D Viewport, press `N` to open the sidebar
    - Look for the "TraitBlender" tab

    **Test Basic Functionality**

    - Create a simple object (cube or sphere)
    - Open the TraitBlender panel
    - Try basic operations to ensure everything works

??? note "Troubleshooting Installation"
    ### Common Issues

    **Add-on doesn't appear after installation:**

    - Ensure you're using Blender 4.3.0 or higher
    - Check that the add-on is enabled in Preferences
    - Restart Blender completely

    **Import errors or missing dependencies:**

    - Re-download the add-on to ensure all wheel files are included
    - Check Blender's console for specific error messages

    **Performance issues:**

    - Check available system memory
    - Close unnecessary applications to free up resources

    For additional help, see the [Troubleshooting section](../troubleshooting/common-issues.md) or report issues on our [GitHub repository](https://github.com/Imageomics/TraitBlender/issues).

## Next Steps

After successful installation, proceed to the [Quick Start Tutorial](./quick-start.md) to begin using TraitBlender. 