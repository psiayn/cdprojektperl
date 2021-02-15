from ply import yacc
from lexer import tokens
import sys

def cprint(ptype: str, line_start: int, line_end: int, pos_start: int, pos_end: int):
    print("<",ptype,", (",line_start, ",", line_end,"), (",pos_start, ",", pos_end,")>")

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
    cprint("use statement", p.lineno(1), p.lineno(3), p.lexpos(1), p.lexpos(3))

def p_var_decl(p):
    """
    var_decl : MY VARNAME SEMI
             | MY VARNAME EQ STRING SEMI
             | MY VARNAME EQ NUMBER SEMI
    """
    cprint("variable declaration")

def p_arr_decl(p):
    """
    arr_decl : MY ARRNAME SEMI
             | MY ARRNAME EQ OP array_init CL SEMI
    """
    cprint(p, "array declaration")

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
    until : UNTIL OP expr CL BLOCKOP command BLOCKCL
    """
    cprint(p, "until block")

    
def p_print(p):
    """
    print : PRINT STRING SEMI
         | PRINT NUMBER SEMI
    """
    cprint(p, "print statement")

def p_expr(p):
    """
    expr : VARNAME GT NUMBER
         | VARNAME LT NUMBER
         | VARNAME EQ EQ NUMBER
         | VARNAME GT EQ NUMBER
         | VARNAME LT EQ NUMBER
         | VARNAME EQ EQ VARNAME
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
    cprint(p, "expr")
    
def p_empty(p):
    """
    empty :
    """
    pass

def p_error(p):
    print("syntax error")

parser = yacc.yacc(debug=True)

if __name__ == "__main__":
    with open(sys.argv[1], "rt") as f:
        result = parser.parse(f.read())
        print(result)
        
