def scanTokens(source):
    return source.split(" ")
    

def run(source):
    tokens = scanTokens(source)
    
    for token in tokens:
        print(token)

def runFile(path):
    file = open(path).read()
    run(file)

def runPrompt():
    
    while True:
        print("> ")
        line = input()
        if line == None or line == "":
            break
        run(line) 

def entry():
    arguments = input('orlang > ').split()
    if len(arguments) > 1:
        print("Usage: orlang [script]")
        exit(64)
    elif len(arguments) == 1:
        runFile(arguments[0])
    else:
        runPrompt()
    
entry()
        