import importlib
import os


def initialize_function_calling(module_names):
    functions = {}
    function_descriptions = []
    for name in module_names:
        try:
            module_path = f"{module_directory}.{name}"
            module = importlib.import_module(module_path)
            functions[name] = module.function
            function_descriptions.append(module.description)
        except ImportError:
            print(f"Failed to import {name}")
        except AttributeError:
            print(f"Module {name} does not have the required attributes")
        except Exception as e:
            print(f"An unexpected error occurred while importing {name}: {e}")
    return functions, function_descriptions


module_directory = 'functions'
module_names = [f.replace('.py', '') for f in os.listdir(module_directory) if f.endswith('.py')]
functions, function_descriptions = initialize_function_calling(module_names)

print("Loaded Functions:")
for func in functions:
    print(f"{func} - {functions[func]}")

print("\nDescriptions:")
for desc in function_descriptions:
    print(desc)
