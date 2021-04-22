from ply import yacc, lex
import lexer_lex
from lexer_lex import tokens
from constructs.ast import *
from constructs.symbol_table import SymbolTable
from constructs.ast_vis import draw_AST
import icg
import sys

symtab = SymbolTable()
start_ast = Node("start", children=[])

def cprint(ptype: str, start: int, end: int ):
    print("<",ptype,", ", start, ", ", end,">", sep="")

def p_start(p):
    """
    start : start command
          | empty
    """
    if (len(p) != 2):
        start_ast.children.append(p[2])

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
    p[0] = p[1]

def p_use(p):
    """
    use : USE ID SEMI
    """
    p[0] = Use(p[2])
    cprint("use statement", p.lineno(1), p.lineno(3))

def p_var_decl(p: yacc.YaccProduction):
    """
    var_decl : MY VARNAME SEMI
             | MY VARNAME EQ STRING SEMI
             | MY VARNAME EQ NUMBER SEMI
    """
    if (len(p) == 4):
        symtab.add_if_not_exists(p[2][0])
        p[0] = Decleration(p[2][0])
        cprint("variable declaration", p.lineno(1), p.lineno(3))
    elif (len(p) == 6):
        symtab.add_if_not_exists(p[2][0])
        symtab.get_symbol(p[2][0]).value = p[4][0]
        p[0] = Decleration(p[2][0], p[4][0])
        cprint("variable declaration", p.lineno(1), p.lineno(5))
    symtab.get_symbol(p[2][0]).lineno = p.lineno(2)

def p_arr_decl(p):
    """
    arr_decl : MY ARRNAME SEMI
             | MY ARRNAME EQ OP handle_types CL SEMI
    """
    if (len(p) == 4):
        symtab.add_if_not_exists(p[2])
        p[0] = Array(p[2])
        cprint("array declaration", p.lineno(1), p.lineno(3))
    elif (len(p) == 8):
        symtab.add_if_not_exists(p[2])
        symtab.get_symbol(p[2]).value = p[5]
        p[0] = Array(p[2], data=p[5])
        cprint("array declaration", p.lineno(1), p.lineno(7))
    symtab.get_symbol(p[2]).lineno = p.lineno(2)

def p_identifier_types(p):
    """
    identifier_types : VARNAME INDEXOP NUMBER INDEXCL
                    | VARNAME INDEXOP VARNAME INDEXCL
                    | VARNAME
                    | NUMBER
                    | STRING
    """
    symbol = symtab.get_symbol(p[1][0])
    if (len(p) == 2):
        cprint("Identifier", p.lineno(1), p.lineno(1))
        if (p[1][1] == "VARNAME"):
            if (symbol is None):
                print("Variable accessed before declaration.")
            else:
                print(symbol)
            p[0] = Literal("variable", p[1][0])
        elif(p[1][1] == "NUMBER"):
            p[0] = Literal("number", p[1][0])
        else:
            p[0] = Literal("string", p[1][0])
    else:
        if (symbol is None):
            print("Array used before declaration.")
        else:
            print(symbol)
        p[0] = Array(p[1][0], index=p[3][0])
        cprint("Array", p.lineno(1), p.lineno(1))

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
        p[0] = BinOP('=', p[1], p[3])
        cprint("Variable reassignment", p.lineno(1), p.lineno(4))
    elif('++' in p):
        cprint("Variable increment", p.lineno(1), p.lineno(3))
        if ( '+' in p[1] ):
            p[0] = BinOP('++', right=p[2])
        else:
            p[0] = BinOP('++', left=p[2])

    elif('--' in p):
        cprint("Variable decrement", p.lineno(1), p.lineno(3))
        if ( '-' in p[1] ):
            p[0] = BinOP('--', right=p[2])
        else:
            p[0] = BinOP('--', left=p[2])

def p_until(p):
    """
    until : UNTIL OP logical_expr_main CL block_op block block_cl
          | UNTIL OP relational_expr CL block_op block block_cl
    """
    p[0] = Until(p[3], p[6])
    cprint("until block", p.lineno(1), p.lineno(7))

def p_foreach(p):
    """
    foreach : FOREACH OP ARRNAME CL block_op block block_cl
           | FOREACH OP handle_types CL block_op block block_cl
    """
    if ('@' in p[3]):
        symb = symtab.get_symbol(p[3])
        if (symb is None):
            print("ERROR array accessed before declaration.")
    p[0] = Foreach(p[3], p[6])
    cprint("foreach block", p.lineno(1), p.lineno(7))

def p_block_op(p):
    """
    block_op : BLOCKOP
    """
    symtab.enter_scope()

def p_block_cl(p):
    """
    block_cl : BLOCKCL
    """
    symtab.leave_scope()

def p_block(p):
    """
    block : block command
          | empty
    """
    if (len(p) == 2):
        p[0] = List([])
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_print(p):
    """
    print : PRINT handle_types SEMI
    """
    p[0] = Print(p[2])
    cprint("print statement", p.lineno(1), p.lineno(3))

def p_handle_types(p):
    """
    handle_types : identifier_types COMMA handle_types
                 | identifier_types
    """
    if (len(p) == 2):
        p[0] = List([p[1]])
    else:
        p[3].append(p[1])
        p[0] = p[3]

def p_relational_expr(p):
    """
    relational_expr : identifier_types GT identifier_types
                 | identifier_types LT identifier_types
                 | identifier_types EQ EQ identifier_types
                 | identifier_types GT EQ identifier_types
                 | identifier_types LT EQ identifier_types
    """
    if (len(p) == 2):
        cprint("relational expr", p.lineno(1), p.lineno(1))
    elif(len(p) == 4):
        p[0] = RelationalExpr(p[2], left = p[1], right = p[3], type=bool)
        cprint("relational expr", p.lineno(1), p.lineno(3))
    elif (len(p) == 5):
        temp_op = str(p[2]+p[3])
        p[0] = RelationalExpr(temp_op, left = p[1], right = p[4], type=bool)
        cprint("relational expr", p.lineno(1), p.lineno(4))
    else:
        print("relational expr")

def p_logical_expr(p):
    """
    logical_expr : logical_expr_bin AND identifier_types
                 | logical_expr_bin OR identifier_types
                 | logical_expr_bin AND relational_expr
                 | logical_expr_bin OR relational_expr
                 | logical_expr_bin AND logical_expr_bin
                 | logical_expr_bin OR logical_expr_bin
                 | logical_expr_bin
                 | empty
    """
    #cprint("logical expr", p.lineno(2), p.lineno(2))        
    pass

def p_logical_expr_bin(p):
    """
    logical_expr_bin : identifier_types AND identifier_types
                     | identifier_types OR identifier_types
                     | relational_expr AND relational_expr
                     | relational_expr OR relational_expr
    """
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 4):
        p[0] = LogicalExprBin(p[2], left = p[1], right = p[3], type=bool)

def p_logical_expr_main(p):
    """
    logical_expr_main : NOT logical_expr
                     | logical_expr
    """
    pass

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

def p_empty(p):
    """
    empty :
    """
    pass

def p_error(p):
    print("syntax error", p.lineno)


if __name__ == "__main__":
    lexer = lex.lex(module=lexer_lex)
    parser = yacc.yacc(debug=True)
    with open(sys.argv[1], "rt") as f:
        data = f.read()
        lexer.input(data)
        result = parser.parse(data)
        print(result)
    print()
    print()
    print()
    print("Printing SYMBOL_TABLE")
    print(symtab)
    print()
    print()
    print()
    print("Printing AST")
    print(start_ast.children)
    print(start_ast.data)
    draw_AST(start_ast)
    icg.intermediate_codegen(start_ast)
