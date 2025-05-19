from typing import List

from .expression import Assign, Binary, Expression, Grouping, Literal, Unary, Variable
from .statement import ExpressionStatement, Print, Statement, Var, Block
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

    def declaration(self) -> Statement:
        try:
            if self.match(TokenType.VARIABLE):
                return self.varDeclaration()

            return self.statement()
        except Parser.ParseError:
            self.synchronize()
            return ExpressionStatement(Literal(None))

    def varDeclaration(self) -> Statement:
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)

    def statement(self) -> Statement:
        if self.match(TokenType.PRINT):
            return self.printStatement()
        
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())

        return self.expressionStatement()

    def printStatement(self) -> Statement:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def expressionStatement(self) -> Statement:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return ExpressionStatement(value)
    
    def block(self) -> List[Statement]:
        statements = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def expression(self) -> Expression:
        return self.assignment()

    def assignment(self) -> Expression:
        expression = self.equality()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if expression is Variable:
                name = Variable(expression).name
                return Assign(name, value)

            self.error(equals, "Invalid assignment target.")

        return expression

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
        from orlang import Orlang
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

