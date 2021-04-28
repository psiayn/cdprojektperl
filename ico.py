from constructs.ast import *
from constructs.symbol_table import SymbolInfo, SymbolTable
from icg import IntermediateCode, Quad
from typing import List

def constant_propagation_and_folding(code_list: List[Quad]):
    ignore_list = ['call_return', 'goto', 'if', 'ifFalse', 'Label: ', 'push', 'print', 'use', 'call']
    vars_dict = dict()

    for line in code_list:
        
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

            elif line.op1.type == "string" and line.op2.type == "number":
                if (line.operator == '+'):
                    line.op1 = line.op1.value + (str)(line.op2.value)
                else:
                    continue

                line.op2 = None
                line.operator = '='

            elif line.op1.type == "number" and line.op2.type == "string":
                if (line.operator == '+'):
                    line.op1 = (str)(line.op1.value) + line.op2.value
                else:
                    continue

                line.op2 = None
                line.operator = '='


            elif line.op1.type == "string" and line.op2.type == "string":
                if (line.operator == '+'):
                    line.op1 = line.op1.value + line.op2.value
                else:
                    continue

                line.op2 = None
                line.operator = '='

            elif line.op1.type == "variable" and line.op2.type == "variable":
                line.op1.value = vars_dict[line.op1.value]
                line.op2.value = vars_dict[line.op2.value]

                if isinstance(line.op1.value, Literal):
                    line.op1 = line.op1.value 

                if isinstance(line.op2.value, Literal):
                    line.op2 = line.op2.value

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

            else:
                continue
        
        if line.operator == '=':
            if not isinstance(line.op1, list) and line.op1 in vars_dict.keys():
                vars_dict[line.dest] = vars_dict[line.op1]
                line.op1 = vars_dict[line.dest]

            else:
                vars_dict[line.dest] = line.op1

        elif line.operator in ['+', '-', '*', '/']:

            if line.op1 in vars_dict.keys():
                line.op1 = vars_dict[line.op1]

            elif isinstance(line.op1, Literal):
                if line.op1.value in vars_dict.keys():
                    line.op1 = vars_dict[line.op1.value]

            if line.op2 in vars_dict.keys():
                line.op2 = vars_dict[line.op2]

            elif isinstance(line.op2, Literal):
                if line.op2.value in vars_dict.keys():
                    line.op2 = vars_dict[line.op2.value]
            
            if line.dest not in vars_dict.keys():
                if line.operator == '+':
                    vars_dict[line.dest] = line.op1 + line.op2

                elif line.operator == '-':
                    vars_dict[line.dest] = line.op1 - line.op2

                elif line.operator == '*':
                    vars_dict[line.dest] = line.op1 * line.op2

                elif line.operator == '/':
                    vars_dict[line.dest] = line.op1 / line.op2

    return code_list

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
        
        if line.dest != None:
            dest_list.append(line.dest)
        
        if line.op1 != None:
            ops_list.append(line.op1)

        if line.op2 != None:
            ops_list.append(line.op2)

    opt_code_list = list()
    
    for line in code_list:
        
        if line.dest in ops_list:
            opt_code_list.append(line)
        elif line.operator in ignore_list:
            opt_code_list.append(line)
        elif isinstance(line.op1, list):
            opt_code_list.append(line)
        else:
            pass

    return opt_code_list

def parse_ico(ic: IntermediateCode, symtab: SymbolTable):
    print("\nConstant propagation and folding\n")
    ic.code_list = constant_propagation_and_folding(ic.code_list)
    ic.print_three_address_code()
    print("\nDead Code Elimination\n")
    ic.code_list = dead_code(ic.code_list)
    return ic

if __name__ == '__main__':
    icg = IntermediateCode()
    res = parse_ico(icg)
