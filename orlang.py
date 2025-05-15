import sys
from typing import List
from scanner import Scanner
from parser import Parser
from astprinter import AstPrinter

class Orlang:
    # error handling
    hadError = False

    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)

    @staticmethod
    def error(line: int, message: str) -> None:
        Orlang.report(line, "", message)

    @staticmethod
    def run(source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scanTokens()
        parser = Parser(tokens)
        expression = parser.parse()

        if Orlang.hadError:
            return

        print(AstPrinter().print(expression))

    @staticmethod
    def runFile(path: str) -> None:
        code = open(path).read()
        Orlang.run(code)
        if Orlang.hadError:
            sys.exit(65)

    @staticmethod
    def runPrompt() -> None:
        while True:
            line = input("> ")
            if not line:
                break
            Orlang.run(line)
            Orlang.hadError = False

    @staticmethod
    def entry() -> None:
        print("orlang ",end="")
        arguments = sys.argv[1:]
        if len(arguments) > 1:
            print("Usage: orlang [script]")
            sys.exit(64)
        elif len(arguments) == 1:
            Orlang.runFile(arguments[0])
        else:
            Orlang.runPrompt()

if __name__ == "__main__":
    Orlang.entry()
