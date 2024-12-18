import os
import time
import itertools
import sys
from tqdm import tqdm
from .utils import SUPPORTED_FUNCTIONS, modify_script, execute_script, extract_metrics, store_results, query_results

VERSION = "0.2.3"

def print_usage():
    print("Usage:")
    print("TuneParams allows you to provide input in three ways:")
    print("1. tuneparams <script.py> param1=value1 param2=value2 ...")
    print("2. tuneparams <script.py> --param-file <param_file.txt>")
    print("3. tuneparams <script.py> --range <range_file.txt>")
    print("4. tuneparams --query <query_condition>")

def parse_param_line(param_line):
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

def parse_range_line(range_line):
    key, value = range_line.split('=')
    key = key.strip()
    value = value.strip().strip('[]')  

    if value.startswith('[') and value.endswith(']'): 
        value_list = value[1:-1].split(',')  
        return key, [v.strip().strip("'").strip('"') for v in value_list] 

    start, end = map(str.strip, value.split(','))  
    if start.isdigit() and end.isdigit():
        return key, (int(start), int(end))  
    else:
        return key, (float(start), float(end))  

def generate_combinations(modifications):
    """Generates all combinations for range-based parameters."""
    ranges = {k: v for k, v in modifications.items() if isinstance(v, tuple)}  # For float ranges
    lists = {k: v for k, v in modifications.items() if isinstance(v, list)}  # For lists of strings
    static_params = {k: v for k, v in modifications.items() if not isinstance(v, (tuple, list))}

    param_names = list(ranges.keys()) + list(lists.keys())
    
    # Find all possible values for each parameter, and generate all combinations
    param_values = []
    for key in param_names:
        if key in ranges:
            start, end = ranges[key]
            step = 1 if isinstance(start, int) else 0.1  
            param_values.append([round(start + step * i, 1) for i in range(int((end - start) / step) + 1)])  # List of values
        elif key in lists:
            param_values.append(lists[key])  


    for combo in itertools.product(*param_values):
        combo_dict = {}
        for i, name in enumerate(param_names):
            if isinstance(modifications[name], tuple) and len(modifications[name]) == 2:
                if isinstance(modifications[name][0], int):
                    combo_dict[name] = int(combo[i])
                else:
                    combo_dict[name] = combo[i]
            else:
                combo_dict[name] = combo[i]
        yield {**static_params, **combo_dict}

def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    clear_file = True 
    
    # print("Arguments received:", sys.argv) 

    if "--version" in sys.argv:
        print(f"tuneparams version {VERSION}")
        sys.exit(0)

    if "--help" in sys.argv or "-h" in sys.argv:
        print_usage()
        sys.exit(0)

    if "--query" in sys.argv:
        query_index = sys.argv.index("--query") + 1
        if query_index < len(sys.argv):    
            query = sys.argv[query_index]
            print("QUERY FOUND: ", query)
            query_results(query)
            return
        else:
            print("Error: No query condition provided.")
            sys.exit(1)

    script_path = sys.argv[1]

    if not script_path.endswith('.py') or not os.path.exists(script_path):
        print("Error: The first argument must be a Python script file (with a .py extension).")
        sys.exit(1)

    if "--param-file" in sys.argv:
        param_file_index = sys.argv.index("--param-file") + 1
        param_file_path = sys.argv[param_file_index]

        if not os.path.exists(param_file_path):
            print(f"Error: Parameter file '{param_file_path}' not found.")
            sys.exit(1)

        with open(param_file_path, 'r') as param_file:
            lines = param_file.readlines()
            for idx, line in enumerate(lines):
                # if line is empty break
                if not line.strip():
                    break
                modifications = parse_param_line(line.strip())
                print(f"Running script with parameters: {modifications}")

                modified_code = modify_script(script_path, modifications, SUPPORTED_FUNCTIONS)
                
                simulate_running_animation()

                printed_output = execute_script(modified_code)
                results = extract_metrics(printed_output)  #extract metrics from the output
                print("SENDING MODIFICATION: ", modifications)
                store_results(idx + 1, results, modifications, clear_file)
                clear_file = False 

    elif "--range" in sys.argv:
        range_file_index = sys.argv.index("--range") + 1
        range_file_path = sys.argv[range_file_index]

        if not os.path.exists(range_file_path):
            print(f"Error: Range file '{range_file_path}' not found.")
            sys.exit(1)

        modifications = {}
        with open(range_file_path, 'r') as range_file:
            lines = range_file.readlines()
            for line in lines:
                key, value = parse_range_line(line.strip())
                modifications[key] = value

        for idx, combo in enumerate(generate_combinations(modifications)):
            print(f"Running script with parameters: {combo}")

            modified_code = modify_script(script_path, combo, SUPPORTED_FUNCTIONS)
            
            simulate_running_animation()

            printed_output = execute_script(modified_code)
            results = extract_metrics(printed_output)

            store_results(idx + 1, results, combo,clear_file)
            clear_file = False  

    else:
        modifications = {}
        for param in sys.argv[2:]:
            key, value = param.split('=')
            modifications[key] = int(value) if value.isdigit() else float(value) if '.' in value else value

        print(f"Running script with parameters: {modifications}")

        modified_code = modify_script(script_path, modifications, SUPPORTED_FUNCTIONS)
        
        simulate_running_animation()

        printed_output = execute_script(modified_code)
        results = extract_metrics(printed_output)

        store_results(1, results,modifications, clear_file)

if __name__ == "__main__":
    main()
