import os
import importlib
import inspect
import ast

def find_registered_classes():
    """
    Dynamically discover all classes that use the @config_subsection_register decorator
    by scanning through Python files in this directory.
    """
    config_classes = []
    current_dir = os.path.dirname(__file__)
    
    # Get all Python files in this directory (excluding __init__.py)
    python_files = [f for f in os.listdir(current_dir) 
                   if f.endswith('.py') and f != '__init__.py']
    
    for filename in python_files:
        filepath = os.path.join(current_dir, filename)
        
        try:
            # Parse the file to find classes with @config_subsection_register decorator
            with open(filepath, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            # Find all class definitions
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Check if the class has decorators
                    if node.decorator_list:
                        for decorator in node.decorator_list:
                            # Check if it's a function call (like @config_subsection_register("name"))
                            if isinstance(decorator, ast.Call):
                                if isinstance(decorator.func, ast.Name) and decorator.func.id == 'config_subsection_register':
                                    # Found a class with @config_subsection_register decorator
                                    module_name = filename[:-3]  # Remove .py extension
                                    try:
                                        # Import the module and get the class
                                        module = importlib.import_module(f'.{module_name}', package=__name__)
                                        class_obj = getattr(module, node.name)
                                        config_classes.append(class_obj)
                                    except (ImportError, AttributeError) as e:
                                        print(f"Warning: Could not import {node.name} from {module_name}: {e}")
                            # Check if it's just a name (like @config_subsection_register)
                            elif isinstance(decorator, ast.Name) and decorator.id == 'config_subsection_register':
                                # Found a class with @config_subsection_register decorator
                                module_name = filename[:-3]  # Remove .py extension
                                try:
                                    # Import the module and get the class
                                    module = importlib.import_module(f'.{module_name}', package=__name__)
                                    class_obj = getattr(module, node.name)
                                    config_classes.append(class_obj)
                                except (ImportError, AttributeError) as e:
                                    print(f"Warning: Could not import {node.name} from {module_name}: {e}")
                                    
        except (SyntaxError, FileNotFoundError) as e:
            print(f"Warning: Could not parse {filename}: {e}")
    
    return config_classes

# Dynamically discover all registered configuration classes
configs = find_registered_classes()

__all__ = ["configs"]