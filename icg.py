from constructs.ast import *
class Quad:
    dest = None
    op1 = None
    op2 = None
    operator = None

    #  func_name = None

    def __init__(self, dest, op1, op2, operator):
        self.dest = dest
        self.op1 = op1
        self.op2 = op2
        self.operator = operator
        #  self.func_name = str(func_name)

    def print_info(self):
        print("{} = {} {} {}".format(self.dest, self.op1, self.operator, self.op2))


class IntermediateCode:
    def __init__(self):
        #  self.code_list: List[Quad] = {Quad.func_name: []}
        self.code_list: List[Quad] = []
        self.temp_var_count = 0

    def get_new_temp_var(self):
        self.temp_var_count += 1
        return "t" + str(self.temp_var_count)

    def add_to_list(self, code: Quad):
        self.code_list.append(code)
        #  self.code_list[Quad.func_name].append(code)

    def print_three_address_code(self):
        for i in self.code_list:
            print("{} = {} {} {}".format(i.dest, i.op1, i.operator, i.op2))
        #  for i in self.code_list:
        #      print("{} : ".format(i))
        #      for j in range(len(self.code_list[i])):
        #          print("%5d:\t" % j, self.code_list[i][j])



def _recur_codegen(node, ic):
    # process all child nodes before parent
    # ast is from right to left, so need to traverse in reverse order

    node_class_name = node.__class__.__name__

    new_children = []
    for child in reversed(node.children):
        new_children.append(_recur_codegen(child, ic))

    new_children.reverse()

    return_val = []

    tac_fn_name = f"tac_{node_class_name}"

    # if tac_fn_name in globals():
    #     globals()[tac_fn_name](ic, node, new_children, return_val)
    if isinstance(node, BinOP):
        print(node)
        print("calling necessary functions")

    else:
        print(f"Intermediate code is not yet implemented for node {node}")

        return_val.append(node)

    return return_val


def intermediate_codegen(ast):
    ic = IntermediateCode()

    _recur_codegen(ast, ic)

    return ic
