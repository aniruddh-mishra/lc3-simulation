class Computer:
    def __init__(self, monitor, keyboard, startAddress=int("3000", 16)):
        self.state = 18
        self.clockCount = 0
        self.registers = [intToBinarySigned(0)] * 8
        self.privelege = 0
        self.priorityLevel = 0
        self.memory = Memory(keyboard, monitor)
        self.startAddress = startAddress
        self.PC = startAddress # TODO starts at x0200 unless said otherwise
        self.IR = intToBinarySigned(0)
        self.nextState = self.state18
        self.BEN = True
        self.ACV = False
        self.INT = False
        self.conditionCodeBits = [False, False, True]
        self.savedSSP = int("3000", 16)
        # TODO self.savedUSP

        self.opCodes = {
            "0001": self.state01, # ADD
            "0101": self.state05, # AND
            "0000": self.state00, # BR
            "1100": self.state12, # JMP
            "0100": self.state04, # JSR
            "0010": self.state02, # LD
            "1010": self.state10, # LDI
            "0110": self.state06, # LDR
            "1110": self.state14, # LEA
            "1001": self.state09, # NOT
            # "1000": self.state08, # RTI
            "0011": self.state03, # ST
            "1011": self.state11, # STI
            "0111": self.state07, # STR
            "1111": self.state15, # TRAP
        }
        """
                                "1101": self.state13  # reserved
                }
        """
        self.monitor = monitor
        self.keyboard = keyboard

    def smallStep(self):
        self.clockCount += 1
        self.nextState()

    def reset(self):
        self.__init__(self.monitor, self.keyboard, self.startAddress)
        self.keyboard.data = 0 
        self.keyboard.status = 0 
        self.monitor.data = 0 
        self.monitor.status = 1 << 15

    def setACV(self):
        self.ACV = (self.memory.mar < int("3000", 16) or self.memory.mar >= int("FE00", 16)) & self.privelege
   
    def setCC(self, number):
        self.conditionCodeBits = [False, False, False]
        number = binaryToIntSigned(number)
        if number > 0:
            self.conditionCodeBits[2] = True
        elif number < 0:
            self.conditionCodeBits[0] = True
        else:
            self.conditionCodeBits[1] = True

    def state18(self):
        self.memory.setMAR(intToBinarySigned(self.PC))
        self.PC += 1 
        self.setACV()
        if self.INT:
            # TODO make interrupt FSM states
            pass
        else:
            self.nextState = self.state33

    def state33(self):
        if self.ACV:
            # TODO make ACV FSM states
            pass
        else: 
            self.nextState = self.state28

    def state28(self):
        self.memory.readMemory()

        if self.memory.isMemoryReady:
            self.nextState = self.state30

    def state30(self):
        self.IR = self.memory.mdr
        self.nextState = self.state32

    def state32(self):
        N, Z, P = self.conditionCodeBits
        self.BEN = (int(self.IR[4]) & N) or (int(self.IR[5]) & Z) or (int(self.IR[6]) & P)
        self.nextState = self.opCodes.get(self.IR[0:4])

    def state01(self):
        SR1 = binaryToIntUnsigned(self.IR[7:10])
        DR = binaryToIntUnsigned(self.IR[4:7])
        bit5 = binaryToIntUnsigned(self.IR[10])
        if bit5:
            val2 = self.signExtend(self.IR[11:16])
        else:
            SR2 = binaryToIntUnsigned(self.IR[13:16])
            val2 = self.registers[SR2]

        result = binaryToIntSigned(self.registers[SR1]) + binaryToIntSigned(val2)
        self.registers[DR] = intToBinarySigned(result)
        self.nextState = self.state18

    def state05(self):
        SR1 = binaryToIntUnsigned(self.IR[7:10])
        DR = binaryToIntUnsigned(self.IR[4:7])
        bit5 = binaryToIntUnsigned(self.IR[10])
        if bit5:
            val2 = self.signExtend(self.IR[11:16])
        else:
            SR2 = binaryToIntUnsigned(self.IR[13:16])
            val2 = self.registers[SR2]

        result = binaryToIntSigned(self.registers[SR1]) & binaryToIntSigned(val2)
        self.registers[DR] = intToBinarySigned(result)
        self.nextState = self.state18

    def state00(self):
        if self.BEN:
            self.nextState = self.state22
        else:
            self.nextState = self.state18

    def state22(self):
        self.PC += binaryToIntSigned(self.signExtend(self.IR[7:]))
        if self.PC < 0:
            self.PC += 2**16
        self.nextState = self.state18

    def state12(self):
        pass

    def state04(self):
        if int(self.IR[11]):
            self.nextState = self.state21
        else:
            self.nextState = self.state20

    def state21(self):
        self.registers[7] = intToUnsignedBinary(self.PC)
        self.PC += self.IR[5:]
        self.nextState = self.state18

    def state20(self):
        self.registers[7] = intToUnsignedBinary(self.PC)
        # TODO check where BaseR is in IR
        self.nextState = self.state18

    def state02(self):
        self.memory.setMAR(intToUnsignedBinary(self.PC + binaryToIntSigned(self.IR[7:])))
        self.setACV()
        self.nextState = self.state35

    def state35(self):
        if self.ACV:
            # TODO make ACV FSM states
            pass
        else:
            self.nextState = self.state25

    def state25(self):
        self.memory.readMemory()

        if self.memory.isMemoryReady:
            self.nextState = self.state27

    def state27(self):
        self.registers[binaryToIntUnsigned(self.IR[4:7])] = self.memory.mdr
        self.setCC(self.memory.mdr)
        self.nextState = self.state18

    def state10(self):
        self.memory.setMAR(intToUnsignedBinary(self.PC + binaryToIntSigned(self.IR[7:])))
        self.setACV()
        self.nextState = self.state17

    def state17(self):
        if self.ACV:
            # TODO make ACV FSM states
            pass
        else:
            self.nextState = self.state24

    def state24(self):
        self.memory.readMemory()

        if self.memory.isMemoryReady:
            self.nextState = self.state26

    def state26(self):
        self.memory.setMAR(self.memory.mdr)
        self.setACV()
        self.nextState = self.state35

    def state06(self):
        base = self.registers[binaryToIntUnsigned(self.IR[7:10])]
        base = binaryToIntUnsigned(base)
        offset = binaryToIntSigned(self.signExtend(self.IR[10:]))
        self.memory.setMAR(intToUnsignedBinary(base + offset))
        self.setACV()
        self.nextState = self.state35

    def state14(self):
        self.registers[binaryToIntUnsigned(self.IR[4:7])] = intToUnsignedBinary(self.PC + binaryToIntSigned(self.IR[7:]))
        self.nextState = self.state18

    def state09(self):
        value = self.registers[binaryToIntUnsigned(self.IR[7:10])]
        result = intToUnsignedBinary(~binaryToIntUnsigned(value))
        self.registers[binaryToIntUnsigned(self.IR[4:7])] = result
        self.nextState = self.state18

    def state03(self):
        self.memory.setMAR(intToUnsignedBinary(self.PC + binaryToIntSigned(self.IR[7:])))
        self.setACV()
        self.nextState = self.state23

    def state23(self):
        self.memory.mdr = self.registers[binaryToIntUnsigned(self.IR[4:7])]

        if self.ACV:
            # TODO make ACV FSM states
            pass
        else:
            self.nextState = self.state16

    def state16(self):
        self.memory.writeMemory()

        if self.memory.isMemoryReady:
            self.nextState = self.state18

    def state11(self):
        self.memory.setMAR(intToUnsignedBinary(self.PC + binaryToIntSigned(self.IR[7:])))
        self.setACV()
        self.nextState = self.state19

    def state19(self):
        if self.ACV:
            # TODO make ACV FSM states
            pass
        else:
            self.nextState = self.state29

    def state29(self):
        self.memory.readMemory()

        if self.memory.isMemoryReady:
            self.nextState = self.state31

    def state31(self):
        self.memory.setMAR(self.memory.mdr)
        self.setACV()
        self.nextState = self.state23

    def state07(self):
        base = self.registers[binaryToIntUnsigned(self.IR[7:10])]
        base = binaryToIntUnsigned(base)
        offset = binaryToIntSigned(self.signExtend(self.IR[10:]))
        self.memory.setMAR(intToUnsignedBinary(base + offset))
        self.setACV()
        self.nextState = self.state23

    def state15(self):
        self.table = format(0, "08b")
        self.PC += 1 
        self.memory.mdr = self.getPSR()
        self.nextState = self.state47

    def state47(self):
        self.vector = self.IR[8:] 
        if self.privelege:
            self.nextState = self.state45
        else:
            self.nextState = self.state37
        self.privelege = 0

    def state45(self):
        self.savedUSP = self.registers[5]
        self.registers[5] = self.savedSSP
        self.nextState = self.state37 

    def state37(self):
        self.registers[5] -= 1
        self.memory.setMAR(intToUnsignedBinary(self.registers[5]))
        self.nextState = self.state41

    def state41(self):
        self.memory.readMemory()

        if self.memory.isMemoryReady:
            self.nextState = self.state43

    def state43(self):
        self.memory.mdr = self.PC - 1

    def signExtend(self, binary):
        signBit = binary[0]
        return signBit * (16 - len(binary)) + binary
    
    def getPSR(self):
        nzp = str(int(self.conditionCodeBits[0])) + str(int(self.conditionCodeBits[1])) + str(int(self.conditionCodeBits[2]))
        return str(self.privelege) + "0" * 4 + format(self.priorityLevel, "03b") + "0" * 5 + nzp

    
class Memory:
    def __init__(self, keyboard, monitor):
        self.mar = 0
        self.mdr = 0 # public read and write
        self.memory = [intToBinarySigned(0)] * (2 ** 16)
        self.isMemoryReady = False
        self.cyclesComplete = 0
        self.memoryCycles = 5
        self.keyboard = keyboard
        self.monitor = monitor
        # TODO Fix memory mapped addresses
        self.memoryMappedIO = {
                                int("FE00", 16): [keyboard.getStatus, keyboard.setStatus],
                                int("FE02", 16): [keyboard.getData, keyboard.setData],
                                int("FE01", 16): [monitor.getStatus, monitor.setStatus],
                                int("FE03", 16): [monitor.getData, monitor.setData]
        }
        self.loadCode()

    def loadCode(self):
        return
        fileName = input("Filename: ")
        with open(fileName, "r") as f:
            code = f.read().split('\n')
        address = int(code[0], 2)
        for instruction in code[1:]:
            self.memory[address] = instruction
            address += 1
        
    def setMAR(self, address):
        self.mar = binaryToIntUnsigned(address)
        self.isMemoryReady = False

    def readMemory(self):
        self.cyclesComplete += 1 
        if self.cyclesComplete == self.memoryCycles:
            if self.mar not in self.memoryMappedIO.keys():
                self.mdr = self.memory[self.mar]
            else:
                self.mdr = self.memoryMappedIO[self.mar][0]()

            self.cyclesComplete = 0 
            self.isMemoryReady = True

    def getMemory(self, index):
        if index not in self.memoryMappedIO.keys():
            return self.memory[index]
        else:
            if index == int("FE02", 16):
                return format(self.keyboard.data, "016b")
            return self.memoryMappedIO[index][0]()


    def writeMemory(self): 
        self.cyclesComplete += 1 
        if self.cyclesComplete == self.memoryCycles:
            if self.mar not in self.memoryMappedIO.keys():
                self.memory[self.mar] = self.mdr
            else:
                self.memoryMappedIO[self.mar][1](self.mdr)

            self.cyclesComplete = 0 
            self.isMemoryReady = True

def binaryToIntUnsigned(binary):
    return int(binary, 2)

def binaryToIntSigned(binary):
    convertedInt = binaryToIntUnsigned(binary)
    if binary[0] == "1":
        convertedInt -= 2 ** 16
    return convertedInt

def intToUnsignedBinary(integer):
    return format(integer, "016b")

def intToBinarySigned(integer):
    if integer < 0:
        integer += 2**16

    binary = intToUnsignedBinary(integer)
    
    return binary
