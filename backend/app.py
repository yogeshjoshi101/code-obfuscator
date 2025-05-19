import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from .obfuscator.lexer import tokenize_code
from .obfuscator.parser import parse_ast
from .obfuscator.transformer import transform_ast
from .obfuscator.generator import generate_obfuscated_code
from .obfuscator.deobfuscator import deobfuscate_code
from .utils import save_mapping, load_mapping

app = Flask(__name__, static_folder=os.path.join(os.getcwd(), 'frontend'))
CORS(app)  # Enable CORS for API calls

# API endpoints
@app.route("/obfuscate", methods=["POST"])
def obfuscate():
    data = request.json
    source_code = data.get("code", "")
    
    # Lexical Analysis (optional for debugging)
    tokens = tokenize_code(source_code)
    
    # Parsing: Build the AST from source code
    ast_tree = parse_ast(source_code)
    if ast_tree is None:
        return jsonify({"error": "Syntax Error in source code"}), 400
    
    # Transformation: Obfuscate the AST
    transformed_ast = transform_ast(ast_tree)
    
    # Code Generation: Convert AST back to source code and encode it
    obfuscated_code = generate_obfuscated_code(transformed_ast)
    
    # Generate a security key and save the mapping
    security_key = str(uuid.uuid4())
    save_mapping(security_key, source_code)
    
    return jsonify({"obfuscated_code": obfuscated_code, "security_key": security_key})

@app.route("/deobfuscate", methods=["POST"])
def deobfuscate():
    data = request.json
    obfuscated_code = data.get("code", "")
    security_key = data.get("security_key", "")
    
    # Load the original code using the security key
    original_code = load_mapping(security_key)
    if original_code is None:
        return jsonify({"error": "Invalid security key"}), 400
    
    return jsonify({"deobfuscated_code": original_code})

# Serve the frontend index.html at the root
@app.route('/')
def serve_index():
    return send_from_directory(os.path.join(os.getcwd(), 'frontend'), 'index.html')

# Serve any static files (CSS, JS, etc.) from the frontend directory
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(os.getcwd(), 'frontend'), path)

if __name__ == "__main__":
    app.run(debug=True)
