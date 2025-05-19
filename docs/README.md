# Advanced Code Obfuscator & De-Obfuscator

This project uses compiler design principles:
- **Lexical Analysis:** Tokenizes source code.
- **Syntax Analysis:** Parses the code into an AST.
- **Code Transformation:** Applies obfuscation via AST transformation.
- **Code Generation:** Converts the AST back to source code and Base64 encodes it.
- **De-Obfuscation:** Decodes the Base64 to retrieve the obfuscated code.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
