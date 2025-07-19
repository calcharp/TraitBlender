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

If you want TraitBlender to be activated by default when opening Blender, you must save your prefernces after activation, with Edit  ->  ☰  ->  Save Preferences.

## Step 2: Open the Museum Scene

1. In the TraitBlender panel, click the **Museum Setup** dropdown, and click **Import Museum**
2. After a second or two, the screen will get dark. Press 0 on your keyboard to switch to Camera View. You should now be looking through the camera at the empty mat lying on the table.
    If you do not have a standard numpad on your keyboard and rely on the number keys at the top, go to Edit -> Preferences -> Input, and check the box for **Emulate Numpad**. This will allow you to use the number keys at the top of your keyboard as a numpad, and you can then press 0 to switch to Camera View.

## Step 3: Alter the configuration of the scene and its layout

Collapse the **Museum Setup** dropdown, and press the dropdown arrow for the **Configuration Panel**.

Internally, Blender is storing the TraitBlender configuration data as a [PropertyGroup](https://docs.blender.org/api/current/bpy.types.PropertyGroup.html), at `bpy.context.scene.tb_config`. The **Configuration Panel** serves as a visual interface for this object.

In this panel, you will see a number of sections:

- **Camera**
- **Lamp**
- **Mat**
- **Metadata**
- **Output**
- **Render**
- **World**

These sections can be used for altering different aspects of the scene, such as the position and focal length of the camera, the color and size of the mat, metadata information to include with images for rendering, and more. Any updates you make here will be changed in the underlying configuration object. 

To see all of the configuration settings, press the **Show Configuration** button at the bottom of the panel. A popup with all of the configuration settings will appear.

You may also export your configuration settings to a YAML file with the **Export Config as YAML** button, and import external configurations in the Museum Setup dropdown, with the YAML path in the **Config File** field, and pressing **Configure Scene**. 

Note that this import will only work if the original **Import Museum** button has been pressed, and none of the default objects/materials/etc... have been deleted. If you run into import problems, you may emptying the scene with the **Clear Scene** button, and re-importing the museum scene.
    

## Step 4: View and Select Morphospaces

The primary goal of TraitBlender is to simulate image datasets of organisms from theoretical morphospaces. 

By default, TraitBlender comes with one pre-built morphospace, called **CO_Raup**. The combines the morphospace developed by [Contreras-Figueroa and Aragón](https://www.mdpi.com/1424-2818/15/3/431) (a generalization of Raup's classic space) with [Okabe and Yoshimura's](https://doi.org/10.1038/srep42445) allometric shell thickness function to make fully 3D models of molluscan shells.

*In the future, users will be able to install their own morphospaces as well, by creating Python modules which export a 'sample' function*.

## Step 5: Manage Datasets

After selecting a morphospace, the next step is to import or create a dataset that individuals can be sampled from.

Under **Datasets**, select the path to a dataset file (.csv, .tsv, or .xlsx). 

TraitBlender assumes that the first column of the dataset represents the names of organisms that will be sampled, and the remaining columns coorespond to organismal traits (the parameters in the sample function of the morphospace being used).

A list of the traits and scales for the default CO_Raup space can be found [here]().

After a dataset file is selected, the names of the organisms from the morphospace should appear in the dropdown box next to **Sample**. To generate a sample, simply press the **Generate Sample** button, and the sample corresponding the selected individual will be placed as the center of the table.

*Users may also be interested in creating datasets from scratch, or editing/viewing existing ones. The Edit Dataset button creates and incomplete popup, that will eventually be a simple dataset editor*

## Step 6: Orientation

When imaging real organisms, 'standard views' are often define, which specify procedures for orienting and placing specimens down to be imaged. TraitBlender allows for organisms to be placed in this way by defing standard rotation and translation optimizations which interact with specimens in complex ways to allow for standard views.

*In the future, this views will serializable in the config, so they can be easily repeated*

## Step 7: Transforms

Real images are often messy in ways that are difficult to control, but nonetheless may effect the inferences/predictions of models which use them.

TraitBlender implements a transformation pipeline that allows users to specify random noise in their images.

In the Tranforms menu, users may select the path to a property which they want to transforms, and a sampler which they want to transform their property by (these are just functions which draw samples from some selected distribution).

*In the future, distribution parameters will be added to the GUI, for users to better implements transformations*

*Transformations are currently serializable and can be specifed from a config file, but I need to add docs to explain this in more detail*

## Step 8: Render an Image Dataset

...



