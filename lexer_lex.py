import ply.lex as lex

# list of reserved tokens
reserved = {
    'if': 'IF',
    'use': 'USE',
    'print': 'PRINT',
    'my' : 'MY',
    'until' : 'UNTIL',
    'foreach' : 'FOREACH'
}

# list of token names
tokens = (
    "NUMBER",
    "STRING",
    "SEMI",
    "ID",
    "VARNAME",
    "ARRNAME",
    "LT",
    "GT",
    "OP",
    "CL",
    "INDEXOP",
    "INDEXCL",
    "BLOCKOP",
    "BLOCKCL",
    "COMMA",
    "EQ",
    "INCREMENT",
    "DECREMENT",
    "PLS",
    "MIN",
    "MUL",
    "DIV",
    "COMMENT",
    "AND",
    "OR",
    "NOT"
) + tuple(reserved.values())

# list of possible states
# states = (
#         ('code', 'exclusive')
# )

# specifying regex for simple tokens
# t_PLUS = r'\+'
t_MIN = r'\-'
t_MUL = r'\*'
t_DIV = r'/'
t_SEMI = r'\;'
t_LT = r'\<'
t_GT = r'\>'
t_EQ = r'\='
t_OP = r'\('
t_CL = r'\)'
t_INDEXOP = r'\['
t_INDEXCL = r'\]'
t_BLOCKOP = r'\{'
t_BLOCKCL = r'\}'
t_COMMA = r'\,'
t_STRING = r'\".*\"'
t_NOT = r'NOT'
# regex rules + other actions

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

def t_newline(t):
    r'\n'
#    print("t.value =", len(t.value))
    t.lexer.lineno += len(t.value)

t_ignore = '\t '

def t_error(t):
    print("Illegal character '%s'"%t.value[0])
    t.lexer.skip(1)

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_VARNAME(t):
    r'\$[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_PLS(t):
    r'\+'
    return t

def t_ARRNAME(t):
    r'\@[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_INCREMENT(t):
    r'(\++)'
    return t

def t_DECREMENT(t):
    r'(\--)'
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_AND(t):
    r'(\and|&&)'
    return t

def t_OR(t):
    r'(/or|\|\|)'
    return t

if __name__ == "__main__":
    lexer = lex.lex()
    data = None
    with open("test.pl", encoding = 'utf-8') as f:
        data = f.read()
    
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok.type, tok.value, tok.lineno, tok.lexpos)
