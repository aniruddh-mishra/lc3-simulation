class Computer:
    def __init__(self, monitor, keyboard, startAddress=int("3000", 16)):
        self.state = 18
        self.registers = [format(0, "016b")] * 8
        self.memory = Memory() 
        self.PC = startAddress # starts at x0200 unless said otherwise
        self.IR = format(0, "016b")
        self.nextState = self.state18
        self.BEN = True
        self.ACV = False
        self.INT = False
        self.conditionCodeBits = [False, False, True]

        self.opCodes = {
                "0001": self.state01, # ADD
        }
        """
                "0101": self.state05, # AND
                "0000": self.state00, # BR
                "1100": self.state12, # JMP
                "0100": self.state04, # JSR
                "0010": self.state02, # LD
                "1010": self.state10, # LDI
                "0110": self.state06, # LDR
                "1110": self.state14, # LEA
                "1001": self.state09, # NOT
                "1000": self.state08, # RTI
                "0011": self.state03, # ST
                "1011": self.state11, # STI
                "0111": self.state07, # STR
                "1111": self.state15, # TRAP
                "1101": self.state13  # reserved
                }
        """
        self.monitor = monitor
        self.keyboard = keyboard

    def setACV(self):
        self.ACV = self.memory.mar < int("3000", 16) or self.memory.mar > int("FE00", 16)
   
    def setCC(self, number):
        self.conditionCodeBits = [False, False, False]
        number = self.binaryToIntSigned(number)
        if number > 0:
            self.conditionCodeBits[2] = True
        elif number < 0:
            self.conditionCodeBits[0] = True
        else:
            self.conditionCodeBits[1] = True

    def state18(self):
        self.memory.setMAR(format(self.PC, "016b"))
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
        # TODO check if memory read
        if self.memory.isMemoryReady:
            self.IR = self.memory.mdr
            self.nextState = self.state30

    def state30(self):
        self.IR = self.memory.mdr
        self.nextState = self.state32

    def state32(self):
        N, Z, P = self.conditionCodeBits
        BEN = (int(self.IR[4]) & N) or (int(self.IR[5]) & Z) or (int(self.IR[6]) & P)
        self.nextState = self.opCodes[self.IR[0:4]]

    def state01(self):
        SR1 = int(self.IR[7:10], 2)
        DR = int(self.IR[4:7], 2)
        bit5 = int(self.IR[10])
        if bit5:
            val2 = self.signExtend(self.IR[11:16])
        else:
            SR2 = int(self.IR[13:16], 2)
            val2 = self.registers[SR2]

        result = self.binaryToIntSigned(self.registers[SR1]) + self.binaryToIntSigned(val2)
        self.registers[DR] = format(result, "016b")
        self.nextState = self.state18
        print(int(self.registers[DR], 2))

    def signExtend(self, binary):
        signBit = binary[0]
        return signBit * (16 - len(binary)) + binary

    def binaryToIntSigned(self, binary):
        convertedInt = int(binary, 2)
        if binary[0] == "1":
            convertedInt -= 2**15
        return convertedInt

class Memory:
    def __init__(self):
        self.mar = 0
        self.mdr = 0 # public read and write
        self.memory = [format(0, "016b")] * (2 ** 16)
        self.isMemoryReady = False
        self.cyclesComplete = 0
        self.memoryCycles = 5

    def setMAR(self, address):
        self.mar = int(address, 2)
        self.isMemoryRead = False

    def readMemory(self):
        self.mdr = self.memory[self.mar]

        self.cyclesComplete += 1 
        if self.cyclesComplete == self.memoryCycles:
            self.cyclesComplete = 0 
            self.isMemoryReady = True

    def writeMemory(self):
        self.memory[self.mar] = self.mdr

        self.cyclesComplete += 1 
        if self.cyclesComplete == self.memoryCycles:
            self.cyclesComplete = 0 
            self.isMemoryReady = True

