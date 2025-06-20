# Advanced Python Code Obfuscator & De-Obfuscator

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Quick Start](#quick-start)
- [Frontend Usage](#frontend-usage)
- [Backend API](#backend-api)
  - [Obfuscate Endpoint](#obfuscate-endpoint)
  - [Deobfuscate Endpoint](#deobfuscate-endpoint)
  - [Upload Endpoint](#upload-endpoint)
  - [Download Endpoint](#download-endpoint)
  - [Features Endpoint](#features-endpoint)
  - [Health Endpoint](#health-endpoint)
- [Obfuscation Pipeline](#obfuscation-pipeline)
  - [Lexical Analysis](#lexical-analysis)
  - [Syntax Analysis](#syntax-analysis)
  - [AST Transformations](#ast-transformations)
  - [Code Generation](#code-generation)
  - [Meta Encryption](#meta-encryption)
  - [Deobfuscation Pipeline](#deobfuscation-pipeline)
- [Frontend Code Walkthrough](#frontend-code-walkthrough)
- [Backend Code Walkthrough](#backend-code-walkthrough)
  - [app.py](#apppy)
  - [obfuscator/lexer.py](#obfuscatorlexerpy)
  - [obfuscator/parser.py](#obfuscatorparserpy)
  - [obfuscator/transformer.py](#obfuscatortransformerpy)
  - [obfuscator/generator.py](#obfuscatorgeneratorpy)
  - [obfuscator/deobfuscator.py](#obfuscatordeobfuscatorpy)
  - [utils.py](#utilspy)
- [Security Considerations](#security-considerations)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Introduction

This project is an **Advanced Python Code Obfuscator & De-Obfuscator** built using compiler design principles. It provides a web-based interface for obfuscating and deobfuscating Python code, making it harder to reverse-engineer or understand. The system leverages Abstract Syntax Tree (AST) transformations, string encoding, identifier renaming, dead/junk code insertion, minification, and meta-data encryption.

The tool is designed for educational, research, and security purposes, demonstrating how code can be programmatically transformed and protected.

---

## Features

- **Lexical Analysis:** Tokenizes Python code for analysis.
- **Syntax Analysis:** Parses code into an AST for structural understanding.
- **Identifier Renaming:** Randomizes variable, function, and class names.
- **String Encoding:** Encodes string literals using Base64.
- **Dead Code Insertion:** Adds unreachable code to confuse static analysis.
- **Junk Code Insertion:** Adds random, unused functions.
- **Minification:** Removes comments, whitespace, and unnecessary formatting.
- **Meta-data Encryption:** Stores transformation meta-data encrypted with a user-provided key.
- **Deobfuscation:** Fully reverses all transformations using the meta-data and key.
- **Web Frontend:** User-friendly interface for code input, obfuscation, deobfuscation, file upload/download, and key management.
- **REST API:** Backend endpoints for integration and automation.
- **Drag-and-Drop File Upload:** Easily load `.py` files.
- **Copy/Paste Obfuscation String:** Securely share or store obfuscated code.
- **Output Download:** Download obfuscated or deobfuscated code as a file.
- **Output Edit Toggle:** Make output read-only or editable.

---

## Project Structure

```
code-obfuscator/
│
├── backend/
│   ├── app.py
│   ├── utils.py
│   └── obfuscator/
│       ├── __init__.py
│       ├── lexer.py
│       ├── parser.py
│       ├── transformer.py
│       ├── generator.py
│       └── deobfuscator.py
│
├── frontend/
│   ├── index.html
│   ├── js/
│   │   ├── api.js
│   │   └── script.js
│   └── css/
│       └── styles.css
│
├── docs/
│   └── README.md
│
├── requirements.txt
├── run.py
└── .gitignore
```

---

## Installation & Setup

### Prerequisites

- Python 3.7+
- pip (Python package manager)
- Node.js (optional, for advanced frontend development)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/code-obfuscator.git
cd code-obfuscator
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Backend Server

```bash
python run.py
```

The backend will start at `http://127.0.0.1:5000/`.

### 4. Open the Frontend

Open `frontend/index.html` in your browser, or visit `http://127.0.0.1:5000/` if running via Flask.

---

## Quick Start

1. **Paste or write Python code** in the left panel.
2. **Enter a key** for obfuscation/deobfuscation (required).
3. Click **Obfuscate** to transform your code.
4. The **obfuscated code** appears in the right panel, and the **deobfuscation string** (Base64) is shown below.
5. To **deobfuscate**, paste the deobfuscation string and enter the key, then click **Deobfuscate**.
6. Use **Download** to save the output, or **Copy String** to copy the obfuscation string.

---

## Frontend Usage

- **Input Python Code:** Paste or type your code in the left textarea.
- **Obfuscation/Deobfuscation Key:** Enter a password/key. This is required for both obfuscation and deobfuscation.
- **Upload .py File:** Drag and drop or click to upload a Python file.
- **Output:** The right panel shows the obfuscated or deobfuscated code.
- **Deobfuscation String:** The Base64 string representing the obfuscated code and encrypted meta-data.
- **Copy String:** Copies the deobfuscation string to clipboard.
- **Download:** Downloads the output as a `.py` file.
- **Clear:** Clears all fields.
- **Toggle Output Edit:** Makes the output textarea editable or read-only.

---

## Backend API

### Obfuscate Endpoint

- **URL:** `/obfuscate`
- **Method:** `POST`
- **Request JSON:**
  ```json
  {
    "code": "<python_code>",
    "features": { ... },   // optional, see features endpoint
    "key": "<password>"
  }
  ```
- **Response JSON:**
  ```json
  {
    "obfuscated_code": "<base64_string>"
  }
  ```

### Deobfuscate Endpoint

- **URL:** `/deobfuscate`
- **Method:** `POST`
- **Request JSON:**
  ```json
  {
    "code": "<base64_string>",
    "key": "<password>"
  }
  ```
- **Response JSON:**
  ```json
  {
    "deobfuscated_code": "<python_code>"
  }
  ```

### Upload Endpoint

- **URL:** `/upload`
- **Method:** `POST`
- **Form Data:** `file` (Python file)
- **Response JSON:**
  ```json
  {
    "code": "<file_contents>"
  }
  ```

### Download Endpoint

- **URL:** `/download`
- **Method:** `POST`
- **Request JSON:**
  ```json
  {
    "code": "<python_code>",
    "filename": "output.py"
  }
  ```
- **Response:** File download.

### Features Endpoint

- **URL:** `/features`
- **Method:** `GET`
- **Response JSON:**
  ```json
  {
    "features": [
      "rename_identifiers",
      "encode_strings",
      "dead_code",
      "junk_code",
      "minify",
      "strip_comments"
    ]
  }
  ```

### Health Endpoint

- **URL:** `/health`
- **Method:** `GET`
- **Response JSON:**
  ```json
  {
    "status": "ok"
  }
  ```

---

## Obfuscation Pipeline

### Lexical Analysis

- **File:** `backend/obfuscator/lexer.py`
- **Function:** `tokenize_code(code)`
- **Purpose:** Tokenizes Python code using the built-in `tokenize` module for optional analysis or debugging.

### Syntax Analysis

- **File:** `backend/obfuscator/parser.py`
- **Function:** `parse_ast(code)`
- **Purpose:** Parses Python code into an AST using the `ast` module. Returns `None` if syntax error.

### AST Transformations

- **File:** `backend/obfuscator/transformer.py`
- **Classes/Functions:**
  - `IdentifierRenamer`: Renames all identifiers (variables, functions, classes) to random names.
  - `StringEncoder`: Encodes all string literals using Base64.
  - `insert_dead_code(tree)`: Adds unreachable code blocks.
  - `insert_junk_code(tree)`: Adds random, unused functions.
  - `minify_source(source)`: Removes comments, whitespace, and blank lines.
  - `strip_comments(source)`: Removes comments from source code.

### Code Generation

- **File:** `backend/obfuscator/generator.py`
- **Function:** `generate_obfuscated_code(source_code, features, key)`
- **Purpose:** Applies all transformations, encrypts meta-data, and returns a Base64-encoded payload.

### Meta Encryption

- **File:** `backend/utils.py`
- **Functions:**
  - `xor_encrypt(data, key)`: Simple XOR-based encryption.
  - `encrypt_meta(meta, key)`: Serializes and encrypts meta-data.
  - `decrypt_meta(enc_meta, key)`: Decrypts and deserializes meta-data.

### Deobfuscation Pipeline

- **File:** `backend/obfuscator/deobfuscator.py`
- **Function:** `deobfuscate_code(obfuscated_code, key)`
- **Purpose:** Decodes the Base64 payload, decrypts meta-data, and reverses all transformations to restore the original code.

---

## Frontend Code Walkthrough

### `frontend/index.html`

- **Layout:** Two panels (input and output) with key fields, upload zone, and action buttons.
- **Key Elements:**
  - `#codeInput`: Input textarea for Python code.
  - `#obfKey`, `#deobfKey`: Password fields for obfuscation/deobfuscation key.
  - `#deobfString`: Textarea for the obfuscation string (Base64).
  - `#output`: Output textarea for obfuscated/deobfuscated code.
  - `#uploadZone`, `#fileInput`: File upload controls.
  - `#copyDeobfBtn`, `#downloadBtn`, `#clearBtn`, `#toggleEditBtn`: Action buttons.
  - `#toast`: Toast notification area.

### `frontend/js/script.js`

- **Functions:**
  - `fetchObfuscate(code, features, key)`: Calls backend to obfuscate code.
  - `fetchDeobfuscate(obfString, key)`: Calls backend to deobfuscate code.
  - `obfuscateCode()`, `deobfuscateCode()`: Button handlers.
  - `handleFileUpload(file)`: Reads uploaded `.py` files.
  - `showToast(message, type)`: Shows notifications.
  - `toggleOutputEdit()`: Toggles output textarea editability.
  - Event listeners for drag-and-drop, copy, download, and clear actions.

### `frontend/js/api.js`

- **Legacy API functions** (now mostly replaced by logic in `script.js`).

### `frontend/css/styles.css`

- **Modern glassmorphism design** with responsive layout.
- **Custom styles** for panels, editors, buttons, upload zone, and notifications.

---

## Backend Code Walkthrough

### app.py

- **Flask app** serving both API and static frontend.
- **Endpoints:** `/obfuscate`, `/deobfuscate`, `/features`, `/health`, `/upload`, `/download`, `/`, and static files.
- **Handles:** File uploads, downloads, error handling, and CORS.

### obfuscator/lexer.py

- **Function:** `tokenize_code(code)`
- **Purpose:** Tokenizes Python code for analysis.

### obfuscator/parser.py

- **Function:** `parse_ast(code)`
- **Purpose:** Parses code into an AST, returns `None` on syntax error.

### obfuscator/transformer.py

- **Classes:**
  - `IdentifierRenamer`: Renames identifiers.
  - `StringEncoder`: Encodes string literals.
- **Functions:**
  - `insert_dead_code(tree)`: Adds unreachable code.
  - `insert_junk_code(tree)`: Adds random functions.
  - `minify_source(source)`: Minifies code.
  - `strip_comments(source)`: Removes comments.
  - `obfuscate_pipeline(code, features)`: Runs all transformations and returns obfuscated code and meta-data.
  - `deobfuscate_pipeline(code, meta)`: Reverses transformations using meta-data.

### obfuscator/generator.py

- **Function:** `generate_obfuscated_code(source_code, features, key)`
- **Purpose:** Runs the obfuscation pipeline, encrypts meta-data, and returns a Base64-encoded payload.

### obfuscator/deobfuscator.py

- **Function:** `deobfuscate_code(obfuscated_code, key)`
- **Purpose:** Decodes and decrypts the payload, then reverses all transformations.

### utils.py

- **Functions:**
  - `xor_encrypt(data, key)`: Simple XOR encryption.
  - `encrypt_meta(meta, key)`: Serializes and encrypts meta-data.
  - `decrypt_meta(enc_meta, key)`: Decrypts and deserializes meta-data.

---

## Security Considerations

- **Key Management:** The obfuscation/deobfuscation key is never stored. Losing the key means the code cannot be deobfuscated.
- **Encryption:** Uses simple XOR encryption for meta-data. For production, use a stronger encryption algorithm.
- **Obfuscation Limitations:** Obfuscation increases code complexity but does not guarantee absolute protection.
- **File Handling:** Uploaded files are read into memory and not stored on disk.

---

## Customization

- **Obfuscation Features:** Modify `features` in the frontend or backend to enable/disable specific transformations.
- **Transformation Logic:** Extend `transformer.py` to add more obfuscation techniques.
- **Frontend Design:** Customize `styles.css` for branding or layout changes.
- **API Integration:** Use the REST API for automation or integration with other tools.

---

## Troubleshooting

- **Syntax Errors:** Ensure your Python code is valid before obfuscation.
- **Key Errors:** Always use the same key for obfuscation and deobfuscation.
- **File Upload Issues:** Only `.py` files are supported.
- **Server Errors:** Check backend logs for detailed error messages.

---

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes.
4. Commit and push: `git push origin feature/your-feature`
5. Open a pull request.

---

## License

This project is unlicensed.

---

## Acknowledgements

- Python `ast` module documentation
- Flask and Flask-CORS
- [astor](https://github.com/berkerpeksag/astor) for AST to source code conversion
- OpenAI Copilot for code suggestions

---

## Detailed Code Reference

### 1. `backend/obfuscator/transformer.py`

#### IdentifierRenamer

- Renames all identifiers (variables, functions, classes) to random names.
- Maintains a mapping for deobfuscation.

#### StringEncoder

- Encodes all string literals using Base64.
- Stores original values for reversal.

#### Dead/Junk Code

- `insert_dead_code`: Adds unreachable code blocks.
- `insert_junk_code`: Adds random, unused functions.

#### Minification

- Removes comments, blank lines, and unnecessary whitespace.

#### Meta-data

- Stores mappings and encoded strings for full reversibility.

### 2. `backend/obfuscator/generator.py`

- Runs the obfuscation pipeline.
- Encrypts meta-data with the user key.
- Returns a Base64-encoded payload containing obfuscated code and encrypted meta.

### 3. `backend/obfuscator/deobfuscator.py`

- Decodes the payload.
- Decrypts meta-data using the key.
- Reverses all transformations to restore the original code.

### 4. `backend/utils.py`

- Provides simple XOR-based encryption for meta-data.
- Handles serialization and deserialization.

### 5. `frontend/js/script.js`

- Handles all frontend logic: API calls, file upload, copy/download, notifications, and UI state.

---

## Example Workflow

1. **Obfuscate Code**
   - Input:
     ```python
     def hello(name):
         print("Hello, " + name)
     ```
   - Key: `mysecret`
   - Output: Obfuscated code and a Base64 string.

2. **Deobfuscate Code**
   - Paste the Base64 string and enter the same key.
   - Output: Original code restored.

---

## FAQ

**Q:** Can I use this for commercial code protection?  
**A:** This tool is for educational and research purposes. For commercial use, consider professional obfuscators and legal protection.

**Q:** Is the obfuscation irreversible?  
**A:** No, as long as you have the key and the obfuscation string, you can fully restore the original code.

**Q:** What happens if I lose the key?  
**A:** The code cannot be deobfuscated without the key.

**Q:** Can I add more obfuscation techniques?  
**A:** Yes! Extend `transformer.py` with new AST transformations.

---

## Contact

For questions, suggestions, or contributions, open an issue or contact the maintainer.

---
