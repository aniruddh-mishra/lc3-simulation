class Computer:
    def __init__(self, monitor, keyboard, startAddress=int("200", 16)):
        """
        self.state = 18
        self.registers = [format(0, "016b")] * 8
        self.memory = Memory() 
        self.PC = startAddress # starts at x0200 unless said otherwise
        self.IR = format(0, "016b")
        self.nextState = state18
        self.BEN = True
        self.ACV = False
        self.INT = False
        self.conditionCodeBits = (False, False, True)

        self.opCodes = {
                "0001": state01, # ADD
                "0101": state05, # AND
                "0000": state00, # BR
                "1100": state12, # JMP
                "0100": state04, # JSR
                "0010": state02, # LD
                "1010": state10, # LDI
                "0110": state06, # LDR
                "1110": state14, # LEA
                "1001": state09, # NOT
                "1000": state08, # RTI
                "0011": state03, # ST
                "1011": state11, # STI
                "0111": state07, # STR
                "1111": state15, # TRAP
                "1101": state13  # reserved
                }
        """
        self.monitor = monitor
        self.keyboard = keyboard

    def setACV(self):
        self.ACV = self.memory.mar < int("3000", 16) or self.memory.mar > int("FE00", 16)
    
    """
    def state18(self):
        self.memory.setMAR(self.PC)
        self.PC += 1 
        self.setACV()
        if self.INT:
            # TODO make interrupt FSM states
            pass
        else:
            self.nextState = state33

    def state33(self):
        if self.ACV:
            # TODO make ACV FSM states
            pass
        else: 
            self.nextState = state28

    def state28(self):
        self.memory.readMemory()
        # TODO check if memory read
        self.nextState = state30

    def state30(self):
        self.IR = self.memory.mdr
        self.nextState = state32

    def state32(self):
        N, Z, P = self.conditionCodeBits
        BEN = (IR[11] & N) or (int(IR[10]) & Z) or (int(IR[9]) & P)
        # TODO check opcode for next state

    def state01(self):
        SR1 = int(IR[6:9], 2)
        DR = int(IR[9:12], 2)
        bit5 = int(IR[5])
        if bit5:
            val2 = int(IR[0:5], 2)
        else:
            SR2 = int(IR[0:3], 2)
            val2 = self.registers[SR2]

        result = self.registers(SR1) + val2
        self.registers[DR] = result
    """

class Memory:
    def __init__(self):
        self.mar = 0
        self.mdr = 0 # public read and write
        self.memory = [format(0, "016b")] * (2 ** 16)
        self.isMemoryRead = False
        self.readCyclesComplete = 0
        self.memoryReadCycles = 5

    def setMAR(self, address):
        self.mar = int(address, 2)
        self.isMemoryRead = False

    def readMemory(self):
        self.mdr = self.memory[self.mar]
        self.readCyclesComplete += 1 
        if self.readCyclesComplete == self.memoryReadCycles:
            self.readCyclesComplete = 0 
            self.isMemoryRead = True

    def writeMemory(self):
        self.memory[self.mar] = self.mdr
