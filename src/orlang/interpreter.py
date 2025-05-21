from .expression import Binary, Grouping, Literal, Unary, Expression, Variable
from .token_type import TokenType
from .token import Token
from .expression import Visitor as ExpressionVisitor
from .statement import Visitor as StatementVisitor
from .statement import ExpressionStatement, Block, Statement, Print, Var, If, While
from .environment import Environment
from typing import List


class Interpreter(ExpressionVisitor[object], StatementVisitor[None]):
    environment = Environment()
    def interpret(self, statements: List[Statement]) -> None:
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            from .orlang import Orlang
            Orlang.runtimeError(error)

    def visitBinaryExpression(self, expression: Binary) -> object:
        left = self.evaluate(expression.left)
        right = self.evaluate(expression.right)

        operator_type = expression.operator.type

        if operator_type == TokenType.GREATER:
            self.checkNumberOperands(expression.operator, left, right)
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return float(left) > float(right)
            raise RuntimeError(expression.operator, "Operands must be numbers.")
        elif operator_type == TokenType.GREATER_EQUAL:
            self.checkNumberOperands(expression.operator, left, right)
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return float(left) >= float(right)
            raise RuntimeError(expression.operator, "Operands must be numbers.")
        elif operator_type == TokenType.LESS:
            self.checkNumberOperands(expression.operator, left, right)
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return float(left) < float(right)
            raise RuntimeError(expression.operator, "Operands must be numbers.")
        elif operator_type == TokenType.LESS_EQUAL:
            self.checkNumberOperands(expression.operator, left, right)
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return float(left) <= float(right)
            raise RuntimeError(expression.operator, "Operands must be numbers.")
        elif operator_type == TokenType.MINUS:
            self.checkNumberOperands(expression.operator, left, right)
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return float(left) - float(right)
            raise RuntimeError(expression.operator, "Operands must be numbers.")
        elif operator_type == TokenType.PLUS:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            raise RuntimeError(expression.operator, "Operands must be two numbers or two strings.")
        elif operator_type == TokenType.SLASH:
            self.checkNumberOperands(expression.operator, left, right)
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                if right == 0:
                    raise RuntimeError(expression.operator, "Division by zero.")
                return float(left) / float(right)
            raise RuntimeError(expression.operator, "Operands must be numbers.")
        elif operator_type == TokenType.STAR:
            self.checkNumberOperands(expression.operator, left, right)
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return float(left) * float(right)
            raise RuntimeError(expression.operator, "Operands must be numbers.")
        elif operator_type == TokenType.BANG_EQUAL:
            return not self.isEqual(left, right)
        elif operator_type == TokenType.EQUAL_EQUAL:
            return self.isEqual(left, right)

        return None

    def visitGroupingExpression(self, expression: Grouping) -> object:
        return self.evaluate(expression.expression)

    def visitLiteralExpression(self, expression: Literal) -> object:
        return expression.value

    def visitUnaryExpression(self, expression: Unary) -> object:
        right = self.evaluate(expression.right)

        if expression.operator.type == TokenType.BANG:
            return not self.isTruthy(right)
        elif expression.operator.type == TokenType.MINUS:
            self.checkNumberOperand(expression.operator, right)
            if isinstance(right, (int, float)):
                return -float(right)
            raise TypeError(f"Unsupported operand type for unary minus: {type(right).__name__}")

        return None
    
    def visitExpressionStatementStatement(self, statement: ExpressionStatement) -> None:
        self.evaluate(statement.expression)
        return None
    
    def visitPrintStatement(self, statement: Print) -> None:
        value = self.evaluate(statement.expression)
        print(self.stringify(value))
        return None
    
    def visitVarStatement(self, statement: Var) -> None:
        value = None
        if statement.initializer is not None:
            value = self.evaluate(statement.initializer)

        self.environment.define(statement.name.lexeme, value)
        return None
    
    def visitAssignExpression(self, expression) -> object:
        value = self.evaluate(expression.value)
        self.environment.assign(expression.name, value)
        return value
    
    def visitVariableExpression(self, expression: Variable) -> object:
        return self.environment.get(expression.name)

    def execute(self, statement: Statement) -> None:
        statement.accept(self)
        
    def visitBlockStatement(self, statement: Block) -> None:
        self.executeBlock(statement.statements, Environment(self.environment))
        return None

    def visitIfStatement(self, statement: If) -> None:
        if self.isTruthy(self.evaluate(statement.condition)):
            self.execute(statement.thenBranch)
        elif statement.elseBranch is not None:
            self.execute(statement.elseBranch)
        return None
    
    def visitLogicalExpression(self, expression):
        left = self.evaluate(expression.left)

        if expression.operator.type == TokenType.OR:
            if self.isTruthy(left):
                return left
        else:
            if self.isTruthy(left):
                return left

        return self.evaluate(expression.right)
    
    def visitWhileStatement(self, statement: While) -> None:
        while self.isTruthy(self.evaluate(statement.condition)):
            self.execute(statement.body)
            
        return None
     
    def executeBlock(self, statements: List[Statement], environment: Environment) -> None:
        previous = self.environment
        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous
                    
    def evaluate(self, expression: Expression) -> object:
        return expression.accept(self)

    def isTruthy(self, obj: object) -> bool:
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def isEqual(self, a: object, b: object) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def checkNumberOperand(self, operator: Token, operand: object):
        if isinstance(operand, (int, float)):
            return
        raise RuntimeError(operator, "Operand must be a number.")

    def checkNumberOperands(self, operator: Token, left: object, right: object):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return
        raise RuntimeError(operator, "Operands must be numbers.")

    def stringify(self, obj: object) -> str:
        if obj is None:
            return "duwwaa"
        if isinstance(obj, bool):
            return "dhugaa" if obj else "soba"
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text

        return str(obj)
    
    
