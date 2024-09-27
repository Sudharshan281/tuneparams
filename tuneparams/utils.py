def modify_script(script_path, modifications, supported_functions):
    import ast
    import astor
    from .script_modifier import ScriptModifier

    with open(script_path, 'r') as file:
        tree = ast.parse(file.read(), filename=script_path)

    modifier = ScriptModifier(modifications)
    tree = modifier.visit(tree)
    ast.fix_missing_locations(tree)

    modified_code_str = astor.to_source(tree)
    # print(f"Modified Code for {script_path}:\n{modified_code_str}")
    
    return modified_code_str

def execute_script(script_code):
    exec_globals = {}
    exec(script_code, exec_globals)

SUPPORTED_FUNCTIONS = {
    'train_test_split',
    'RandomForestClassifier',
    'LinearRegression',
    'LogisticRegression',
    'Ridge',
    'Lasso',
    'DecisionTreeClassifier',
    'DecisionTreeRegressor',
    'KNeighborsClassifier',
    'KNeighborsRegressor',
    'SVC',
    'SVR'
}
