import ast
import astor
import csv
import contextlib
import io
import os
import pandas as pd
from .script_modifier import ScriptModifier

RESULTS_FILE = 'results.csv'

# SUPPORTED_FUNCTIONS = {
#     'train_test_split',
#     'RandomForestClassifier',
#     'LinearRegression',
#     'LogisticRegression',
#     'Ridge',
#     'Lasso',
#     'DecisionTreeClassifier',
#     'DecisionTreeRegressor',
#     'KNeighborsClassifier',
#     'KNeighborsRegressor',
#     'SVC',
#     'SVR'
# }

def modify_script(script_path, modifications, supported_functions):
    with open(script_path, 'r') as file:
        tree = ast.parse(file.read(), filename=script_path)

    modifier = ScriptModifier(modifications)
    tree = modifier.visit(tree)
    ast.fix_missing_locations(tree)

    modified_code_str = astor.to_source(tree)
    
    # modified code after parameter substitution
    print(f"Modified Code for {script_path}:\n{modified_code_str}")
    
    return modified_code_str

def execute_script(script_code):
    exec_globals = {}
    
    # get the printed output
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        exec(script_code, exec_globals)
    
    printed_output = output.getvalue()
    return printed_output

def extract_metrics(printed_output):
    """
    from the printed output, extract the metrics which are in the format 'metric_name: value'
    """
    results = {}
    for line in printed_output.splitlines():
        line = line.strip()  # remove the white spaces
        if ':' in line:
            key, value = line.split(':', 1)  # splits at the first ':'
            key = key.strip().lower()

            # Extract the numeric part of the value using regex
            numeric_value = re.search(r'[-+]?\d*\.?\d+', value.strip())

            if numeric_value:
                try:
                    results[key] = float(numeric_value.group())
                except ValueError:
                    continue
    return results

def store_results(id, results, modifications, clear_file=False):
    """Stores the results of each run along with its ID and prints the output."""
    file_exists = os.path.exists(RESULTS_FILE)
    print("INPUT PARAMS IN STORE RESULTS: \n", modifications)
    
    #remove previous entries
    if clear_file and file_exists:
        with open(RESULTS_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Input Parameters"] + list(results.keys()))

    modifications_list = [f"{key}: {value}" for key, value in modifications.items()]

    with open(RESULTS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists: 
            writer.writerow(["ID", "Input Parameters"] + list(results.keys()))

        writer.writerow([id, modifications_list] + list(results.values()))
        
    print(f"Stored Results - ID: {id}, Input Params: {modifications}, Results: {results}")


import re

def query_results(query):
    print(f"Querying with condition: {query}") 

    operators = {
        '>=': lambda x, y: x >= y,
        '>': lambda x, y: x > y,
        '<=': lambda x, y: x <= y,
        '<': lambda x, y: x < y,
        '=': lambda x, y: x == y
    }

    pattern = re.compile(r"([a-zA-Z_]+)\s*(>=|<=|>|<|=)\s*([0-9\.]+)")

    #find all matches in the query
    matches = pattern.findall(query)

    if not matches:
        print("Invalid query format. Please provide a valid condition.")
        return

    conditions = [(param, op, float(value)) for param, op, value in matches]

    #Check if conditions were found
    if not conditions:
        print("Invalid query format. Please provide a valid condition.")
        return

    df = pd.read_csv(RESULTS_FILE)

    for param, _, _ in conditions:
        if param not in df.columns:
            print(f"Column '{param}' not found in the results.")
            return
        df[param] = df[param].astype(float)

    #now, we build a filter for the dataframe based on condtns
    filter_expression = pd.Series([True] * len(df))  #start with all true

    for param, op, value in conditions:
        if op in operators:
            filter_expression &= df[param].apply(lambda x: operators[op](x, value))

    # Apply the combined filter to the DataFrame
    filtered_df = df[filter_expression]

    # Output matching results
    if filtered_df.empty:
        print("No results found matching the query.")
        return

    for _, row in filtered_df.iterrows():
        print(f"Input Params: {row['Input Parameters']}")
