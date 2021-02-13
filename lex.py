import ply.lex as lex

# list of reserved tokens
reserved = {
    'if': 'IF',
    'use': 'USE',
    'print': 'PRINT',
    'my' : 'MY',
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
    "BLOCKOP",
    "BLOCKCL",
    "COMMA",
    "EQ",
    "PLS",
    "MIN",
    "MUL",
    "DIV",
    "COMMENT",
) + tuple(reserved.values())

# list of possible states
states = (
        ('code', 'exclusive')
)

# specifying regex for simple tokens
t_PLS = r'\+'
t_MIN = r'\-'
t_MUL = r'\*'
t_DIV = r'/'
t_SEMI = r'\;'
t_LT = r'\<'
t_GT = r'\>'
t_EQ = r'\='
t_OP = r'\('
t_CL = r'\)'
# t_BLOCKOP = r'\{'
# t_BLOCKCL = r'\}'
t_COMMA = r'\,'
t_STRING = r'\".*\"'

# regex rules + other actions
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n'
    t.lexer.lineno += len(t.value)

t_ignore = '\t '

def t_error(t):
    print("Illegal character '%s'"%t.value[0])

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_VARNAME(t):
    r'\$[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_ARRNAME(t):
    r'\@[a-zA-Z_][a-zA-Z_0-9]*'
    return t


def t_COMMENT(t):
    r'\#.*'
    pass

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
