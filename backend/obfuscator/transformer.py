import ast
import random
import string

def generate_random_name():
    """Generates a random 8-character name."""
    return ''.join(random.choices(string.ascii_letters, k=8))

class CodeObfuscator(ast.NodeTransformer):
    def __init__(self):
        self.mapping = {}

    def visit_FunctionDef(self, node):
        # Obfuscate function name
        original_name = node.name
        new_name = generate_random_name()
        self.mapping[original_name] = new_name
        node.name = new_name
        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        # Obfuscate variable names (both on store and load)
        if isinstance(node.ctx, ast.Store):
            original_name = node.id
            if original_name not in self.mapping:
                self.mapping[original_name] = generate_random_name()
            node.id = self.mapping[original_name]
        elif isinstance(node.ctx, ast.Load):
            if node.id in self.mapping:
                node.id = self.mapping[node.id]
        return node

def transform_ast(ast_tree):
    """Transforms the AST using our obfuscator."""
    obfuscator = CodeObfuscator()
    return obfuscator.visit(ast_tree)
