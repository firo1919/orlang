from typing import List
from orlang_token import Token
from tokenType import TokenType
from typing import Dict

class Scanner:
    
    KEYWORDS: Dict[str, TokenType] = {
        "fi":       TokenType.FI,
        "kutaa":     TokenType.KUTAA,
        "kanbiroo":      TokenType.KANBIROO,
        "soba":     TokenType.SOBA,
        "hama":       TokenType.HAMA,
        "hojjaa":       TokenType.HOJJAA,
        "yoo":        TokenType.YOO,
        "duwwaa":       TokenType.DUWWAA,
        "ykn":        TokenType.YKN,
        "barreessi":     TokenType.BARREESSI,
        "deebihi":    TokenType.DEEBIHI,
        "olaanoo":     TokenType.OLAANOO,
        "kana":      TokenType.KANA,
        "dhugaa":      TokenType.DHUGAA,
        "bakkabutee":       TokenType.BAKKABUTEE,
        "yeroo":     TokenType.YEROO,
    }
    
    def __init__(self, source: str) -> None:
        self.__tokens: List[Token] = []
        self.__source: str = source
        self.__start: int = 0
        self.__current: int = 0
        self.__line: int = 1
    
    def isAtEnd(self) -> bool:
        return self.__current >= len(self.__source)
    
    def advance(self) -> str:
        self.__current += 1
        return self.__source[self.__current - 1]
        
    def addToken(self, type: TokenType, literal: object = None) -> None:
        text: str = self.__source[self.__start:self.__current]
        self.__tokens.append(Token(type, text, self.__line, literal))
      
    def scanToken(self) -> None:
        c: str = self.advance()
        if c == '(':
            self.addToken(TokenType.LEFT_PAREN)
        elif c == ')':
            self.addToken(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.addToken(TokenType.LEFT_BRACE)
        elif c == '}':
            self.addToken(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.addToken(TokenType.COMMA)
        elif c == '.':
            self.addToken(TokenType.DOT)
        elif c == '-':
            self.addToken(TokenType.MINUS)
        elif c == '+':
            self.addToken(TokenType.PLUS)
        elif c == ';':
            self.addToken(TokenType.SEMICOLON)
        elif c == '*':
            self.addToken(TokenType.STAR)
        elif c == '!':
            self.addToken(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif c == '=':
            self.addToken(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif c == '<':
            self.addToken(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif c == '>':
            self.addToken(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        elif c == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.isAtEnd():
                    self.advance()
            else:
                self.addToken(TokenType.SLASH)
        elif c in {' ', '\r', '\t'}:
            # Ignore whitespace.
            pass
        elif c == '\n':
            self.__line += 1
        elif c == '"':
            self.string()      
        else:
            if c.isdigit():
                self.number()
            elif c.isalpha():
                self.identifier()
            else:
                from orlang import Orlang
                Orlang.error(self.__line, "Unexpected character.")
                
    def identifier(self) -> None:
        while self.peek().isalnum():
            self.advance()
        text: str = self.__source[self.__start:self.__current]
        type = Scanner.KEYWORDS.get(text)
        if type is None:
            type = TokenType.IDENTIFIER
        self.addToken(type)
        
    def number(self) -> None:
        while self.peek().isdigit():
            self.advance()
        # Look for a fractional part.
        if self.peek() == '.' and self.peekNext().isdigit():
            # Consume the "."
            self.advance()
            while self.peek().isdigit():
                self.advance()
        self.addToken(TokenType.NUMBER, float(self.__source[self.__start:self.__current]))
    
    def peekNext(self) -> str:
        if self.__current + 1 >= len(self.__source):
            return '\0'
        return self.__source[self.__current + 1]
    
    def string(self) -> None:
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == '\n':
                self.__line += 1
            self.advance()
        if self.isAtEnd():
            from orlang import Orlang
            Orlang.error(self.__line, "Unterminated string.")
            return
        # The closing ".
        self.advance()
        # Trim the surrounding quotes.
        value: str = self.__source[self.__start + 1:self.__current - 1]
        self.addToken(TokenType.STRING, value)

    def peek(self) -> str:
        if self.isAtEnd():
            return '\0'
        return self.__source[self.__current]
    
    def match(self, expected: str) -> bool:
        if self.isAtEnd():
            return False
        if self.__source[self.__current] != expected:
            return False
        self.__current += 1
        return True

    def scanTokens(self) -> List[Token]:
        while not self.isAtEnd():
            self.__start = self.__current
            self.scanToken()
        self.__tokens.append(Token(TokenType.DHUMA, "", self.__line, None))
        return self.__tokens