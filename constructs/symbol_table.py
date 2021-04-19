import re
from pprint import pprint
scopes = {'until': 0, 'foreach': 0} 

class table_stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def get_length(self):
        return len(self.items)

class symbol_table:
    def __init__(self, name, parent): # parent is another object of the symbol_table class
        self.symbols = {}
        self.name = name
        self.children = {} # to store all scopes inside an enclosing one
        self.parent = parent

    def insert(self, symbol, token): 
        if symbol not in self.symbols:
            self.symbols[symbol] = token
        else:
            pre = self.lookup(symbol)
            print("ERROR! SYMBOL ~", symbol, "~ AT LINE ", token['line'], " ALREADY EXISTS AT LINE ", pre['line'], sep="")

    def lookup(self, symbol):
        return self.symbols[symbol]
    
    def get_symbols(self):
        return self.symbols

    def get_name(self):
        return self.name

    def get_parent(self):
        return self.parent

    def put_child(self, name, child):
        self.children[name] = child

    def get_child(self, name):
        return self.children[name]

    def get_children(self):
        return self.children.keys()

    def print_table(self):
        print ("Table :  ", self.name)
        pprint(self.symbols)
        for i in self.symbols:
            pprint(f"{i} : {self.symbols[i]}")
        pprint('')
        for i in self.children:
            self.children[i].print_table()	

def find_most_recent_scope(scope_name):
    global scopes
    if scope_name not in scopes.keys():
        return 0
    level = scopes[scope_name]
    scopes[scope_name] += 1
    return level
