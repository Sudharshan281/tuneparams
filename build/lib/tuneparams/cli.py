import sys
import os
import time
from tqdm import tqdm
from .utils import SUPPORTED_FUNCTIONS, modify_script, execute_script

VERSION = "0.1.4"

def print_usage():
    print("Usage:")
    print("TuneParams allows you to provide input in two ways:")
    print("1.tuneparams <script.py> param1=value1 param2=value2 ...")
    print("2.tuneparams <script.py> --param-file <param_file.txt>")
    print("NOTE: For the second method, the parameter file should contain parameters separated by commas.")

def parse_param_line(param_line): #parse the params from the params input file
    modifications = {}
    for param in param_line.split(','):
        key, value = param.strip().split('=')
        modifications[key] = int(value) if value.isdigit() else float(value) if '.' in value else value
    return modifications

def simulate_running_animation():
    total_length = 50 
    print("Modifications applied. Running...")

    for i in range(total_length + 1):
        filled_length = i
        line = '\033[92m' + '█' * filled_length + '\033[0m' + ' ' * (total_length - filled_length)
        print(f'\r{line}', end='')
        time.sleep(0.02) 

    print() 

def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    if "--version" in sys.argv:
        print(f"tuneparams version {VERSION}")
        sys.exit(0)

    if "--help" in sys.argv or "-h" in sys.argv:
        print_usage()
        sys.exit(0)

    script_path = sys.argv[1]

    if not script_path.endswith('.py') or not os.path.exists(script_path)   :
        print("Error: The first argument must be a Python script file (with a .py extension).")
        sys.exit(1)

    if "--param-file" in sys.argv:
        param_file_index = sys.argv.index("--param-file") + 1
        param_file_path = sys.argv[param_file_index]

        if not os.path.exists(param_file_path):
            print(f"Error: Parameter file '{param_file_path}' not found.")
            sys.exit(1)
        
        with open(param_file_path, 'r') as param_file:
            for line in param_file:
                modifications = parse_param_line(line.strip())
                print(f"Running script with parameters: {modifications}")

                modified_code = modify_script(script_path, modifications, SUPPORTED_FUNCTIONS)
                
                simulate_running_animation()
                
                execute_script(modified_code)
                
                print("\n")

    else:
        # Command line arguments (original way)
        modifications = {}
        for param in sys.argv[2:]:
            key, value = param.split('=')
            modifications[key] = int(value) if value.isdigit() else float(value) if '.' in value else value

        modified_code = modify_script(script_path, modifications, SUPPORTED_FUNCTIONS)
        
        simulate_running_animation()

        execute_script(modified_code)
        
        print("\n")

if __name__ == "__main__":
    main()
