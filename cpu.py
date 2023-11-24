class Computer:
    def __init__(self, startAddress=int("200", 16)):
        self.state = 18
        self.registers = [0] * 8
        self.memory = Memory() 
        self.PC = startAddress # starts at x0200 unless said otherwise
        self.IR = format(0, "016b")
        self.nextState = state18

    def state18(self):
        self.memory.setMAR = self.PC 
        self.PC += 1 
        # TODO set ACV
        # TODO check interrupt signal
        self.nextState = state33

    def state33(self):
        # TODO check ACV
        self.nextState = state28

    def state28(self):
        self.memory.readMemory()
        # TODO check if memory read
        self.nextState = state30

    def state30(self):
        self.IR = self.memory.mdr
        self.nextState = state32

    def state32(self):
        # TODO set BEN = IR[11] & N + IR[10] & Z + IR[9] & P
        # TODO check opcode for next state 
    


class Memory:
    def __init__(self):
        self.mar = 0
        self.mdr = 0 # public read and write
        self.memory = [0] * (2 ** 16)

    def setMAR(self, address):
        self.mar = int(address, 2)

    def readMemory(self):
        self.mdr = self.memory[self.mar]

    def writeMemory(self):
        self.memory[self.mar] = self.mdr
