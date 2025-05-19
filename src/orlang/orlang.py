import sys
from .scanner import Scanner
from .parser import Parser
from .interpreter import Interpreter

class Orlang:
    # error handling
    hadError = False
    hadRuntimeError = False
    interpreter = Interpreter()

    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)

    @staticmethod
    def error(line: int, message: str) -> None:
        Orlang.report(line, "", message)

    @staticmethod
    def runtimeError(error) -> None:
        print(f"{error}\n[line {error.token.line}]", file=sys.stderr)
        Orlang.hadRuntimeError = True

    @staticmethod
    def run(source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scanTokens()
        parser = Parser(tokens)
        statements = parser.parse()

        if Orlang.hadError:
            return

        Orlang.interpreter.interpret(statements)

    @staticmethod
    def runFile(path: str) -> None:
        code = open(path).read()
        Orlang.run(code)
        if Orlang.hadError:
            sys.exit(65)
        if Orlang.hadRuntimeError:
            sys.exit(70)

    @staticmethod
    def runPrompt() -> None:
        while True:
            try:
                line = input("> ")
                if not line:
                    break
                Orlang.run(line)
                Orlang.hadError = False
            except EOFError:
                break

    @staticmethod
    def entry() -> None:
        # print("orlang ", end="")
        arguments = sys.argv[1:]
        if len(arguments) > 1:
            print("Usage: orlang [script]")
            sys.exit(64)
        elif len(arguments) == 1:
            Orlang.runFile(arguments[0])
        else:
            Orlang.runPrompt()

def main() -> None:
    Orlang.entry()

if __name__ == "__main__":
    main()