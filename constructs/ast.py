class Node:
    def __init__(self, name, **kwargs):
        self.name = name
        self.children = [ c for c in kwargs['children'] if c is not None ]
        self.data = kwargs.get('data', None)

    def add_child(self, child):
        if child is not None:
            self.children.append(child)

class BinOP(Node):
    def __init__(self, operator, left=None, right=None):
        self.operator = operator
        self.left = left
        self.right = right
        children_ = []
        if isinstance(left, Node):
            children_.append(left)
        if isinstance(right, Node):
            children_.append(right)
        super().__init__("Binary", children=children_, data=operator)
        print("self.left", self.left)
        print("self.right", self.right)
        print("self.operator", self.operator)

    def __repr__(self):
        return f'<{self.left}, {self.right}, {self.operator}>'

class Literal(Node):
    def __init__(self, type, value):
        super().__init__("Literal", children=[], data=[value])
        self.type = type
        self.value = value

    def __repr__(self):
        return f'<{self.value}: {self.type}>'

class Array(Node):
    def __init__(self, name, index=None, data=None):
        if isinstance(data, Node):
            super().__init__("Array", children=[data], data=[name, index])
        else:
            super().__init__("Array", children=[None], data=[name, index, data])
        self.name = name
        self.index = index
        self.data = data
    def __repr__(self):
        return f'<{self.name}[{self.data}, {self.index}]>'

class Use(Node):
    def __init__(self, package):
        super().__init__("Use Statement", children=[], data=package)

class List(Node):
    def __init__(self, children):
        super().__init__("LIST", children=children, data=[])
        self.append = self.add_child

    def __iter__(self):
        return iter(self.children)

    def __len__(self):
        return len(self.children)

class Print(Node):
    def __init__(self, string):
        self.string = string
        if isinstance(string, Node):
            super().__init__("print", children=[string], data=[])
        else:
            super().__init__("print", children=[], data=string)

class Until(Node):
    def __init__(self, condition, block):
        print("Node: Until(condition = {}, block = {})".format(condition, block))
        super().__init__("Until", children=block, data=condition)

class Foreach(Node):
    def __init__(self, iterator, block):
        super().__init__("Foreach", children=block, data=iterator)

class Decleration(Node):
    def __init__(self, name, value=None):
        if isinstance(value, Node):
            super().__init__("decleration", children=[value], data=[name])
        else:
            super().__init__("decleration", children=[], data=[name, value])
        self.name = name
        self.value = value

    def __repr__(self):
        return f'<{self.name}: {self.value}>'

class LogicalExprBin(Node):
    def __init__(self, operator, left=None, right=None, type=None):
        self.operator = operator
        self.left = left
        self.right = right
        children_ = []
        if isinstance(left, Node):
            children_.append(left)
        if isinstance(right, Node):
            children_.append(right)
        super().__init__("LogicalBinary", children=children_, data=type)
        print("self.left", self.left)
        print("self.right", self.right)
        print("self.operator", self.operator)

    def __repr__(self):
        return f'<{self.left}, {self.right}, {self.operator}>'

class RelationalExpr(Node):
    def __init__(self, operator, left=None, right=None, type=None):
        self.operator = operator
        self.left = left
        self.right = right
        children_ = []
        if isinstance(left, Node):
            children_.append(left)
        if isinstance(right, Node):
           children_.append(right)
        super().__init__("RelationalExpr", children=children_, data=type)
        print("self.left", self.left)
        print("self.right", self.right)
        print("self.operator", self.operator)

    def __repr__(self):
        return f'<{self.left}, {self.right}, {self.operator}>'
