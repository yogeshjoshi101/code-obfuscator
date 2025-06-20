import ast
import random
import string
import base64
import re

def generate_random_name(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))

class IdentifierRenamer(ast.NodeTransformer):
    def __init__(self):
        self.mapping = {}
        self.reverse_mapping = {}

    def visit_FunctionDef(self, node):
        original = node.name
        if original not in self.mapping:
            new = generate_random_name()
            self.mapping[original] = new
            self.reverse_mapping[new] = original
        node.name = self.mapping[original]
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        original = node.name
        if original not in self.mapping:
            new = generate_random_name()
            self.mapping[original] = new
            self.reverse_mapping[new] = original
        node.name = self.mapping[original]
        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Store, ast.Load, ast.Del)):
            if node.id not in self.mapping and not node.id.startswith('__'):
                new = generate_random_name()
                self.mapping[node.id] = new
                self.reverse_mapping[new] = node.id
            if node.id in self.mapping:
                node.id = self.mapping[node.id]
        return node

class StringEncoder(ast.NodeTransformer):
    def __init__(self):
        self.encoded_strings = {}

    def visit_Constant(self, node):
        if isinstance(node.value, str):
            encoded = base64.b64encode(node.value.encode('utf-8')).decode('utf-8')
            self.encoded_strings[encoded] = node.value
            node.value = encoded
        return node

    def visit_Str(self, node):
        encoded = base64.b64encode(node.s.encode('utf-8')).decode('utf-8')
        self.encoded_strings[encoded] = node.s
        node.s = encoded
        return node

def decode_strings_in_source(source, encoded_strings):
    for encoded, original in encoded_strings.items():
        source = source.replace(f'"{encoded}"', f'"{original}"').replace(f"'{encoded}'", f"'{original}'")
    return source

def insert_dead_code(tree):
    dead_code = ast.parse("if False:\n    print('dead code')\n")
    if isinstance(tree, ast.Module):
        tree.body = [dead_code.body[0]] + tree.body
    return tree

def remove_dead_code_from_source(source):
    return re.sub(r"if False:\s*print\(['\"]dead code['\"]\)\s*", "", source)

def minify_source(source):
    # Remove comments
    source = re.sub(r'#.*', '', source)
    # Remove blank lines
    source = re.sub(r'\n\s*\n', '\n', source)
    # Remove leading/trailing whitespace
    source = '\n'.join(line.rstrip() for line in source.splitlines())
    # Remove unnecessary spaces
    source = re.sub(r'[ \t]+', ' ', source)
    return source.strip()

def deminify_source(source):
    # Not fully reversible, but just for demonstration
    return source

def insert_junk_code(tree):
    # Insert a dummy function as junk code
    junk_func = ast.parse("def {}():\n    return {}".format(
        generate_random_name(), random.randint(0, 10000)
    ))
    if isinstance(tree, ast.Module):
        tree.body.append(junk_func.body[0])
    return tree

def strip_comments(source):
    return re.sub(r'#.*', '', source)

def obfuscate_pipeline(code, features=None):
    features = features or {
        "rename_identifiers": True,
        "encode_strings": True,
        "dead_code": True,
        "junk_code": True,
        "minify": True,
        "strip_comments": True
    }
    tree = ast.parse(code)
    meta = {}

    if features.get("rename_identifiers"):
        renamer = IdentifierRenamer()
        tree = renamer.visit(tree)
        ast.fix_missing_locations(tree)
        meta['identifier_mapping'] = renamer.reverse_mapping

    if features.get("encode_strings"):
        encoder = StringEncoder()
        tree = encoder.visit(tree)
        ast.fix_missing_locations(tree)
        meta['encoded_strings'] = encoder.encoded_strings

    if features.get("dead_code"):
        tree = insert_dead_code(tree)

    if features.get("junk_code"):
        tree = insert_junk_code(tree)

    import astor
    source = astor.to_source(tree)

    if features.get("strip_comments"):
        source = strip_comments(source)
    if features.get("minify"):
        source = minify_source(source)

    return source, meta

def deobfuscate_pipeline(code, meta):
    code = deminify_source(code)
    code = remove_dead_code_from_source(code)
    code = decode_strings_in_source(code, meta.get('encoded_strings', {}))
    for obf, orig in meta.get('identifier_mapping', {}).items():
        code = code.replace(obf, orig)
    return code
