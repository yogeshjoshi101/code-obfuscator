import base64
import json

# This module can host additional utility functions as needed.

# Ensure this file is in the backend package root (not inside obfuscator)
def xor_encrypt(data: str, key: str) -> str:
    key = (key * ((len(data) // len(key)) + 1))[:len(data)]
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(data, key))

def encrypt_meta(meta, key):
    meta_json = json.dumps(meta)
    encrypted = xor_encrypt(meta_json, key)
    return base64.b64encode(encrypted.encode()).decode()

def decrypt_meta(enc_meta, key):
    try:
        encrypted = base64.b64decode(enc_meta.encode()).decode()
        decrypted = xor_encrypt(encrypted, key)
        return json.loads(decrypted)
    except Exception:
        return {}
