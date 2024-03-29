# from ply import lex, yacc
# import sys
# import os
# import lexer_lex
# import parser_yacc
# from parser_yacc import start_ast as start
# from constructs.symbol_table import symbol_table, table_stack, find_most_recent_scope
# 
# lexer = lex.lex(module=lexer_lex)
# 
# with open(sys.argv[1]) as f:
#     data = f.read()
# 
# lexer.input(data)
# global_symbol_table = symbol_table("global", "global")
# stack = table_stack()
# stack.push(global_symbol_table)
# lineno, items = 1, list()
# 
# tables = list()
# for tok in lexer:
#     if (tok.lineno == lineno):
#         items.append(tok.value)
#     else:
#         items = [tok.value]
#         lineno += 1
# 
#     sym_table = stack.peek()
#     if(tok.type == 'VARNAME' or tok.type == 'ARRNAME'):
#         scope = sym_table.get_name()
#         name = ''
#         if (tok.type == 'VARNAME'):
#             name = str(tok.value).strip('$')
#         elif (tok.type == 'ARRNAME'):
#             name = str(tok.value).strip('@')
#         if ('my' in items or 'MY' in items):
#             try:
#                 old = sym_table.lookup(name)
#                 sym_table.insert(name, {'token' : tok.value,'line': tok.lineno, 'type' : tok.type, 'scope': scope})
#             except:
#                 sym_table.insert(name, {'token' : tok.value,'line': tok.lineno, 'type' : tok.type, 'scope': scope})
# 
#     elif(tok.type == 'BLOCKOP'):
#         scope_name = ''
#         if 'until' in items:
#             scope_name = 'until'
#         elif 'foreach' in items:
#             scope_name = 'foreach'
#         elif 'UNTIL' in items:
#             scope_name = 'until'
#         elif 'FOREACH' in items:
#             scope_name = 'foreach'
#         level = find_most_recent_scope(scope_name)
#         scope_name = ''.join([scope_name,"_", str(level+1)])
#         new_sym_table = symbol_table(scope_name, sym_table)
#         stack.push(new_sym_table)
#     elif(tok.type == 'BLOCKCL'):
#         child_sym_table = stack.pop()
#         tables.append(child_sym_table)
#         sym_table = stack.peek()
#         sym_table.put_child(child_sym_table.name, child_sym_table)
# 
# final_table = stack.peek()
# parser = yacc.yacc(module=parser_yacc, debug=True)
# parser.parse(data, tracking=True)
# final_table.print_table()
# tables.append(global_symbol_table)
# 
# print(start.children)
# print()
# print()
# print(start.data)
