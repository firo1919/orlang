from enum import Enum, auto

class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # One or two character tokens.
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals.
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords.
    FI = auto()
    KUTAA = auto()
    KANBIROO = auto()
    SOBA = auto()
    HOOJJAA = auto()
    HAMA = auto()
    YOO = auto()
    DUWWAA = auto()
    YKN = auto()
    BARREESSI = auto()
    DEEBIHI = auto()
    OLAANOO = auto()
    KANA = auto()
    DHUGAA = auto()
    BAKKABUTEE = auto()
    YEROO = auto()

    # End of file.
    DHUMA = auto()
