"""
Test script for the Transform Editor
Run this to test the standalone app without Blender.
"""

from transforms_editor import TransformEditor

# Test data - sample transforms pipeline
test_yaml = """- property_path: world.color
  sampler_name: dirichlet
  params:
    alphas: [0.3, 0.3, 0.3, 1]
- property_path: lamp.power
  sampler_name: gamma
  params:
    alpha: 2
    beta: 5
- property_path: camera.location
  sampler_name: normal
  params:
    mu: 0
    sigma: 0.1
    n: 3
"""

if __name__ == "__main__":
    print("Launching Transform Pipeline Editor...")
    print("This is a test of the standalone app.")
    print()
    
    # Create and run the editor
    app = TransformEditor()
    app.load_pipeline_from_yaml(test_yaml)
    app.run(window_title="Transform Pipeline Editor - Test Mode")
    
    # Show results
    print("\n" + "="*50)
    print("App closed")
    print(f"Export requested: {app.export_requested}")
    
    if app.export_requested:
        print("\nFinal YAML output:")
        print("-"*50)
        print(app.final_yaml_data)
        print("-"*50)
    else:
        print("\nChanges not exported (checkbox was unchecked or cancelled)")

