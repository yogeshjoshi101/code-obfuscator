import tokenize
from io import BytesIO

def tokenize_code(code):
    """Tokenizes the Python source code into a list of tokens."""
    tokens = []
    try:
        token_stream = tokenize.tokenize(BytesIO(code.encode('utf-8')).readline)
        for tok in token_stream:
            # Skip the encoding token
            if tok.type != tokenize.ENCODING:
                tokens.append((tok.type, tok.string))
    except tokenize.TokenError:
        return None
    return tokens
