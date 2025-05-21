from typing import List

from .expression import (
    Assign,
    Binary,
    Expression,
    Grouping,
    Literal,
    Logical,
    Unary,
    Variable,
)
from .statement import Block, ExpressionStatement, If, Print, Statement, Var, While
from .token import Token
from .token_type import TokenType


class Parser:
    class ParseError(RuntimeError):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)
        
    def __init__(self, tokens: List[Token]) -> None:
        self.current = 0
        self.tokens = tokens

    def parse(self) -> List[Statement]:
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())

        return statements

    def declaration(self) -> Statement | None:
        try:
            if self.match(TokenType.VARIABLE):
                return self.varDeclaration()

            return self.statement()
        except Parser.ParseError:
            self.synchronize()
            return ExpressionStatement(Literal(None))

    def varDeclaration(self) -> Statement | None:
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer if initializer is not None else Literal(None))

    def statement(self) -> Statement | None:
        if self.match(TokenType.FOR):
            return self.forStatement()

        if self.match(TokenType.IF):
            return self.ifStatement()

        if self.match(TokenType.PRINT):
            return self.printStatement()

        if self.match(TokenType.WHILE):
            return self.whileStatement()

        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())

        return self.expressionStatement()

    def forStatement(self) -> Statement:
        # consume the '(' after 'for'
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
        # --- initializer ---
        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.VARIABLE):
            initializer = self.varDeclaration()
        else:
            initializer = self.expressionStatement()
        # --- condition ---
        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        else:
            # no condition → infinite loop
            condition = Literal(True)
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")
        # --- increment ---
        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")
        # --- body ---
        body = self.statement()
        if body is None:
            raise Exception("Body of the 'for' statement cannot be None.")
        # run body first, then increment
        if increment is not None:
            body = Block([body, ExpressionStatement(increment)])
        # wrap in a while
        body = While(condition, body)
        # initializer before the loop
        if initializer is not None:
            body = Block([initializer, body])
        return body

    def ifStatement(self) -> Statement | None:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
        if self.match(TokenType.ELSE):
            thenBranch = self.statement()
            elseBranch = self.statement()
            if thenBranch and elseBranch:
                return If(condition, thenBranch, elseBranch)

        return None

    def printStatement(self) -> Statement:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def expressionStatement(self) -> Statement:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return ExpressionStatement(value)

    def whileStatement(self) -> Statement | None:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()

        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()

        if body and condition:
            return While(condition, body)

        return None

    def block(self) -> List[Statement]:
        statements = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def expression(self) -> Expression:
        return self.assignment()

    def assignment(self) -> Expression:
        expr = self._or()
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            # FIX: use isinstance, and pull the name off the expr
            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)

            self.error(equals, "Invalid assignment target.")

        return expr

    def _or(self) -> Expression:
        expr = self._and()

        while self.match(TokenType.OR):
            operator = self.previous()
            right = self._and()
            expr = Logical(expr, operator, right)

        return expr

    def _and(self) -> Expression:
        expr = self.equality()

        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)

        return expr

    def equality(self) -> Expression:
        expression = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expression = Binary(expression, operator, right)

        return expression
    
    def match(self, *types: TokenType) -> bool:
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False
    
    def check(self, type: TokenType) -> bool:
        if self.isAtEnd():
            return False
        return self.peek().type == type
    
    def advance(self) -> Token:
        if not self.isAtEnd(): 
            self.current += 1
        return self.previous()
    
    def isAtEnd(self) -> bool:
        return self.peek().type == TokenType.DHUMA

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]
    
    def comparison(self) -> Expression:
        expression = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expression = Binary(expression, operator, right)

        return expression
    
    def term(self) -> Expression:
        expression = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expression = Binary(expression, operator, right)

        return expression
    
    def factor(self) -> Expression:
        expression = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expression = Binary(expression, operator, right)

        return expression

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()
    
    def primary(self) -> Expression:
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NULL):
            return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        if self.match(TokenType.LEFT_PAREN):
            expression = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expression)

        raise Exception(self.peek(), "Expect expression.")
    
    def consume(self, type: TokenType, message: str):
        if self.check(type):
            return self.advance()
        raise Exception(self.peek(), message)

    def error(self, token: Token, message: str):
        Parser.parseerror(token, message)
        return Parser.ParseError()
    
    @staticmethod
    def parseerror(token: Token, message: str):
        from .orlang import Orlang
        if (token.type == TokenType.DHUMA):
            Orlang.report(token.line, " at end", message)
        else:
            Orlang.report(token.line, " at '" + token.lexeme + "'", message)
    
    def synchronize(self):
        self.advance()

        while not self.isAtEnd():
            if (self.previous().type == TokenType.SEMICOLON):
                return
            if self.peek().type in {
                TokenType.CLASS,
                TokenType.FUNCTION,
                TokenType.VARIABLE,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            }:
                return
        
        self.advance()

