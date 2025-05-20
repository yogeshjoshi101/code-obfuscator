# Advanced Code Obfuscator & De-Obfuscator

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Workflow](#workflow)
5. [Implementation Details](#implementation-details)
6. [Codebase Structure](#codebase-structure)
7. [API Reference](#api-reference)
8. [Testing and Validation](#testing-and-validation)
9. [Deployment](#deployment)
10. [Contributing](#contributing)
11. [License](#license)

---

## Introduction

The *Advanced Code Obfuscator & De-Obfuscator* is a professional-grade, compiler-based tool designed to enhance the security of Python source code. It transforms readable code into an obfuscated form that is difficult to reverse-engineer, while retaining its original functionality. This project addresses the growing need for intellectual property protection in software development by providing a secure, scalable, and user-friendly solution for code transformation.

---

## Features

- *AST-Based Obfuscation:* Uses Abstract Syntax Tree (AST) transformations for robust code obfuscation.
- *Dead Code Insertion:* Randomly inserts non-functional code to confuse reverse engineers.
- *String Literal Encoding:* Encodes string literals using Base64 and decodes them at runtime.
- *Advanced Variable & Function Renaming:* Renames variables and functions to random, non-meaningful names.
- *Comment Removal/Insertion:* Optionally removes or inserts misleading comments.
- *Base64 Encoding:* Provides an additional layer of security by encoding the obfuscated code.
- *Security Key Mechanism:* Generates a unique key for each obfuscation, required for de-obfuscation.
- *Mapping System:* Securely stores the mapping between original and obfuscated code.
- *Web-Based Interface:* User-friendly frontend for code upload, obfuscation, and de-obfuscation.
- *Modular & Extensible:* Designed for easy extension and collaborative development.

---

## System Architecture

### High-Level Design

The system is modular and consists of the following components:

- *Frontend:*  
  - Static web interface (HTML/CSS/JS) for user interaction.
  - Allows users to input code, view obfuscated/encoded results, and manage security keys.

- *Backend:*  
  - Flask-based Python application.
  - Handles code obfuscation, de-obfuscation, and mapping management.

- *Mapping System:*  
  - JSON-based storage for mapping security keys to original code.

- *Security Key Mechanism:*  
  - Ensures only authorized users can de-obfuscate code.

### Architecture Diagram


+-----------+        +-----------+        +-------------------+
| Frontend  | <----> |  Backend  | <----> |  Mapping System   |
+-----------+        +-----------+        +-------------------+


---

## Workflow

### Obfuscation Process

1. User submits Python code via the web interface.
2. Backend performs:
   - Lexical analysis (tokenization).
   - Parsing to AST.
   - AST transformations (obfuscation, dead code, string encoding, renaming).
   - Code generation (obfuscated code).
   - Base64 encoding (optional, for extra security).
3. Backend returns:
   - Obfuscated code (readable, but obfuscated).
   - Obfuscated + encoded code (not directly readable/executable).
   - Security key for de-obfuscation.
4. User can copy/download both outputs.

### De-Obfuscation Process

1. User submits the encoded code and security key via the web interface.
2. Backend retrieves the original code using the security key from the mapping system.
3. Backend returns the original source code.

---

## Implementation Details

### Backend

- *Framework:* Flask (with Flask-CORS for cross-origin requests)
- *Modules:*
  - *Lexer:* Tokenizes input code.
  - *Parser:* Converts code to AST.
  - *Transformer:* Applies obfuscation (variable renaming, dead code, string encoding).
  - *Generator:* Converts AST back to code, handles encoding.
  - *De-Obfuscator:* Retrieves original code using the mapping and security key.
  - *Utils:* Handles mapping storage and retrieval.

### Frontend

- *Technologies:* HTML, CSS, JavaScript
- *Features:*
  - Code input area.
  - Buttons for obfuscation and de-obfuscation.
  - Separate outputs for obfuscated and obfuscated+encoded code.
  - Security key management.

### Mapping System

- *Storage:* JSON file (code_mapping.json)
- *Function:* Maps security keys to original code for secure retrieval.

### Key Libraries

- Flask, Flask-CORS: Backend web framework and CORS support.
- astor: AST manipulation and code generation.
- uuid: Unique security key generation.
- base64: String and code encoding.

---

## Codebase Structure


code-obfuscator-main/
│
├── backend/
│   ├── app.py                # Flask application
│   ├── obfuscator/
│   │   ├── lexer.py          # Lexical analysis
│   │   ├── parser.py         # AST parsing
│   │   ├── transformer.py    # AST transformations (obfuscation)
│   │   ├── generator.py      # Code generation and encoding
│   │   ├── deobfuscator.py   # De-obfuscation logic
│   │   └── __init__.py
│   └── utils.py              # Utility functions (mapping)
│
├── frontend/
│   ├── index.html            # Web interface
│   ├── css/
│   │   └── styles.css        # Styling
│   └── js/
│       ├── script.js         # UI logic
│       └── api.js            # API calls
│
├── code_mapping.json         # JSON file for mapping
├── requirements.txt          # Python dependencies
├── run.py                    # Entry point for the application
├── .gitignore                # Git ignore file
└── docs/
    └── README.md             # Documentation


---

## API Reference

### POST /obfuscate

- *Request:*  
  json
  { "code": "<python_source_code>" }
  
- *Response:*  
  json
  {
    "obfuscated_code": "<obfuscated_python_code>",
    "obfuscated_encoded_code": "<base64_encoded_obfuscated_code>",
    "security_key": "<security_key>"
  }
  

### POST /deobfuscate

- *Request:*  
  json
  {
    "code": "<obfuscated_encoded_code>",
    "security_key": "<security_key>"
  }
  
- *Response:*  
  json
  {
    "deobfuscated_code": "<original_python_code>"
  }
  

---

## Testing and Validation

- *Unit Testing:*  
  - Each module (lexer, parser, transformer, generator, deobfuscator, utils) is unit tested.
  - Achieved high test coverage.

- *Integration Testing:*  
  - Verified seamless communication between frontend and backend.

- *Edge Case Testing:*  
  - Tested with large files, complex code structures, and various Python constructs.

- *Security Validation:*  
  - Validated security key mechanism and mapping file integrity.

---

## Deployment

- *Platform:* Cloud-based hosting (e.g., AWS, Azure, Heroku)
- *Steps:*
  1. Containerize the application using Docker.
  2. Deploy the container to the chosen cloud platform.
  3. Configure secure API hosting with HTTPS.
  4. Set up environment variables and persistent storage for mappings.

---

## Contributing

Contributions are welcome!  
- Please fork the repository and submit pull requests.
- Follow PEP8 coding standards and write clear docstrings/comments.
- Add tests for new features and bug fixes.

---

## License  
See [LICENSE](../LICENSE) for details.

---
