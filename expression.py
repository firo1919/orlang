from abc import ABC, abstractmethod
from orlang_token import Token
from typing import TypeVar, Generic

R = TypeVar('R')

class Expression(ABC):
   @abstractmethod
   def accept(self, visitor: 'Visitor') -> R:
       pass

class Binary(Expression):
   def __init__(self, left: Expression, operator: Token, right:Expression) -> None:
       self.left = left
       self.operator = operator
       self.right = right
   def accept(self, visitor: 'Visitor') -> R:
       return visitor.visitBinaryExpression(self)

class Grouping(Expression):
   def __init__(self, expression: Expression) -> None:
       self.expression = expression
   def accept(self, visitor: 'Visitor') -> R:
       return visitor.visitGroupingExpression(self)

class Literal(Expression):
   def __init__(self, value: object) -> None:
       self.value = value
   def accept(self, visitor: 'Visitor') -> R:
       return visitor.visitLiteralExpression(self)

class Unary(Expression):
   def __init__(self, operator: Token, right: Expression) -> None:
       self.operator = operator
       self.right = right
   def accept(self, visitor: 'Visitor') -> R:
       return visitor.visitUnaryExpression(self)

class Visitor(ABC, Generic[R]):
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
    def visitUnaryExpression(self, expression: Unary) -> R:
        pass

