import ast
import random
import string
import base64

# --- Variable Renamer (Member 1) ---
class VariableRenamer(ast.NodeTransformer):
    def __init__(self):
        self.mapping = {}

    def generate_random_name(self):
        return ''.join(random.choices(string.ascii_letters, k=8))

    def visit_FunctionDef(self, node):
        original_name = node.name
        new_name = self.generate_random_name()
        self.mapping[original_name] = new_name
        node.name = new_name
        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            original_name = node.id
            if original_name not in self.mapping:
                self.mapping[original_name] = self.generate_random_name()
            node.id = self.mapping[original_name]
        elif isinstance(node.ctx, ast.Load):
            if node.id in self.mapping:
                node.id = self.mapping[node.id]
        return node

# --- Dead Code Inserter (Member 2) ---
class DeadCodeInserter(ast.NodeTransformer):
    """
    Inserts dead code (code that does not affect program logic).
    """
    def random_dead_code(self):
        # Insert a random dead assignment or pass statement
        dead_code_types = [
            ast.Assign(targets=[ast.Name(id='_' + ''.join(random.choices(string.ascii_letters, k=5)), ctx=ast.Store())],
                       value=ast.Constant(value=random.randint(0, 100))),
            ast.Pass(),
            ast.Expr(value=ast.Constant(value=None)),
        ]
        return random.choice(dead_code_types)

    def visit_FunctionDef(self, node):
        # Insert dead code at the start of function body
        node.body.insert(0, self.random_dead_code())
        self.generic_visit(node)
        return node

    def visit_Module(self, node):
        # Insert dead code at the start of the module
        node.body.insert(0, self.random_dead_code())
        self.generic_visit(node)
        return node

# --- String Literal Encoder (Member 3) ---
class StringEncoder(ast.NodeTransformer):
    """
    Encodes string literals using base64 and decodes them at runtime.
    Skips encoding for strings inside f-strings (JoinedStr).
    """
    def __init__(self):
        super().__init__()
        self._in_joinedstr = False

    def visit_JoinedStr(self, node):
        # Mark that we're inside a JoinedStr (f-string)
        self._in_joinedstr = True
        self.generic_visit(node)
        self._in_joinedstr = False
        return node

    def visit_Constant(self, node):
        # Only encode if not inside a JoinedStr and is a string
        if isinstance(node.value, str) and not self._in_joinedstr:
            encoded = base64.b64encode(node.value.encode('utf-8')).decode('utf-8')
            new_node = ast.Call(
                func=ast.Attribute(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id='base64', ctx=ast.Load()),
                            attr='b64decode',
                            ctx=ast.Load()
                        ),
                        args=[ast.Constant(value=encoded)],
                        keywords=[]
                    ),
                    attr='decode',
                    ctx=ast.Load()
                ),
                args=[ast.Constant(value='utf-8')],
                keywords=[]
            )
            return ast.copy_location(new_node, node)
        return node

def transform_ast(ast_tree):
    """
    Applies a pipeline of obfuscation transformations.
    """
    # Variable renaming
    ast_tree = VariableRenamer().visit(ast_tree)
    # Dead code insertion
    ast_tree = DeadCodeInserter().visit(ast_tree)
    # String literal encoding
    ast_tree = StringEncoder().visit(ast_tree)
    ast.fix_missing_locations(ast_tree)
    return ast_tree
