import sys
from typing import List

hadError: bool = False

# error handling
def error(line: int, message: str) -> None:
    __report(line, "", message)

def __report(line: int, where: str, message: str) -> None:
    print(f"[line {line} ] Error {where} : {message}", file=sys.stderr)

def scanTokens(source: str) -> List[str]:
    return source.split(" ")

# the code executers
def run(source: str) -> None:
    tokens = scanTokens(source)
    
    for token in tokens:
        print(token)

def runFile(path: str) -> None:
    file = open(path).read()
    run(file)
    if hadError:
        sys.exit(65)

def runPrompt() -> None:
    while True:
        print("> ")
        line = input()
        if line is None or line == "":
            break
        run(line) 
        hadError = False

# entry point for the language
def entry() -> None:
    arguments = input('orlang > ').split()
    if len(arguments) > 1:
        print("Usage: orlang [script]")
        sys.exit(64)
    elif len(arguments) == 1:
        runFile(arguments[0])
    else:
        runPrompt()
    
entry()
