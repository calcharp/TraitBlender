"""
TraitBlender Material Application Utilities

Helper functions for applying materials and textures to objects in TraitBlender.
"""

import bpy
import os
import re
from PIL import ImageColor


# Supported texture types
VALID_TEXTURES = {"DIFFUSE", "AO", "ROUGHNESS", "METALLIC", "NORMAL", "DISPLACEMENT"}


def apply_material(object_name: str, textures_path: str = None, hex_color: str = None, material_name: str = None):
    """
    Apply a material to a given object in Blender.
    
    Can create a textured material, solid color material, or apply an existing material.
    
    Args:
        object_name (str): Name of the object in the scene to apply material to
        textures_path (str, optional): Path to folder containing texture files matching 
                                     format {TYPE}_{description}.ext
        hex_color (str, optional): Hex color code (e.g., "#FF5733", "#000000")
        material_name (str, optional): Name of existing material to apply
        
    Returns:
        bpy.types.Material: The applied material, or None if failed
        
    Example:
        # Apply textures (creates material named "wood_textures")
        apply_material("Cube", textures_path="/path/to/wood_textures/")
        
        # Apply solid color (creates material named "#FF5733")
        apply_material("Cube", hex_color="#ff5733")
        
        # Apply existing material
        apply_material("Cube", material_name="My_Existing_Material")
    """
    
    # Count how many options are provided
    options_count = sum(x is not None for x in [textures_path, hex_color, material_name])
    
    if options_count == 0:
        print("Error: Must specify one of: textures_path, hex_color, or material_name.")
        return None
    
    if options_count > 1:
        print("Error: Can only specify one of: textures_path, hex_color, or material_name.")
        return None
    
    # Validate object exists
    if object_name not in bpy.data.objects or bpy.data.objects[object_name].type != 'MESH':
        print(f"Error: Mesh '{object_name}' not found or is not a mesh.")
        return None

    if material_name:
        # Apply existing material
        if material_name in bpy.data.materials:
            material = bpy.data.materials[material_name]
            print(f"Found existing material '{material_name}'")
        else:
            print(f"Error: Material '{material_name}' not found in scene.")
            return None
    
    elif hex_color:
        # Create solid color material (named after hex code or material_name if provided)
        try:
            # Convert hex to RGBA (PIL returns RGB tuple, we add alpha=1.0)
            rgb = ImageColor.getrgb(hex_color)
            rgba = (*[c/255.0 for c in rgb], 1.0)  # Convert to 0-1 range and add alpha
            
            # Name material after material_name if provided, else hex code
            mat_name = material_name if material_name else hex_color
            material = bpy.data.materials.new(name=mat_name)
            material.use_nodes = True
            
            bsdf = material.node_tree.nodes["Principled BSDF"]
            bsdf.inputs["Base Color"].default_value = rgba
            print(f"Created solid color material '{mat_name}' for '{object_name}'")
            
        except ValueError as e:
            print(f"Error: Invalid hex color '{hex_color}': {e}")
            return None
    
    else:
        # Create textured material (named after folder)
        folder_name = os.path.basename(textures_path.rstrip(os.sep))
        material = _create_textured_material(object_name, textures_path, folder_name)
        if not material:
            return None

    # Apply material to object
    mesh_obj = bpy.data.objects.get(object_name)
    if mesh_obj.data.materials:
        # Replace the first material slot if one exists
        mesh_obj.data.materials[0] = material
    else:
        # Otherwise, add the material to the object's material slots
        mesh_obj.data.materials.append(material)

    return material


def _create_textured_material(object_name: str, textures_path: str, material_name: str):
    """
    Internal function to create a textured material from files.
    """
    # Validate textures directory
    if not os.path.isdir(textures_path):
        print(f"Error: Directory '{textures_path}' does not exist.")
        return None
    
    # Create material with folder name
    material = bpy.data.materials.new(name=material_name)
    material.use_nodes = True
    node_tree = material.node_tree

    # Get default nodes
    bsdf = node_tree.nodes["Principled BSDF"]
    output = node_tree.nodes["Material Output"]

    # Regex to match format TYPE_description.ext
    pattern = re.compile(rf"^({'|'.join(VALID_TEXTURES)})_.+\.[^.]+$")

    # List matching files
    matching_files = [f for f in os.listdir(textures_path) if pattern.match(f)]
    
    if not matching_files:
        print(f"Warning: No texture files found in '{textures_path}' matching the required pattern.")
        bpy.data.materials.remove(material)
        return None

    # Check for duplicate texture types
    for texture_type in VALID_TEXTURES:
        files_of_type = [f for f in matching_files if f.startswith(texture_type + "_")]
        if len(files_of_type) > 1:
            print(f"Error: More than one texture of type {texture_type} exists: {files_of_type}")
            bpy.data.materials.remove(material)
            return None

    # Create dictionary mapping texture types to file paths
    texture_files = {
        f.split('_', 1)[0]: os.path.join(textures_path, f)
        for f in matching_files
    }

    # Create texture nodes for each found texture
    texture_nodes = {}
    for texture_type, file_path in texture_files.items():
        tex_node = node_tree.nodes.new("ShaderNodeTexImage")
        tex_node.image = bpy.data.images.load(file_path)
        
        # Set color space: Diffuse uses sRGB; all others use Non-Color
        tex_node.image.colorspace_settings.name = "sRGB" if texture_type == "DIFFUSE" else "Non-Color"
        texture_nodes[texture_type] = tex_node

    # Connect texture nodes to material
    _connect_texture_nodes(node_tree, texture_nodes, bsdf, output)
    
    print(f"Successfully applied textures to '{object_name}' with material '{material.name}'")
    return material


def _connect_texture_nodes(node_tree, texture_nodes, bsdf, output):
    """
    Internal function to connect texture nodes to the Principled BSDF and Material Output.
    
    Args:
        node_tree: The material's node tree
        texture_nodes: Dictionary of texture type -> texture node
        bsdf: Principled BSDF node
        output: Material Output node
    """
    
    # Handle Diffuse and AO combination
    if "AO" in texture_nodes and "DIFFUSE" not in texture_nodes:
        raise ValueError("Error: AO exists without a corresponding DIFFUSE texture.")

    if "DIFFUSE" in texture_nodes:
        diffuse_node = texture_nodes["DIFFUSE"]
        
        if "AO" in texture_nodes:
            # Multiply Diffuse and AO textures
            ao_node = texture_nodes["AO"]
            mix_node = node_tree.nodes.new("ShaderNodeMixRGB")
            mix_node.blend_type = 'MULTIPLY'
            
            # Connect Diffuse and AO to the MixRGB node (using numbered inputs)
            node_tree.links.new(diffuse_node.outputs["Color"], mix_node.inputs[1])
            node_tree.links.new(ao_node.outputs["Color"], mix_node.inputs[2])
            node_tree.links.new(mix_node.outputs["Color"], bsdf.inputs["Base Color"])
        else:
            # Just connect diffuse directly
            node_tree.links.new(diffuse_node.outputs["Color"], bsdf.inputs["Base Color"])

    # Connect Roughness and Metallic textures
    if "ROUGHNESS" in texture_nodes:
        node_tree.links.new(texture_nodes["ROUGHNESS"].outputs["Color"], bsdf.inputs["Roughness"])
    
    if "METALLIC" in texture_nodes:
        node_tree.links.new(texture_nodes["METALLIC"].outputs["Color"], bsdf.inputs["Metallic"])

    # Handle Normal vs. Displacement (displacement takes priority)
    if "DISPLACEMENT" in texture_nodes:
        disp_tex = texture_nodes["DISPLACEMENT"]
        disp_node = node_tree.nodes.new("ShaderNodeDisplacement")
        node_tree.links.new(disp_tex.outputs["Color"], disp_node.inputs["Height"])
        node_tree.links.new(disp_node.outputs["Displacement"], output.inputs["Displacement"])
        
        if "NORMAL" in texture_nodes:
            print("Warning: Normal and Displacement both found. Only Displacement will be used.")
            
    elif "NORMAL" in texture_nodes:
        normal_tex = texture_nodes["NORMAL"]
        normal_map_node = node_tree.nodes.new("ShaderNodeNormalMap")
        node_tree.links.new(normal_tex.outputs["Color"], normal_map_node.inputs["Color"])
        node_tree.links.new(normal_map_node.outputs["Normal"], bsdf.inputs["Normal"])

    # Connect BSDF to Material Output
    node_tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])


def get_texture_info(textures_path: str):
    """
    Get information about available textures in a directory.
    
    Args:
        textures_path (str): Path to the folder containing texture files
        
    Returns:
        dict: Dictionary with texture types as keys and file names as values
    """
    if not os.path.isdir(textures_path):
        return {}
        
    pattern = re.compile(rf"^({'|'.join(VALID_TEXTURES)})_.+\.[^.]+$")
    matching_files = [f for f in os.listdir(textures_path) if pattern.match(f)]
    
    return {
        f.split('_', 1)[0]: f
        for f in matching_files
    }


# Backward compatibility alias
set_textures = apply_material