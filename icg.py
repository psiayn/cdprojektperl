from constructs.ast import *
from constructs.symbol_table import SymbolInfo, SymbolTable

class Quad:
    dest = None
    op1 = None
    op2 = None
    operator = None

    def __init__(self, dest, op1, op2, operator):
        self.dest = dest
        self.op1 = op1
        self.op2 = op2
        self.operator = operator

    def print_info(self):
        print("{} = {} {} {}".format(self.dest, self.op1, self.operator, self.op2))

class IntermediateCode:
    def __init__(self):
        #  self.code_list: List[Quad] = {Quad.func_name: []}
        self.code_list: List[Quad] = []
        self.temp_var_count = 0
        self.label_count = 0
        self.loop_stack = []

    def get_new_temp_var(self):
        self.temp_var_count += 1
        return "t" + str(self.temp_var_count)

    def get_new_label(self):
        self.label_count += 1
        return "LABEL_" + str(self.label_count)

    def add_to_list(self, code: Quad):
        self.code_list.append(code)

    def print_three_address_code(self):
        for i in self.code_list:
            dest = i.dest
            op1 = i.op1
            operator = i.operator
            op2 = i.op2

            if isinstance(dest, SymbolInfo):
                dest = dest.name
            if isinstance(op1, SymbolInfo):
                op1 = op1.name
            if isinstance(op2, SymbolInfo):
                op2 = op2.name
            if operator == '=':
                print("{} = {}".format(dest, op1))
            elif operator == 'Label: ':
                print("{}{}".format(operator, dest))
            elif operator == 'if':
                print("{} {} goto {}".format(operator, op1, dest))
            elif operator == 'ifFalse':
                print("{} goto {}".format(operator, dest))
            elif operator == 'print':
                print("call print")
            elif operator == 'push':
                print("push {}".format(dest))
            elif operator == 'use':
                print("call use")
            elif operator == 'call_return':
                print("{} = call {}".format(dest, op1))
            elif operator == 'goto':
                print("goto {}".format(dest))
            elif operator == '++':
                op = op1
                if(op1 is None):
                    op = op2
                print("{} = {} + 1".format(dest, op))
            else:
                print("{} = {} {} {}".format(dest, op1, operator, op2))

def _recur_codegen(node, ic: IntermediateCode, symtab: SymbolTable):
    # process all child nodes before parent
    # ast is from right to left, so need to traverse in reverse order

    if isinstance(node, Until):
        l = ic.get_new_label()
        ic.add_to_list(Quad(l, None, None, "Label: "))
        true_l = ic.get_new_label()
        false_l = ic.get_new_label()
        condition = node.data
        condition_res = _recur_codegen(condition, ic, symtab)
        ic.add_to_list(Quad(true_l, condition_res.name, None, "if"))
        ic.add_to_list(Quad(false_l, None, None, "ifFalse"))
        ic.add_to_list(Quad(true_l, None, None, "Label: "))
        symtab.enter_scope()
        body = node.children
        # body.reverse()
        for i in body:
            _recur_codegen(i, ic, symtab)
        symtab.leave_scope()
        node.children = []
        ic.add_to_list(Quad(l, None, None, "goto"))
        ic.add_to_list(Quad(false_l, None, None, "Label: "))

    elif isinstance(node, Foreach):
        lab = ic.get_new_label()
        ic.add_to_list(Quad(lab, None, None, "Label: "))
        true_l = ic.get_new_label()
        false_l = ic.get_new_label()
        iterator = node.data
        # i = 0
        t_i = ic.get_new_temp_var()
        symtab.add_if_not_exists(t_i)
        i = symtab.get_symbol(t_i)
        i.value = 0
        ic.add_to_list(Quad(i.name, 0, None, '='))
        # l = range(iterator)
        t_l = ic.get_new_temp_var()
        symtab.add_if_not_exists(t_l)
        l = symtab.get_symbol(t_l)
        ic.add_to_list(Quad(iterator, None, None, "push"))
        ic.add_to_list(Quad(l.name, "len", None, "call_return"))
        # i < l
        t_r = ic.get_new_temp_var()
        symtab.add_if_not_exists(t_r)
        r = symtab.get_symbol(t_l)
        ic.add_to_list(Quad(r.name, i.name, l.name, '<'))
        # checking condition
        # res = _recur_codegen(iterator, ic, symtab)
        ic.add_to_list(Quad(true_l, r.name, None, "if"))
        ic.add_to_list(Quad(false_l, None, None, "ifFalse"))
        ic.add_to_list(Quad(true_l, None, None, "Label: "))
        # body
        symtab.enter_scope()
        body = node.children
        ic.loop_stack.append((i, iterator))
        # body.reverse()
        for ibrr in body:
            _recur_codegen(ibrr, ic, symtab)
        symtab.leave_scope()
        # i++
        ic.add_to_list(Quad(i.name, i.name, None, '++'))
        node.children = []
        ic.add_to_list(Quad(lab, None, None, "goto"))
        ic.add_to_list(Quad(false_l, None, None, "Label: "))

    new_children = []
    print("PRINTING NODE CHILDREN:", node.children)
    for child in node.children:
        new_children.append(_recur_codegen(child, ic, symtab))

    new_children.reverse()
    return_val = None

    if isinstance(node, (BinOP, RelationalExpr, LogicalExprBin)):
        if node.operator == '=':
            ic.add_to_list(Quad(new_children[1], new_children[0], None, node.operator))
            return_val = new_children[1]
        else:
            temp = ic.get_new_temp_var()
            symtab.add_if_not_exists(temp)
            temp_symbol = symtab.get_symbol(temp)
            temp_symbol.value = node
            if (len(new_children) < 2):
                new_children.append(None)
            ic.add_to_list(Quad(temp_symbol, new_children[0], new_children[1], node.operator))
            return_val = temp_symbol

    elif isinstance(node, Use):
        ic.add_to_list(Quad(node.data, None, None, "push"))
        ic.add_to_list(Quad(None, None, None, "use"))

    elif isinstance(node, Literal):
        return_val = node
        if (node.type == "variable" and node.value == "$_"):
            if (ic.loop_stack == []):
                print("ERROR: CANNOT USE $_ as variable")
            else:
                t = ic.get_new_temp_var()
                symtab.add_if_not_exists(t)
                temp = symtab.get_symbol(t)
                temp.value = ic.loop_stack[-1][1] + '[' + ic.loop_stack[-1][0].name + ']'
                ic.add_to_list(Quad(temp.name, temp.value, None, '='))
                return_val = temp
            print("Literal:", node.value)

    elif isinstance(node, List):
        return_val = new_children

    elif isinstance(node, Array):
        print("ARRAY", node)
        data = node.data
        name = node.name
        if isinstance(data, List):
            data = data.children
        if node.name is None:
            name = name + "[" + str(int(node.index)) + "]"
        ic.add_to_list(Quad(name, data, None, '='))

    #     ic.add_to_list(Quad(node.))
    elif isinstance(node, Decleration):
        ic.add_to_list(Quad(node.name, node.value, None, '='))
        return_val = node

    elif isinstance(node, Print):
        if (node.children is not None):
            t = new_children[0]
            print(t)
            for i in t:
                ic.add_to_list(Quad(i, None, None, "push"))
            print(t)
            ic.add_to_list(Quad(None, None, None, "print"))
        else:
            ic.add_to_list(Quad(node.data, None, None, "print"))
    else:
        print(f"Intermediate code is not yet implemented for node {node}")

        return_val = node

    return return_val

def intermediate_codegen(ast, symtab):
    ic = IntermediateCode()

    _recur_codegen(ast, ic, symtab)
    return ic
