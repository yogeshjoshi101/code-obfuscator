import base64
import json
from .transformer import obfuscate_pipeline

# Fix import for utils (relative import)
from ..utils import encrypt_meta

def generate_obfuscated_code(source_code, features=None, key=""):
    """
    Obfuscates code and encodes it with meta for deobfuscation.
    """
    obf_code, meta = obfuscate_pipeline(source_code, features)
    encrypted_meta = encrypt_meta(meta, key)
    payload = {
        'code': obf_code,
        'meta': encrypted_meta
    }
    encoded = base64.b64encode(json.dumps(payload).encode()).decode()
    return encoded
