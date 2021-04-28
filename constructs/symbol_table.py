from pprint import pprint
from dataclasses import dataclass
from typing import Optional, Any
from collections import defaultdict
from tabulate import tabulate

scopes = {'until': 0, 'foreach': 0}

@dataclass
class SymbolInfo:
    name: str
    scope_id: str
    lineno: Optional[int] = None
    value: Any = None


class SymbolTable:
    def __init__(self):
        self.stack = [{}]
        self.symbols = []
        self.cur_scope = "1"
        self.level = 1
        self.scopes_at_level = defaultdict(lambda: 0)
        self.scopes_at_level[0] = 1

    def enter_scope(self):
        self.level += 1
        self.scopes_at_level[self.level] += 1
        self.cur_scope += f".{self.scopes_at_level[self.level]}"
        self.stack.append({})

    def leave_scope(self):
        self.level -= 1
        ind_of_dot = self.cur_scope.rfind(".")
        self.cur_scope = self.cur_scope[:ind_of_dot]
        self.scopes_at_level[self.level + 2] = 0
        self.stack.pop()

    def add_if_not_exists(self, symbol):
        if symbol in self.stack[-1]:
            return self.stack[-1][symbol]

        new_symbol = SymbolInfo(symbol, self.cur_scope)

        self.symbols.append(new_symbol)
        self.stack[-1][symbol] = new_symbol

        return new_symbol

    def get_symbol(self, symbol):
        for symtab in reversed(self.stack):
            if symbol in symtab:
                return symtab[symbol]

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
