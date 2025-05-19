import base64

def deobfuscate_code(obfuscated_code):
    """
    Reverses the Base64 encoding to retrieve the obfuscated Python source.
    (Note: This does not reverse the AST transformation.)
    """
    try:
        decoded = base64.b64decode(obfuscated_code.encode('utf-8')).decode('utf-8')
        return decoded
    except Exception as e:
        return f"Deobfuscation failed: {str(e)}"
