import json
import os

MAPPING_FILE = os.path.join(os.getcwd(), "code_mapping.json")

def save_mapping(security_key, original_code):
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, "r") as file:
            mappings = json.load(file)
    else:
        mappings = {}
    
    mappings[security_key] = original_code
    
    with open(MAPPING_FILE, "w") as file:
        json.dump(mappings, file)

def load_mapping(security_key):
    if not os.path.exists(MAPPING_FILE):
        return None
    
    with open(MAPPING_FILE, "r") as file:
        mappings = json.load(file)
    
    return mappings.get(security_key)

# This module can host additional utility functions as needed.
