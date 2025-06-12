import re

token_specification = [
    ('NUMBER',   r'\d+'),
    ('PRINT',    r'PRINT'),
    ('READSTR',  r'READSTR'),
    ('READ',     r'READ'),
    ('FOR',      r'FOR'),
    ('FROM',     r'FROM'),
    ('TO',       r'TO'),
    ('END',      r'END'),
    ('IF',       r'IF'),
    ('ELSE',     r'ELSE'),
    ('SET',      r'SET'),
    ('EQ',       r'='),
    ('OP',       r'[+\-*/<>]'),
    ('ID',       r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('STRING',   r'\"[^\"]*\"'),
    ('NEWLINE',  r'\n'),
    ('SKIP',     r'[ \t]+'),
    ('MISMATCH', r'.'),
]

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

def tokenize(code):
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            yield ('NUMBER', int(value))
        elif kind in ('PRINT', 'READ', 'READSTR', 'FOR', 'FROM', 'TO', 'END', 'IF', 'ELSE', 'SET') or kind == 'ID':
            yield (kind, value)
        elif kind == 'STRING':
            yield ('STRING', value.strip('"'))
        elif kind == 'EQ':
            yield ('EQ', value)
        elif kind == 'OP':
            yield ('OP', value)
        elif kind == 'NEWLINE' or kind == 'SKIP':
            continue
        else:
            raise SyntaxError(f"Unexpected character: {value}")
