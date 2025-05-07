
memoryAddress = 5000
tRegister = 0
vars = dict()
statementNumber = 0
forStatementNumber = 0
ifStatements = 0
forStatements = 0
data = ""
datanum = 0

def getInstructionLine(varName):
    global memoryAddress, tRegister
    tRegisterName = f"$r{tRegister}"
    setVariableRegister(varName, tRegisterName)
    returnText = f"addi {tRegisterName}, $zero, {memoryAddress}"
    tRegister += 1
    memoryAddress += 4
    return returnText

def setVariableRegister(varName, tRegister):
    global vars
    vars[varName] = tRegister

def getVariableRegister(varName):
    global vars
    if varName in vars:
        return vars[varName]
    else:
        return "ERROR"
    
def getAssignmentLinesImmediateValue(val, varName):
    global tRegister
    outputText = f"""addi $r{tRegister}, $zero, {val}\nsw $r{tRegister}, 0({getVariableRegister(varName)})"""
    tRegister += 1
    return outputText

def getAssignmentLinesVariable(varSource, varDest):
    global tRegister
    outputText = ""
    registerSource = getVariableRegister(varSource)
    outputText += f"lw $r{tRegister}, 0({registerSource})" + "\n"
    tRegister += 1
    registerDest = getVariableRegister(varDest)
    outputText += f"sw $r{tRegister-1}, 0({registerDest})"
    # tRegister += 1
    return outputText

def getIfStatement(expr):
    global tRegister, vars, statementNumber, ifStatements
    outputText = ""
    ifStatements += 1
    statementNumber += 1
    var1, expr, var2 = expr.split()
    varRegister1 = getVariableRegister(var1)
    varRegister2 = getVariableRegister(var2)
    if "==" in expr:
        outputText += f"bne {varRegister1}, {varRegister2}, AFTER{statementNumber}"
    elif ">=" in expr:
        outputText += f"blt {varRegister1}, {varRegister2}, AFTER{statementNumber}"
    elif "<=" in expr:
        outputText += f"bgt {varRegister1}, {varRegister2}, AFTER{statementNumber}"
    elif ">" in expr:
        outputText += f"ble {varRegister1}, {varRegister2}, AFTER{statementNumber}"
    elif "<" in expr:
        outputText += f"bge {varRegister1}, {varRegister2}, AFTER{statementNumber}"
    if "!=" in expr:
        outputText += f"beq {varRegister1}, {varRegister2}, AFTER{statementNumber}"
    return outputText


def getAssignment(expr):
    outputText = ""
    var, _, var1, operation, var2 = line.split()
    var2 = var2.replace(";", "")
    if not var1.isdigit():
        if operation == "+":
            outputText += f"addi {getVariableRegister(var)}, {getVariableRegister(var1)}, {var2}"
            return outputText
    return ""

def whileLoop(expr):
    global forStatements, forStatementNumber, vars
    statement = ""
    forStatements = forStatements + 1
    forStatementNumber += 1
    var1, expr, var2 = expr.split()
    varRegister1 = getVariableRegister(var1)
    varRegister2 = getVariableRegister(var2)
    if "==" in expr:
        statement += f"bne {varRegister1}, {varRegister2}, WHILE{forStatementNumber}"
    elif ">=" in expr:
        statement += f"blt {varRegister1}, {varRegister2}, WHILE{forStatementNumber}"
    elif "<=" in expr:
        statement += f"bgt {varRegister1}, {varRegister2}, WHILE{forStatementNumber}"
    elif ">" in expr:
        statement += f"ble {varRegister1}, {varRegister2}, WHILE{forStatementNumber}"
    elif "<" in expr:
        statement += f"bge {varRegister1}, {varRegister2}, WHILE{forStatementNumber}"
    elif "!=" in expr:
        statement += f"beq {varRegister1}, {varRegister2}, WHILE{forStatementNumber}"
    vars[forStatements] = statement
    return f"WHILE{forStatementNumber}:"

def modulo(expr):
    outputText = ""
    expr = expr.strip()
    expr = expr.replace(";", "")
    var1, equal, var2, percent, var3 = expr.split(" ")
    varRegister1 = getVariableRegister(var1)
    varRegister2 = getVariableRegister(var2)
    varRegister3 = getVariableRegister(var3)
    outputText += f"mod {varRegister1}, {varRegister2}, {varRegister3}"
    return(outputText)

def printf(expr):
    global data, vars, datanum
    outputText = ""
    datanum += 1
    if "%d" in expr:
        expr.strip()
        expr = expr.replace("(","").replace(")","").replace("{","").replace("\n", "")
        _, var1 = expr.split(", ")
        var1 = var1.replace(" ", "")
        varRegister1 = getVariableRegister(var1)
        outputText += f"sw $a0, {varRegister1}" + "\n"
        outputText += f"li $v0, 10" + "\n"
        outputText += "syscall"
        return outputText
    else:
        expr.strip()
        expr = expr.replace("(","").replace(")","").replace("{","").replace("\n", "")
        _, expr, _ = expr.split('"')
        outputText += f"sw $a0, $str{datanum}" + "\n"
        outputText += f"li $v0, 4" + "\n"
        outputText += "syscall"
        data += f'str{datanum}:     .asciiz     "{expr}"'
        data += "\n"
        return outputText

f = open("program7.c", "r")
lines = f.readlines()
outputText = ""
data = ""
for line in lines:
    # if line.startswith("if "):
    if "if" in line:
        _, expr = line.split("if ")
        expr = expr.replace("(","").replace(")","").replace("{","")
        outputText += getIfStatement(expr) + "\n"
    elif "else if" in line:
    # elif line.startswith("else if "):
        _, expr = line.split("if ")
        expr = expr.replace("(","").replace(")","").replace("{","")
        outputText += getIfStatement(expr) + "\n"
    # while loop
    elif line.startswith("while"):
        _, expr = line.split("while ")
        expr = expr.replace("(","").replace(")","").replace("{","")
        outputText += whileLoop(expr) + "\n"
    # end for/if
    # elif line.startswith("}"):
    elif "}" in line:
        if ifStatements > 0:
            outputText += f"AFTER{statementNumber}:" + "\n"
            ifStatements -= 1
        elif forStatements > 0:
            outputText += vars[forStatements] + "\n"
    # int declarations
    elif line.startswith("int "):
        _, var = line.split()
        var = var.strip(";")
        outputText += getInstructionLine(var) + "\n"
    # assignments
    elif "printf" in line:
        outputText += printf(line) + "\n"
    elif "%" in line:
        outputText += modulo(line) + "\n"
    elif "=" in line:
        if len(line.split()) == 3:
            varName, _, val = line.split()
        else:
            outputText += getAssignment(line) + "\n";
        val = val.strip(";")
        if val.isdigit():
            # immediately value assignments
            outputText += getAssignmentLinesImmediateValue(val, varName) + "\n"
        else:
            # variable assignments
            outputText += getAssignmentLinesVariable(val, varName) + "\n"
    else:
        pass
outputText = ".data" + "\n" + data + ".text" + "\n" + outputText
outputFile = open("output7.asm", "w")
outputFile.write(outputText)
