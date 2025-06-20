import os
import tempfile
import logging
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from .obfuscator.lexer import tokenize_code
from .obfuscator.parser import parse_ast
from .obfuscator.generator import generate_obfuscated_code
from .obfuscator.deobfuscator import deobfuscate_code

app = Flask(__name__, static_folder=os.path.join(os.getcwd(), 'frontend'))
CORS(app)  # Enable CORS for API calls

# Setup logging
logging.basicConfig(level=logging.INFO)

# API endpoints
@app.route("/obfuscate", methods=["POST"])
def obfuscate():
    data = request.json
    source_code = data.get("code", "")
    features = data.get("features", None)
    key = data.get("key", "")
    if not isinstance(source_code, str) or not source_code.strip():
        logging.warning("No code provided for obfuscation.")
        return jsonify({"error": "No code provided"}), 400
    if not key or not isinstance(key, str):
        return jsonify({"error": "Key is required for obfuscation"}), 400

    # Lexical Analysis (optional for debugging)
    tokens = tokenize_code(source_code)

    # Parsing: Build the AST from source code
    ast_tree = parse_ast(source_code)
    if ast_tree is None:
        logging.warning("Syntax error in source code.")
        return jsonify({"error": "Syntax Error in source code"}), 400

    try:
        # Code Generation: Obfuscate and encode
        obfuscated_code = generate_obfuscated_code(source_code, features, key)
        return jsonify({"obfuscated_code": obfuscated_code})
    except Exception as e:
        logging.error(f"Obfuscation failed: {e}")
        return jsonify({"error": "Obfuscation failed"}), 500

@app.route("/deobfuscate", methods=["POST"])
def deobfuscate():
    data = request.json
    obfuscated_code = data.get("code", "")
    key = data.get("key", "")
    if not isinstance(obfuscated_code, str) or not obfuscated_code.strip():
        logging.warning("No code provided for deobfuscation.")
        return jsonify({"error": "No code provided"}), 400
    if not key or not isinstance(key, str):
        return jsonify({"error": "Key is required for deobfuscation"}), 400
    try:
        readable_code = deobfuscate_code(obfuscated_code, key)
        return jsonify({"deobfuscated_code": readable_code})
    except Exception as e:
        logging.error(f"Deobfuscation failed: {e}")
        return jsonify({"error": "Deobfuscation failed"}), 500

@app.route("/features", methods=["GET"])
def features():
    return jsonify({
        "features": [
            "rename_identifiers",
            "encode_strings",
            "dead_code",
            "junk_code",
            "minify",
            "strip_comments"
        ]
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '' or not file.filename.endswith('.py'):
        return jsonify({"error": "Invalid file"}), 400
    code = file.read().decode('utf-8')
    return jsonify({"code": code})

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    code = data.get("code", "")
    filename = data.get("filename", "output.py")
    # Use a secure temporary file in the backend directory
    temp_dir = os.path.dirname(os.path.abspath(__file__))
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", dir=temp_dir, delete=False, encoding="utf-8") as tmp:
        tmp.write(code)
        tmp_path = tmp.name
    try:
        return send_file(tmp_path, as_attachment=True, download_name=filename)
    finally:
        # Clean up the temp file after sending
        try:
            os.remove(tmp_path)
        except Exception:
            pass

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
    app.run(debug=True)
