import importlib
import inspect
import os


def initialize_function_calling(module_names, module_directory):
    functions = {}
    function_descriptions = []
    for name in module_names:
        try:
            module_path = f"{module_directory}.{name}"
            module = importlib.import_module(module_path)

            for func_name, func in inspect.getmembers(module, inspect.isfunction):
                functions[func_name] = func

            if hasattr(module, 'description'):
                function_descriptions.append(module.description)
            else:
                print(f"Module {name} does not have a 'description' attribute")

        except ImportError as e:
            print(f"Failed to import {name}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while importing {name}: {e}")

    return functions, function_descriptions


module_directory = 'functions'
module_names = [f.replace('.py', '') for f in os.listdir(module_directory) if f.endswith('.py')]
functions, function_descriptions = initialize_function_calling(module_names, module_directory)

# print("Loaded Functions:")
# for func_name, func in functions.items():
#     print(f"{func_name} - {func}")
#
# print("\nDescriptions:")
# for desc in function_descriptions:
#     print(desc)
