import astor
import base64

def generate_obfuscated_code(ast_tree):
    """
    Converts the transformed AST back into Python source code
    and then applies an extra layer of obfuscation (Base64 encoding).
    Ensures 'import base64' is present for runtime string decoding.
    """
    # Insert 'import base64' at the top if not present
    source_code = astor.to_source(ast_tree)
    if 'import base64' not in source_code:
        source_code = 'import base64\n' + source_code
    encoded = base64.b64encode(source_code.encode('utf-8')).decode('utf-8')
    return encoded
