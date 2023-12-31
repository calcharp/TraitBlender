#!/bin/bash

# Path to Blender executable
blender_executable="C:/Program Files/Blender Foundation/Blender 3.3/blender.exe"

# Path to the bpy script
script_path="D:/TraitBlender/TraitBlender/generate_dataset.py"  # Replace with the actual path to your updated script

# Paths to the make_mesh_function, csv_file, and json_file
make_mesh_function_path="D://TraitBlender/TraitBlender/Examples/snails/make_raupian_snail.py"
csv_file_path="C://Users/caleb/Downloads/wc2.csv"
json_file_path="C://Users/caleb/Downloads/raup_snails/traitblender_settings.json"

# Run Blender with the bpy script and the paths as arguments
"$blender_executable" --background --python "$script_path" -- "$make_mesh_function_path" "$csv_file_path" "$json_file_path"
