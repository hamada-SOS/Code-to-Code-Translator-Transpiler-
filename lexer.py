import re

token_specification = [
    ('NUMBER',   r'\d+'),
    ('PRINT',    r'PRINT'),
    ('READSTR',  r'READSTR'),
    ('READ',     r'READ'),
    ('FOR',      r'FOR'),
    ('FROM',     r'FROM'),
    ('TO',       r'TO'),
    ('ENDWHILE', r'END[ \t]+WHILE'),
    ('END',      r'END'),
    ('WHILE',    r'WHILE'),
    ('IF',       r'IF'),
    ('ELSE',     r'ELSE'),
    ('SET',      r'SET'),
    ('OP',       r'==|!=|<=|>=|[+\-*/<>%]'),
    ('EQ',       r'='),
    ('ID',       r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('STRING',   r'"[^"]*"'),
    ('NEWLINE',  r'\n'),
    ('SKIP',     r'[ \t]+'),
    ('MISMATCH', r'.'),
]

tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

def tokenize(code):
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            yield ('NUMBER', int(value))
        elif kind in ('PRINT', 'READ', 'READSTR', 'FOR', 'FROM', 'TO', 'ENDWHILE', 'WHILE', 'END', 'IF', 'ELSE', 'SET') or kind == 'ID':
            yield (kind, value)
        elif kind == 'STRING':
            yield ('STRING', value.strip('"'))
        elif kind in ('OP', 'EQ'):
            yield (kind, value)
        elif kind in ('NEWLINE', 'SKIP'):
            continue
        else:
            raise SyntaxError(f"Unexpected character: {value}")
