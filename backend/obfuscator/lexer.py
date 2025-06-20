import tokenize
from io import BytesIO

def tokenize_code(code):
    """
    Tokenizes the Python source code into a list of tokens using the built-in tokenize module.
    Returns a list of (type, string, start, end, line) tuples.
    """
    tokens = []
    try:
        token_stream = tokenize.tokenize(BytesIO(code.encode('utf-8')).readline)
        for tok in token_stream:
            if tok.type == tokenize.ENCODING:
                continue
            tokens.append((tokenize.tok_name.get(tok.type, tok.type), tok.string, tok.start, tok.end, tok.line))
    except tokenize.TokenError:
        return None
    return tokens
