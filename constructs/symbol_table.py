from pprint import pprint
from dataclasses import dataclass
from typing import Optional, Any
from collections import defaultdict
from tabulate import tabulate
scopes = {'until': 0, 'foreach': 0}

@dataclass
class SymbolInfo:
    """Stores information related to a symbol"""

    name: str
    scope_id: str
    lineno: Optional[int] = None
    value: Any = None


class SymbolTable:
    """Stores all identifiers, literals and information
    related to them"""

    def __init__(self):
        self.stack = [{}]
        self.symbols = []
        self.cur_scope = "1"
        self.depth = 1
        self.scopes_at_depth = defaultdict(lambda: 0)
        self.scopes_at_depth[0] = 1

    def enter_scope(self):
        self.depth += 1
        self.scopes_at_depth[self.depth] += 1
        self.cur_scope += f".{self.scopes_at_depth[self.depth]}"
        self.stack.append({})

    def leave_scope(self):
        self.depth -= 1
        ind_of_dot = self.cur_scope.rfind(".")
        self.cur_scope = self.cur_scope[:ind_of_dot]
        self.scopes_at_depth[self.depth + 2] = 0
        self.stack.pop()

    def add_if_not_exists(self, symbol):
        if symbol in self.stack[-1]:
            return self.stack[-1][symbol]

        new_symbol = SymbolInfo(symbol, self.cur_scope)

        self.symbols.append(new_symbol)
        self.stack[-1][symbol] = new_symbol

        return new_symbol

    def get_symbol(self, symbol):
        """Finds the symbol in the closest symtab

        Returns None if symbol doesn't exist
        """
        for symtab_ in reversed(self.stack):
            if symbol in symtab_:
                return symtab_[symbol]

    def __str__(self):
        return str(
            tabulate(
                [
                    [
                        symbol.name,
                        symbol.scope_id,
                        symbol.lineno,
                        symbol.value,
                    ]
                    for symbol in self.symbols
                ],
                headers=[
                    "Symbol",
                    "Scope",
                    "Line No.",
                    "Value",
                ],
                tablefmt="fancy_grid",
            )
        )


""" {{{
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
    }}}"""
