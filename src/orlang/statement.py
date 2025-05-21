from abc import ABC, abstractmethod
from .expression import Expression
from .token import Token
from typing import TypeVar, Generic, List

class Statement(ABC):
   @abstractmethod
   def accept(self, visitor: 'Visitor') -> object:
       pass

class Block(Statement):
   def __init__(self, statements: List[Statement]) -> None:
       self.statements = statements
   def accept(self, visitor: 'Visitor') -> object:
       return visitor.visitBlockStatement(self)

class ExpressionStatement(Statement):
   def __init__(self, expression: Expression) -> None:
       self.expression = expression
   def accept(self, visitor: 'Visitor') -> object:
       return visitor.visitExpressionStatementStatement(self)

class If(Statement):
   def __init__(self, condition: Expression, thenBranch: Statement, elseBranch: Statement) -> None:
       self.condition = condition
       self.thenBranch = thenBranch
       self.elseBranch = elseBranch
   def accept(self, visitor: 'Visitor') -> object:
       return visitor.visitIfStatement(self)

class Print(Statement):
   def __init__(self, expression: Expression) -> None:
       self.expression = expression
   def accept(self, visitor: 'Visitor') -> object:
       return visitor.visitPrintStatement(self)

class Var(Statement):
   def __init__(self, name: Token, initializer: Expression) -> None:
       self.name = name
       self.initializer = initializer
   def accept(self, visitor: 'Visitor') -> object:
       return visitor.visitVarStatement(self)

class While(Statement):
   def __init__(self, condition: Expression, body: Statement) -> None:
       self.condition = condition
       self.body = body
   def accept(self, visitor: 'Visitor') -> object:
       return visitor.visitWhileStatement(self)

R = TypeVar('R')

class Visitor(ABC, Generic[R]):
    @abstractmethod
    def visitBlockStatement(self, statement: Block) -> R:
        pass
    @abstractmethod
    def visitExpressionStatementStatement(self, statement: ExpressionStatement) -> R:
        pass
    @abstractmethod
    def visitIfStatement(self, statement: If) -> R:
        pass
    @abstractmethod
    def visitPrintStatement(self, statement: Print) -> R:
        pass
    @abstractmethod
    def visitVarStatement(self, statement: Var) -> R:
        pass
    @abstractmethod
    def visitWhileStatement(self, statement: While) -> R:
        pass

