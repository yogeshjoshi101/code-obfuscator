import base64
import json
from .transformer import deobfuscate_pipeline

# Fix import for utils (relative import)
from ..utils import decrypt_meta

def deobfuscate_code(obfuscated_code, key=""):
    """
    Fully reverses all obfuscation steps using stored meta.
    """
    try:
        decoded = base64.b64decode(obfuscated_code.encode()).decode()
        payload = json.loads(decoded)
        code = payload['code']
        encrypted_meta = payload.get('meta', "")
        meta = decrypt_meta(encrypted_meta, key)
        return deobfuscate_pipeline(code, meta)
    except Exception as e:
        return f"Deobfuscation failed: {str(e)}"
