import ast

class ScriptModifier(ast.NodeTransformer):
    def __init__(self, modifications):
        self.modifications = modifications

    def visit_FunctionDef(self, node):
        """Visit function definitions and modify default parameter values."""
        for i, default in enumerate(node.args.defaults):
            if i < len(node.args.args):
                arg_name = node.args.args[-len(node.args.defaults) + i].arg
                if arg_name in self.modifications:
                    new_value = self.modifications[arg_name]
                    node.args.defaults[i] = ast.Constant(value=new_value)
        return self.generic_visit(node)

    def visit_Assign(self, node):
        """Visit assignments and modify values if they match any modification keys."""
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, (int, float, str)):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in self.modifications:
                    new_value = self.modifications[target.id]
                    node.value = ast.Constant(value=new_value)
        return self.generic_visit(node)

    def visit_Call(self, node):
        """Visit all function calls and modify keyword arguments and positional arguments."""
        for keyword in node.keywords:
            if keyword.arg in self.modifications:
                new_value = self.modifications[keyword.arg]
                keyword.value = ast.Constant(value=new_value)

        for i, arg in enumerate(node.args):
            if isinstance(arg, ast.Name) and arg.id in self.modifications:
                new_value = self.modifications[arg.id]
                node.args[i] = ast.Constant(value=new_value)

        return self.generic_visit(node)
