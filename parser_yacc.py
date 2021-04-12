from ply import yacc
from lexer_lex import tokens
from constructs.ast import BinOP, Literal
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
             | MY VARNAME EQ EXPR SEMI
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

def p_identifier_types(p):
    """
    identifier_types : VARNAME INDEXOP NUMBER INDEXCL
                    | VARNAME INDEXOP VARNAME INDEXCL
                    | VARNAME
                    | NUMBER
                    | STRING
    """
    if (len(p) == 2):
        cprint("Identifier", p.lineno(1), p.lineno(1))
        if ('$' in p):
            p[0] = Literal("variable", p[1])
        elif(r'[0-9]' in p):
            p[0] = Literal("number", p[1])
        else:
            p[0] = Literal("string", p[1])
    else:
        cprint("Identifier", p.lineno(1), p.lineno(1))

def p_var_op(p):
    """
    var_op : identifier_types EQ identifier_types SEMI
           | identifier_types EQ expr SEMI
           | identifier_types INCREMENT SEMI
           | identifier_types DECREMENT SEMI
           | INCREMENT identifier_types
           | DECREMENT identifier_types
    """
    if('=' in p):
        cprint("Variable reassignment", p.lineno(1), p.lineno(4))
    elif('++' in p):
        cprint("Variable increment", p.lineno(1), p.lineno(3))
    elif('--' in p):
        cprint("Variable decrement", p.lineno(1), p.lineno(3))

def p_until(p):
    """
    until : UNTIL OP relational_expression CL BLOCKOP block BLOCKCL 
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
    handle_types : identifier_types COMMA handle_types
                 | identifier_types  
    """
    pass

def p relational_expr(p):
    """
 relational_expr : identifier_types GT identifier_types
                 | identifier_types LT identifier_types
                 | identifier_types EQ EQ identifier_types
                 | identifier_types GT EQ identifier_types
                 | identifier_types LT EQ identifier_types
    """
    if (len(p) == 2):
        cprint("expr", p.lineno(1), p.lineno(1))
    elif(len(p) == 4):
        cprint("expr", p.lineno(1), p.lineno(3))
    elif (len(p) == 5):
        cprint("expr", p.lineno(1), p.lineno(4))
    else:
        print("expr")

def p_logical_expr(p):
    """
    logical_expr : logical_bin_expr AND identifier_types
                 | logical_bin_expr AND logical_bin_expr
                 | logical_bin_expr OR identifier_types
                 | logical_bin_expr OR logical_bin_expr
                 | logical_bin_expr NOT logical_bin_expr
                 | logical_bin_expr NOT identifier_types
                 | empty
    """
    pass

def p_logical_bin_expr(p):
    """
    logical_bin_expr : identifier_types AND identifier_types
                     | identifier_types OR identifier_types
                     | identifier_types NOT identifier_types
    """

def p_expr(p):
    """
    expr : expr_bin PLS identifier_types
         | expr_bin MIN identifier_types
         | expr_bin DIV identifier_types
         | expr_bin MUL identifier_types
         | expr_bin PLS expr_bin
         | expr_bin MIN expr_bin
         | expr_bin DIV expr_bin
         | expr_bin MUL expr_bin
         | expr_bin
         | empty
    """
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 4):
        p[0] = BinOP(p[2], left = p[1], right = p[3])

def p_expr_bin_op(p):
    """
    expr_bin : identifier_types PLS identifier_types
          | identifier_types MIN identifier_types
          | identifier_types DIV identifier_types
          | identifier_types MUL identifier_types
    """
    cprint("binary operation", p.lineno(1), p.lineno(1))
    p[0] = BinOP(p[2], left = p[1], right=p[3])
    # p[0] = Node("assignment", [p[1]])
    # p[0] = Node( relational", [p[1]])

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
        
def 