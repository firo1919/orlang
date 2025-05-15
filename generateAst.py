import sys
from typing import List, TextIO

def defineType(file: TextIO, baseName: str, className: str, fields:str):
    file.write(f"class {className}({baseName}):\n")
    file.write(f"   def __init__(self, {fields}) -> None:\n")
    fieldList = fields.split(", ")
    
    for field in fieldList:
        name = field.split(":")[0]
        file.write(f"       self.{name} = {name}\n")
    
    file.write("   def accept(self, visitor: 'Visitor') -> R:\n")
    file.write(f"       return visitor.visit{className}{baseName}(self)\n")

def defineVisitor(file: TextIO, baseName: str, types: List[str]):
    file.write("class Visitor(ABC, Generic[R]):\n")
    for type in types:
        typeName = type.split("|")[0].strip()
        file.write(f"    @abstractmethod\n")
        file.write(f"    def visit{typeName}{baseName}(self, {baseName.lower()}: {typeName}) -> R:\n")
        file.write(f"        pass\n")
    file.write("\n")
    
def defineAst(outputDir: str, baseName: str, types: List[str]):
    path = outputDir + "/" + baseName + ".py"

    with open(path, "a") as f:
        f.write("from abc import ABC, abstractmethod\n")
        f.write("from orlang_token import Token\n")
        f.write("from typing import TypeVar, Generic\n\n")
        f.write("R = TypeVar('R')\n\n")
        f.write(f"class {baseName.capitalize()}(ABC):\n")
        f.write("   @abstractmethod\n")
        f.write("   def accept(self, visitor: 'Visitor') -> R:\n")
        f.write("       pass\n")
        f.write("\n")
        
        for type in types:
            className = type.split("|")[0].strip()
            fields = type.split("|")[1].strip()
            defineType(f, baseName.capitalize(), className.capitalize(), fields)
            f.write("\n")
        defineVisitor(f, baseName.capitalize(), types)
        
        
        

arguments = sys.argv[1:]

if len(arguments) != 1:
    print("Usage: generate_ast <output directory>", file=sys.stderr)
    sys.exit(64)

outputDir = arguments[0]
defineAst(outputDir, "expression", [
      "Binary   | left: Expression, operator: Token, right:Expression",
      "Grouping | expression: Expression",
      "Literal  | value: object",
      "Unary    | operator: Token, right: Expression"
    ])