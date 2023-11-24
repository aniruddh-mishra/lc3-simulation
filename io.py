import getch
import time

class IODevice:
    def __init__(self):
        self.status = 0 
        self.data = 0

    def getStatus(self):
        return format(self.status, "016b") # 016 means 16 digits with leading 0s 

    def setStatus(self, status):
        self.status = int(status, 2)

    def getData(self):
        return format(self.data, "016b") # 016 means 16 digits with leading 0s 
    
    def setData(self, data):
        self.data = int(data, 2)

class Monitor(IODevice):
    def __init__(self):
        self.status = 1 << 15
        self.data = 0
    
    def writeCharacter(self, character):
        if not (self.status & 1 << 15):
            return

        self.data = ord(character)
        self.status &= ~ (1 << 15)

    def printFromData(self):
        if not (self.status & 1 << 15):
            print(chr(self.data), end="", flush=True)
        
        self.status |= 1 << 15 

class Keyboard(IODevice):
    def writeCharacter(self, character):
        if self.status & 1 << 15:
            return

        self.data = ord(character)
        self.status |= 1 << 15

    def getData(self):
        self.status &= ~(1 << 15)
        return format(self.data, "016b") # 016 means 16 digits with leading 0s 

def pollKeyboard(keyboard):
    while True:
        character = getch.getch()
        keyboard.writeCharacter(character)

def updateMonitor(monitor):
    while True:
        monitor.writeCharacter("a")
        time.sleep(0.1)
        monitor.printFromData()

monitor = Monitor()
updateMonitor(monitor)
