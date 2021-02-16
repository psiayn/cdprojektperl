from ply import yacc
from lexer import tokens
import sys

def cprint(ptype: str, start: int, end: int ):
    print("<",ptype,", ", start, ", ", end,">", sep="")

def p_start(p):
    """
    start : start command
          | empty
    """
    pass

def p_command(p):
    """
    command : use 
            | print 
            | var_decl 
            | arr_decl 
            | until
    """
    pass

def p_use(p):
    """
    use : USE ID SEMI
    """
    cprint("use statement", p.lineno(1), p.lineno(3))

def p_var_decl(p: yacc.YaccProduction):
    """
    var_decl : MY VARNAME SEMI
             | MY VARNAME EQ STRING SEMI
             | MY VARNAME EQ NUMBER SEMI
    """
    if (len(p) == 4):
        cprint("variable declaration", p.lineno(1), p.lineno(3))
    elif (len(p) == 6):
        cprint("variable declaration", p.lineno(1), p.lineno(5))
    else:
        print("variable declaration", p.lineno(1))

def p_arr_decl(p):
    """
    arr_decl : MY ARRNAME SEMI
             | MY ARRNAME EQ OP array_init CL SEMI
    """
    if (len(p) == 4):
        cprint("array declaration", p.lineno(1), p.lineno(3))
    elif (len(p) == 8):
        cprint("array declaration", p.lineno(1), p.lineno(7))
    else:
        print("array declaration", p.lineno(1), len(p) )

def p_array_init(p):
    """
    array_init : STRING COMMA array_init
               | NUMBER COMMA array_init
               | STRING 
               | NUMBER
    """
    pass

def p_until(p):
    """
    until : UNTIL OP expr CL BLOCKOP block BLOCKCL 
    """
    cprint("until block", p.lineno(1), p.lineno(7))
    

def p_block(p):
    """
    block : block command
          | empty
    """
    pass
    
def p_print(p):
    """
    print : PRINT STRING SEMI
         | PRINT NUMBER SEMI
    """
    cprint("print statement", p.lineno(1), p.lineno(3))

def p_expr(p):
    """
    expr : VARNAME GT NUMBER
         | VARNAME LT NUMBER
         | VARNAME EQ EQ NUMBER
         | VARNAME GT EQ NUMBER
         | VARNAME LT EQ NUMBER
         | VARNAME EQ EQ VARNAME
         | VARNAME EQ EQ STRING
         | VARNAME GT EQ VARNAME
         | VARNAME LT EQ VARNAME
         | VARNAME GT VARNAME
         | VARNAME LT VARNAME
         | VARNAME
         | NUMBER GT NUMBER
         | NUMBER LT NUMBER
         | NUMBER EQ EQ NUMBER
         | NUMBER GT EQ NUMBER
         | NUMBER LT EQ NUMBER
         | STRING EQ EQ NUMBER
    """
    if (len(p) == 2):
        cprint("expr", p.lineno(1), p.lineno(1))
    elif(len(p) == 4):
        cprint("expr", p.lineno(1), p.lineno(3))
    elif (len(p) == 5):
        cprint("expr", p.lineno(1), p.lineno(4))
    else:
        print("expr")

    
def p_empty(p):
    """
    empty :
    """
    pass

def p_error(p):
    print("syntax error", p.lineno)

parser = yacc.yacc(debug=True)

if __name__ == "__main__":
    with open(sys.argv[1], "rt") as f:
        result = parser.parse(f.read())
        print(result)
        
