from icg import IntermediateCode, Quad
from typing import List

def constant_folding(code_list: List[Quad]):
    for line in code_list:
        if (line.operator == '=' and line.print_info() is not None):
            print(line.print_info())

def parse_ico(ic: IntermediateCode):
    print("lol nub")
    # for i in ic.code_list:
    #     if i.print_info() is not None:
    #         print(i.print_info())
    constant_folding(ic.code_list)

if __name__ == '__main__':
    icg = IntermediateCode()
    parse_ico(icg)
