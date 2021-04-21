class Node:
    def __init__(self, name, **kwargs):
        self.name = name
        self.children = [ c for c in kwargs['children'] if c is not None ]
        self.data = kwargs.get('data', None)

    def add_child(self, child):
        if child is not None:
            self.children.append(child)

class BinOP(Node):
    def __init__(self, operator, left=None, right=None, type=None):
        super().__init__("Binary", children=[left, right], data=type)
        self.operator = operator
        self.left = left
        self.right = right
        x = self.left
        y = self.right
        if isinstance(left, Node):
            x = left.data
        if isinstance(right, Node):
            y = right.data
        print("self.left", self.left)
        print("self.right", self.right)
        print("self.operator", self.operator)

    def __repr__(self):
        return f'<{self.left}, {self.right}, {self.operator}>'

class Literal(Node):
    def __init__(self, type, value):
        super().__init__("Literal", children=[type], data=value)
        self.type = type
        self.value = value

    def __repr__(self):
        return f'<{self.value}: {self.type}>'

class Array(Node):
    def __init__(self, name, index=None, data=None):
        super().__init__("Array", children=[], data=[name, index, data])
        self.name = name
        self.index = index
        self.data = data
    def __repr__(self):
        return f'<{self.name}[{self.data}, {self.index}]>'

class Use(Node):
    def __init__(self, package):
        super().__init__("Use Statement", children=[], data=package)

class List(Node):
    """Node to store literals"""

    def __init__(self, children):
        super().__init__("LIST", children=children)
        self.append = self.add_child

    def __iter__(self):
        return iter(self.children)

    def __len__(self):
        return len(self.children)

class Print(Node):
    def __init__(self, string):
        super().__init__("Print", children=[], data=string)

class Until(Node):
    def __init__(self, condition, block):
        super().__init__("Until", children=block, data=condition)

class Foreach(Node):
    def __init__(self, iterator, block):
        super().__init__("Foreach", children=block, data=iterator)

class Decleration(Node):
    def __init__(self, value, type=None):
        super().__init__("Decleration", children=[None], data=value)
        self.type = type
        self.value = value
    
    def __repr__(self):
        return f'<{self.value}: {self.type}>'

class LogicalExprBin(Node):
    def __init__(self, operator, left=None, right=None, type=None):
        super().__init__("LogicalBinary", children=[left,right], data=type)
        self.operator = operator
        self.left = left
        self.right = right
        x = self.left
        y = self.right
        if isinstance(left, Node):
            x = left.data
        if isinstance(right, Node):
            y = right.data
        print("self.left", self.left)
        print("self.right", self.right)
        print("self.operator", self.operator)

    def __repr__(self):
        return f'<{self.left}, {self.right}, {self.operator}>'

class RelationalExpr(Node):
    def __init__(self, operator, left=None, right=None, type=None):
        super().__init__("RelationalExpr", children=[left,right], data=type)
        self.operator = operator
        self.left = left
        self.right = right
        x = self.left
        y = self.right
        if isinstance(left, Node):
            x = left.data
        if isinstance(right, Node):
            y = right.data
        print("self.left", self.left)
        print("self.right", self.right)
        print("self.operator", self.operator)

    def __repr__(self):
        return f'<{self.left}, {self.right}, {self.operator}>'
