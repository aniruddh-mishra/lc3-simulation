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
    def __init__(self, refreshRate):
        super().__init__()
        self.status = 1 << 15
        self.delay = 1 / refreshRate
    
    def writeCharacter(self, character):
        if not (self.status & 1 << 15):
            return

        self.data = character 
        self.status &= ~ (1 << 15)

    def printFromData(self, display):
        if not (self.status & 1 << 15):
            display.configure(state="normal")
            try:
                if self.data == 8:
                    display.delete("end-2c", "end")
                elif self.data == 13:
                    display.insert("end", "\n")
                else:
                    display.insert("end", chr(self.data))
            except:
                display.insert("end", "☒")
            display.configure(state="disabled")
            display.see("end")

        self.status |= 1 << 15

    def setData(self, data):
        self.data = int(data, 2)
        self.status &= ~(1 << 15)

class Keyboard(IODevice):
    def writeCharacter(self, character):
        if self.status & 1 << 15:
            return

        self.data = ord(character)
        self.status |= 1 << 15

    def getData(self):
        self.status &= ~(1 << 15)
        return format(self.data, "016b") # 016 means 16 digits with leading 0s 

def updateMonitor(monitor, display):
    while True:
        time.sleep(monitor.delay)
        monitor.printFromData(display)


