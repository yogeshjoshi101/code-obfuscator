import ast

class ASTNode:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.children = children or []
        self.value = value

def parse_ast(code):
    """
    Parses the Python code into an Abstract Syntax Tree (AST).
    Returns the AST node or None if syntax error.
    """
    try:
        return ast.parse(code)
    except SyntaxError:
        return None
    @_('statements statement')  # type: ignore
    def statements(self, p):
        return ASTNode('statements', p.statements.children + [p.statement])

    @_('statement')  # type: ignore
    def statements(self, p):
        return ASTNode('statements', [p.statement])

    @_('ID "=" expr NEWLINE')  # type: ignore
    def statement(self, p):
        return ASTNode('assign', [ASTNode('id', value=p.ID), p.expr])

    @_('expr NEWLINE')  # type: ignore
    def statement(self, p):
        return p.expr

    @_('NUMBER')  # type: ignore
    def expr(self, p):
        return ASTNode('number', value=p.NUMBER)

    @_('STRING')  # type: ignore
    def expr(self, p):
        return ASTNode('string', value=p.STRING)

    @_('ID')  # type: ignore
    def expr(self, p):
        return ASTNode('id', value=p.ID)

    # ...extend for more Python syntax as needed...

def parse_ast(code):
    """
    Parses the Python code into an Abstract Syntax Tree (AST).
    Returns the AST node or None if syntax error.
    """
    try:
        return ast.parse(code)
    except SyntaxError:
        return None
