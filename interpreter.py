from expression import *
from tokenType import TokenType
from orlang_token import Token


class Interpreter(Visitor[object]):
    def interpret(self, expression: Expression):
        try:
            value = self.evaluate(expression)
            print(self.stringify(value))
        except RuntimeError as error:
            from orlang import Orlang
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

        # Unreachable
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

    def evaluate(self, expr: Expression) -> object:
        return expr.accept(self)

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
            return "nil"

        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text

        return str(obj)
