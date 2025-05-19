import sys
from typing import List, TextIO

def defineType(file: TextIO, baseName: str, className: str, fields:str):
    file.write(f"class {className}({baseName[0].upper() + baseName[1:]}):\n")
    file.write(f"   def __init__(self, {fields}) -> None:\n")
    fieldList = fields.split(", ")
    
    for field in fieldList:
        name = field.split(":")[0]
        file.write(f"       self.{name} = {name}\n")
    
    file.write("   def accept(self, visitor: 'Visitor') -> object:\n")
    file.write(f"       return visitor.visit{className}{baseName[0].upper() + baseName[1:]}(self)\n")

def defineVisitor(file: TextIO, baseName: str, types: List[str]):
    file.write("R = TypeVar('R')\n\n")
    file.write("class Visitor(ABC, Generic[R]):\n")
    for type in types:
        typeName = type.split("|")[0].strip()
        file.write("    @abstractmethod\n")
        file.write(f"    def visit{typeName}{baseName[0].upper() + baseName[1:]}(self, {baseName}: {typeName}) -> R:\n")
        file.write("        pass\n")
    file.write("\n")
    
def defineAst(outputDir: str, baseName: str, types: List[str]):
    path = outputDir + "/" + baseName + ".py"

    with open(path, "w") as f:
        f.write("from abc import ABC, abstractmethod\n")
        f.write("from .token import Token\n")
        f.write("from typing import TypeVar, Generic\n\n")
        f.write(f"class {baseName.capitalize()}(ABC):\n")
        f.write("   @abstractmethod\n")
        f.write("   def accept(self, visitor: 'Visitor') -> object:\n")
        f.write("       pass\n")
        f.write("\n")
        
        for type in types:
            className = type.split("|")[0].strip()
            fields = type.split("|")[1].strip()
            defineType(f, baseName, className, fields)
            f.write("\n")
        defineVisitor(f, baseName, types)
        
        
        

arguments = sys.argv[1:]

if len(arguments) != 1:
    print("Usage: generate_ast <output directory>", file=sys.stderr)
    sys.exit(64)

outputDir = arguments[0]
defineAst(outputDir, "expression", [
    "Assign   | name: Token, value: Expression",
    "Binary   | left: Expression, operator: Token, right: Expression",
    "Grouping | expression: Expression",
    "Literal  | value: object",
    "Unary    | operator: Token, right: Expression",
    "Variable | name: Token"
])

defineAst(outputDir, "statement", [
    "Block      | statements: List[Statement]",
    "ExpressionStatement | expression: Expression",
    "Print      | expression: Expression",
    "Var        | name: Token, initializer: Expression"
])