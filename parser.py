from typing import List
from tokenType import TokenType
from orlang_token import Token
from expression import *
from typing import Optional

class Parser:
    class ParseError(RuntimeError):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)
        
    def __init__(self, tokens: List[Token]) -> None:
        self.current = 0
        self.tokens = tokens

    def parse(self) -> Optional[Expression]:
        try:
            return self.expression()
        except Parser.ParseError:
            return None

    def expression(self) -> Expression:
        return self.equality()
    
    def equality(self) -> Expression:
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr
    
    def match(self, *types: TokenType) -> bool:
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False
    
    def check(self, type: TokenType) -> bool:
        if self.isAtEnd(): return False
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
        expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr
    
    def term(self) -> Expression:
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr
    
    def factor(self) -> Expression:
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
            
        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()
    
    def primary(self) -> Expression:
        if self.match(TokenType.SOBA): 
            return Literal(False)
        if self.match(TokenType.DHUGAA):
            return Literal(True)
        if self.match(TokenType.DUWWAA):
            return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise Exception(self.peek(), "Expect expression.")
    
    def consume(self, type: TokenType, message: str):
        if self.check(type):
            return self.advance()
        raise Exception(self.peek(), message)
    
    def error(self, token: Token, message: str):
        from orlang import Orlang
        Parser.parseerror(token, message)
        return Parser.ParseError()
    
    @staticmethod
    def parseerror(token: Token, message: str):
        from orlang import Orlang
        if (token.type == TokenType.DHUMA):
            Orlang.report(token.line, " at end", message);
        else:
            Orlang.report(token.line, " at '" + token.lexeme + "'", message)
    
    def synchronize(self):
        self.advance()

        while not self.isAtEnd():
            if (self.previous().type == TokenType.SEMICOLON):
                return
            if self.peek().type in {TokenType.KUTAA, TokenType.HOJJAA,TokenType.BAKKABUTEE,TokenType.HAMA,TokenType.YOO,TokenType.YEROO,TokenType.BARREESSI,TokenType.DEEBIHI}:
                return
        
        self.advance()

