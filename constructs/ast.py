class Node:
    def __init__(self, name, **kwargs):
        self.name = name
        self.children = [ c for c in kwargs['children'] if c is not None ]
        self.data = kwargs.get('data', None)


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

class Decleration(Node):
    def __init__(self, type=None, value):
        super().__init__("Decleration", children=None, data=value)
        self.type = type
        self.value = value