from ply import yacc
from lexer_lex import tokens
from constructs.ast import Node
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
            | var_op 
            | until
            | foreach
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
             | MY ARRNAME EQ OP handle_types CL SEMI
    """
    if (len(p) == 4):
        cprint("array declaration", p.lineno(1), p.lineno(3))
    elif (len(p) == 8):
        cprint("array declaration", p.lineno(1), p.lineno(7))
    else:
        print("array declaration", p.lineno(1), len(p) )

def p_var_op(p):
    """
    var_op : VARNAME INDEXOP NUMBER INDEXCL EQ STRING SEMI
           | VARNAME INDEXOP NUMBER INDEXCL EQ NUMBER SEMI
           | VARNAME INDEXOP VARNAME INDEXCL EQ STRING SEMI
           | VARNAME INDEXOP VARNAME INDEXCL EQ NUMBER SEMI
           | VARNAME EQ STRING SEMI
           | VARNAME EQ NUMBER SEMI
           | VARNAME INDEXOP NUMBER INDEXCL INCREMENT SEMI
           | VARNAME INDEXOP VARNAME INDEXCL INCREMENT SEMI
           | VARNAME INCREMENT SEMI
           | VARNAME INDEXOP NUMBER INDEXCL DECREMENT SEMI
           | VARNAME INDEXOP VARNAME INDEXCL DECREMENT SEMI
           | VARNAME DECREMENT SEMI
           | INCREMENT VARNAME INDEXOP NUMBER INDEXCL SEMI
           | INCREMENT VARNAME INDEXOP VARNAME INDEXCL SEMI
           | DECREMENT VARNAME INDEXOP NUMBER INDEXCL SEMI
           | DECREMENT VARNAME INDEXOP VARNAME INDEXCL SEMI
           | INCREMENT VARNAME SEMI
           | DECREMENT VARNAME SEMI
    """
    if('=' in p):
        cprint("Variable reassignment", p.lineno(1), p.lineno(4))
    elif('++' in p):
        cprint("Variable increment", p.lineno(1), p.lineno(3))
    elif('--' in p):
        cprint("Variable decrement", p.lineno(1), p.lineno(3))

def p_until(p):
    """
    until : UNTIL OP logical_expr CL BLOCKOP block BLOCKCL 
    """
    cprint("until block", p.lineno(1), p.lineno(7))
    
def p_foreach(p):
    """
    foreach : FOREACH OP ARRNAME CL BLOCKOP block BLOCKCL
            | FOREACH OP handle_types CL BLOCKOP block BLOCKCL
    """
    cprint("foreach block", p.lineno(1), p.lineno(7))

def p_block(p):
    """
    block : block command
          | empty
    """
    pass

def p_print(p):
    """
    print : PRINT handle_types SEMI
    """
    cprint("print statement", p.lineno(1), p.lineno(3))

def p_handle_types(p):
    """
    handle_types : VARNAME INDEXOP NUMBER INDEXCL COMMA handle_types
             | VARNAME INDEXOP VARNAME INDEXCL COMMA handle_types
             | STRING COMMA handle_types
             | VARNAME COMMA handle_types
             | NUMBER COMMA handle_types
             | FLOAT COMMA handle_types
             | VARNAME INDEXOP NUMBER INDEXCL
             | VARNAME INDEXOP VARNAME INDEXCL
             | VARNAME 
             | NUMBER 
             | FLOAT 
             | STRING  
    """
    pass

def p_logical_expr(p):
    """
    logical_expr : VARNAME GT NUMBER
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
         | VARNAME INDEXOP NUMBER INDEXCL GT NUMBER
         | VARNAME INDEXOP NUMBER INDEXCL LT NUMBER
         | VARNAME INDEXOP NUMBER INDEXCL EQ EQ NUMBER
         | VARNAME INDEXOP NUMBER INDEXCL GT EQ NUMBER
         | VARNAME INDEXOP NUMBER INDEXCL LT EQ NUMBER
         | VARNAME INDEXOP NUMBER INDEXCL GT VARNAME
         | VARNAME INDEXOP NUMBER INDEXCL LT VARNAME
         | VARNAME INDEXOP NUMBER INDEXCL EQ EQ VARNAME
         | VARNAME INDEXOP NUMBER INDEXCL GT EQ VARNAME
         | VARNAME INDEXOP NUMBER INDEXCL LT EQ VARNAME
         | VARNAME INDEXOP NUMBER INDEXCL LT VARNAME INDEXOP NUMBER INDEXCL
         | VARNAME INDEXOP NUMBER INDEXCL GT VARNAME INDEXOP NUMBER INDEXCL
         | VARNAME INDEXOP NUMBER INDEXCL EQ EQ VARNAME INDEXOP NUMBER INDEXCL
         | VARNAME INDEXOP NUMBER INDEXCL LT EQ VARNAME INDEXOP NUMBER INDEXCL
         | VARNAME INDEXOP NUMBER INDEXCL GT EQ VARNAME INDEXOP NUMBER INDEXCL
    """
    if (len(p) == 2):
        cprint("expr", p.lineno(1), p.lineno(1))
    elif(len(p) == 4):
        cprint("expr", p.lineno(1), p.lineno(3))
    elif (len(p) == 5):
        cprint("expr", p.lineno(1), p.lineno(4))
    else:
        print("expr")

def p_var_const(p):
    """
    var_const: VARNAME
         | VARNAME INDEXOP NUMBER INDEXCL
         | NUMBER
         | STRING
    """
    pass
        
def p_expr_bin_op(p):
    """
    expr: var_const PLUS var_const
          | var_const MIN var_const
          | var_const DIV var_const
          | var_const MUL var_const
    """
    p[0] = Node("binop", [p[1], p[3]], p[2])

def p_empty(p):
    """
    empty :
    """
    pass

def p_error(p):
    print("syntax error", p.lineno)


if __name__ == "__main__":
    parser = yacc.yacc(debug=True)
    with open(sys.argv[1], "rt") as f:
        result = parser.parse(f.read())
        print(result)
        
