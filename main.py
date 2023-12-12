from inputOutput import *
from computer import *
from clock import *
import tkinter as tk
import threading

# Computer Specs
clockFrequency = 10000 # Hz
monitorRefreshRate = 120 # Hz
keyboard = Keyboard()
monitor = Monitor(monitorRefreshRate)
computer = Computer(monitor, keyboard)

# Test code
address = int("3000", 16)
for i in range(10000):
    code = "0001001001100001"
    computer.memory.memory[address] = code
    address += 1

# Set up the window
window = tk.Tk()

# keyboardRoutine = threading.Thread(target=pollKeyboard, args=[keyboard])
monitorRoutine = threading.Thread(target=updateMonitor, args=[monitor])
clockRoutine = threading.Thread(target=clockThread, args=[clockFrequency, computer])

monitorRoutine.daemon = True
clockRoutine.daemon = True

monitorRoutine.start()
clockRoutine.start()

def key_press(event):
    key = event.char
    if not key:
        return
    keyboard.writeCharacter(key)
    monitor.writeCharacter(int(keyboard.getData(), 2))
 
window.bind('<Key>', key_press)

# Start window
window.mainloop()
