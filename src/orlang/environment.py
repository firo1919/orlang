from .runtime_error import RuntimeError
from .token import Token


class Environment:

    def __init__(self, enclosing: 'Environment|None'=None) -> None:
        self.values = dict()
        self.enclosing = enclosing
        
    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        
        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")
        
    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        
        raise RuntimeError(name,
            "Undefined variable '" + name.lexeme + "'.")
    
    def define(self, name: str, value: object):
        self.values[name] = value