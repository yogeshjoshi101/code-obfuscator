import ast

def parse_ast(code):
    """Parses the Python code into an Abstract Syntax Tree (AST)."""
    try:
        return ast.parse(code)
    except SyntaxError:
        return None
