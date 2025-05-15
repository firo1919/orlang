from expression import *
from orlang_token import Token
from tokenType import TokenType

class AstPrinter(Visitor[str]):
    def print(self, expr: Expression) -> str:
        return expr.accept(self)

    def visitBinaryExpression(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpression(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    def visitLiteralExpression(self, expr: Literal) -> str:
        return "nil" if expr.value is None else str(expr.value)

    def visitUnaryExpression(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs: Expression) -> str:
        builder = []
        builder.append(f"({name}")
        for expr in exprs:
            builder.append(f" {expr.accept(self)}")
        builder.append(")")
        return "".join(builder)

if __name__ == "__main__":
    expression = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(
            Literal(45.67)))

    print(AstPrinter().print(expression))