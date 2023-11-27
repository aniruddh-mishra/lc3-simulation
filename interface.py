opCodes = {
        'add': '0001' + '2' * 3 + '3' * 3 + '4' * 6,
        'and': '0101' + '2' * 3 + '3' * 3 + '4' * 6,
        'br': '0000' + '2' * 3 + '3' * 9,
        'jmp': '1100' + '0' * 3 + '2' * 3 + '0' * 6,
        'jsr': '0100' + '1' + '2' * 11,
        'jsrr': '0100' + '0' * 3 + '2' * 3 + '0' * 6,
        'ld': '0010' + '2' * 3 + '3' * 9,
        'ldi': '1010' + '2' * 3 + '3' * 9,
        'ldr': '0110' + '2' * 3 + '3' * 3 + '4' * 6,
        'lea': '1110' + '2' * 3 + '3' * 9,
        'not': '1001' + '2' * 3 + '3' * 3 + '1' * 6,
        'ret': '1100' + '0' * 3 + '1' * 3 + '0' * 6,
        'rti': '1000' + '0' * 12,
        'st': '0011' + '2' * 3 + '3' * 9,
        'sti': '1011' + '2' * 3 + '3' * 9,
        'str': '0111',
        'trap': '1111'
        }

registers = {
        'r0': '000',
        'r1': '001',
        'r2': '010',
        'r3': '011',
        'r4': '100',
        'r5': '101',
        'r6': '110',
        'r7': '111'
        }

def assemble(fileName):
    with open(fileName, "r") as f:
        code = f.read().lower()
        code = code.split(".end")

    # Clean code
    for segment in code:
        segment = segment.strip()
        segment = segment.split('\n')
        segment = [line for line in segment if line.replace(' ', '').replace('\t', '')]
        convertCode(segment)

def convertCode(code):
    if not len(code):
        return False
   
    # Check .ORIG value
    if ".orig" not in code[0]:
        print("Code must start with a .ORIG address")
        return False

    machineCode = []

    startingAddress = convertToInteger(code[0].replace(".orig", ''))

    symbolTable = firstCycle(startingAddress, code[1:])
    
    if symbolTable == -1:
        return

    machineCode = secondCycle(symbolTable, startingAddress, code[1:])
    
    if not machineCode:
        return

    print(machineCode)

def firstCycle(programCounter, code):
    symbolTable = {}
    for line in code:
        line = line.strip().split(' ')
        if line[0] not in opCodes.keys() and line[0]:
            if symbolTable.get(line[0]):
                print("Can not use a label more than once")
                return -1
            symbolTable[line[0]] = programCounter
        programCounter += 1

    return symbolTable

def secondCycle(symbolTable, programCounter, code):
    machineCode = []
    machineCode.append(format(startingAddress, "016b"))
    for line in code:
        arguments = []
        line = line.strip().replace(',', '').split(' ')
        if line[0] == 'and' or line[0] == 'add':
            arguments.extend([registers[register] for register in line[1:3]])
            if registers.get(line[3]):
                arguments.append('000' + registers[line[3]])
            else:
                binary = convertTo2sCompliment(line[3], 5, programCounter)
                if not binary:
                    return False
                
                arguments.append('1' + binary)

        programCounter += 1

        machineCode.append(synthesizeLine(line[0], arguments))

    return machineCode
           
def synthesizeLine(opCode, args):
    machineCode = opCodes[opCode]
    argPos = 2
    for arg in args:
        machineCode.replace(str(argPos) * len(arg), arg)
        argPos += 1

    return machineCode

def convertToInteger(number):
    if "x" in number:
        return int(number.replace("x", ""), 16)
    elif "#" in number:
        return int(number.replace("#", ""))
    else:
        return int(number)

def convertTo2sCompliment(number, bits, programCounter):
    binary = format(abs(number), '0' + str(bits) + 'b')
    if len(binary) > bits or binary[0] == 1:
        print('In instruction at address ' + str(programCounter) + ' the number can not be converted to binary with set number of bits')
        return

    if number < 0:
        binary = ~int(binary, 2) + 1
        binary = format(binary, '0' + str(bits) + 'b')

    return binary

# assemble('test.asm')
print(convertTo2sCompliment(-2, 3, 3))
