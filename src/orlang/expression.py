from abc import ABC, abstractmethod
from .token import Token
from typing import TypeVar, Generic

class Expression(ABC):
   @abstractmethod
   def accept(self, visitor: 'Visitor') -> object:
       pass

class Assign(Expression):
   def __init__(self, name: Token, value: Expression) -> None:
       self.name = name
       self.value = value
   def accept(self, visitor: 'Visitor') -> object:
       return visitor.visitAssignExpression(self)

class Binary(Expression):
   def __init__(self, left: Expression, operator: Token, right: Expression) -> None:
       self.left = left
       self.operator = operator
       self.right = right
   def accept(self, visitor: 'Visitor') -> object:
       return visitor.visitBinaryExpression(self)

class Grouping(Expression):
   def __init__(self, expression: Expression) -> None:
       self.expression = expression
   def accept(self, visitor: 'Visitor') -> object:
       return visitor.visitGroupingExpression(self)

class Literal(Expression):
   def __init__(self, value: object) -> None:
       self.value = value
   def accept(self, visitor: 'Visitor') -> object:
       return visitor.visitLiteralExpression(self)

class Logical(Expression):
   def __init__(self, left: Expression, operator: Token, right: Expression) -> None:
       self.left = left
       self.operator = operator
       self.right = right
   def accept(self, visitor: 'Visitor') -> object:
       return visitor.visitLogicalExpression(self)

class Unary(Expression):
   def __init__(self, operator: Token, right: Expression) -> None:
       self.operator = operator
       self.right = right
   def accept(self, visitor: 'Visitor') -> object:
       return visitor.visitUnaryExpression(self)

class Variable(Expression):
   def __init__(self, name: Token) -> None:
       self.name = name
   def accept(self, visitor: 'Visitor') -> object:
       return visitor.visitVariableExpression(self)

R = TypeVar('R')

class Visitor(ABC, Generic[R]):
    @abstractmethod
    def visitAssignExpression(self, expression: Assign) -> R:
        pass
    @abstractmethod
    def visitBinaryExpression(self, expression: Binary) -> R:
        pass
    @abstractmethod
    def visitGroupingExpression(self, expression: Grouping) -> R:
        pass
    @abstractmethod
    def visitLiteralExpression(self, expression: Literal) -> R:
        pass
    @abstractmethod
    def visitLogicalExpression(self, expression: Logical) -> R:
        pass
    @abstractmethod
    def visitUnaryExpression(self, expression: Unary) -> R:
        pass
    @abstractmethod
    def visitVariableExpression(self, expression: Variable) -> R:
        pass

