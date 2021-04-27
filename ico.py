from constructs.ast import *
from constructs.symbol_table import SymbolInfo, SymbolTable
from icg import IntermediateCode, Quad
from typing import List

def constant_folding(code_list: List[Quad], symtab: SymbolTable):
    for line in code_list:
        # print(line.op1, line.op2)
        if isinstance(line.dest, SymbolInfo):
            line.dest = line.dest.name
        elif isinstance(line.dest, Literal):
            line.dest = line.dest.value

        if isinstance(line.op1, SymbolInfo):
            line.op1 = line.op1.name
        # elif isinstance(line.op1, Literal):
        #     line.op1 = line.op1.value
        
        if isinstance(line.op2, SymbolInfo):
            line.op2 = line.op2.name
        # elif isinstance(line.op2, Literal):
        #     line.op2 = line.op2.value
        
        if (isinstance(line.op1, Literal) and isinstance(line.op2, Literal) and (line.operator in ['+', '-', '*', '/'] )):
            if line.op1.type == "number" and line.op2.type == "number":
                if (line.operator == '+'):
                    line.op1 = line.op1.value + line.op2.value
                elif (line.operator == '-'):
                    line.op1 = line.op1.value - line.op2.value
                elif (line.operator == '*'):
                    line.op1 = line.op1.value * line.op2.value
                elif (line.operator == '/'):
                    line.op1 = line.op1.value / line.op2.value
                else:
                    continue
                line.op2 = None
                line.operator = '='
                t = symtab.get_symbol(line.dest)
                t.value = line.op1
            elif line.op1.type == "string" and line.op2.type == "number":
                if (line.operator == '+'):
                    line.op1 = line.op1.value + (str)(line.op2.value)
                else:
                    continue
                line.op2 = None
                line.operator = '='
                t = symtab.get_symbol(line.dest)
                t.value = line.op1
            elif line.op1.type == "number" and line.op2.type == "string":
                if (line.operator == '+'):
                    line.op1 = (str)(line.op1.value) + line.op2.value
                else:
                    continue
                line.op2 = None
                line.operator = '='
                t = symtab.get_symbol(line.dest)
                t.value = line.op1
            elif line.op1.type == "string" and line.op2.type == "string":
                if (line.operator == '+'):
                    line.op1 = line.op1.value + line.op2.value
                else:
                    continue
                line.op2 = None
                line.operator = '='
                t = symtab.get_symbol(line.dest)
                t.value = line.op1
            else:
                continue
            print("{} = {} {} {}".format(line.dest, line.op1, line.operator, line.op2))

def dead_code(code_list: List[Quad]):
    ignore_list = ['call_return', 'goto', 'if', 'ifFalse', 'Label: ', 'push', 'print', 'use', 'call']
    dest_list = list()
    ops_list = list()

    for line in code_list:
        
        if isinstance(line.dest, SymbolInfo):
            line.dest = line.dest.name
        elif isinstance(line.dest, Literal):
            line.dest = line.dest.value

        if isinstance(line.op1, SymbolInfo):
            line.op1 = line.op1.name
        elif isinstance(line.op1, Literal):
            line.op1 = line.op1.value
        
        if isinstance(line.op2, SymbolInfo):
            line.op2 = line.op2.name
        elif isinstance(line.op2, Literal):
            line.op2 = line.op2.value
        
        #print(line.dest,"\t",line.op1,"\t",line.op2,"\t",line.operator)

        if line.dest != None:
            dest_list.append(line.dest)
        
        if line.op1 != None:
            ops_list.append(line.op1)

        if line.op2 != None:
            ops_list.append(line.op2)

    #print("\n",dest_list,"\n\n\n\n\n",ops_list)
    
    opt_code_list = list()
    
    for line in code_list:
        
        if line.dest in ops_list:
            opt_code_list.append(line)
        elif line.operator in ignore_list:
            opt_code_list.append(line)
        else:
            pass

    return opt_code_list

def parse_ico(ic: IntermediateCode, symtab: SymbolTable):
    print("lol nub")
    # for i in ic.code_list:
    #     if i.print_info() is not None:
    #         print(i.print_info())
    constant_folding(ic.code_list, symtab)
    print("bonjour")
    # ic.code_list = dead_code(ic.code_list)
    return ic

if __name__ == '__main__':
    icg = IntermediateCode()
    res = parse_ico(icg)
