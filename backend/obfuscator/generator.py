import astor
import base64

def generate_obfuscated_code(ast_tree):
    """
    Converts the transformed AST back into Python source code
    and then applies an extra layer of obfuscation (Base64 encoding).
    """
    source_code = astor.to_source(ast_tree)
    encoded = base64.b64encode(source_code.encode('utf-8')).decode('utf-8')
    return encoded
