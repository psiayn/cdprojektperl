from ply import lex, yacc
import sys
import os
import lexer_lex
import parser_yacc
from symbol_table import symbol_table, table_stack, find_most_recent_scope

lexer = lex.lex(module=lexer_lex)

with open(sys.argv[1]) as f:
    data = f.read()

lexer.input(data)
global_symbol_table = symbol_table("global", "global")
stack = table_stack()
stack.push(global_symbol_table)
lineno, items = 0, list()

for tok in lexer:
    if (tok.lineno == lineno):
        items.append(tok.value)
    else:
        items = [tok.value]
        lineno += 1

    sym_table = stack.peek()
    if(tok.type == 'VARNAME' or tok.type == 'ARRNAME'):
        if (tok.type == 'VARNAME'):
            name = str(tok.value).strip('$')
        elif (tok.type == 'ARRNAME'):
            name = str(tok.value).strip('@')
        try:
            old = sym_table.lookup(name)
            if 'my' not in items:
                print("spront", old)
            else: 
                print("PREVIOUS SYMBOL IS", old)
        except:
            print(end="")
        sym_table.insert(name, {'token' : tok.value,'line': tok.lineno, 'type' : tok.type, 'scope': "global"})
    elif(tok.type == 'BLOCKOP'):
        scope_name = ''
        if 'UNTIL' in items:
            scope_name = 'until'
        elif 'FOREACH' in items:
            scope_name = 'foreach'
        level = find_most_recent_scope(scope_name)
        scope_name = ''.join([scope_name, str(level+1)])
        new_sym_table = symbol_table(scope_name, sym_table)
        stack.push(new_sym_table)
    elif(tok.type == 'BLOCKCL'):
        child_sym_table = stack.pop()
        sym_table = stack.peek()
        sym_table.put_child(child_sym_table.name, child_sym_table)

final_table = stack.peek()
parser = yacc.yacc(module=parser_yacc)
final_table.print_table()
