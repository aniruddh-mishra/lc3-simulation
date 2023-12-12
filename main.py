from inputOutput import *
from cpu import *
from clock import *
import tkinter as tk
import threading

# Computer Specs
clockFrequency = 1 # Hz
monitorRefreshRate = 1 # Hz
keyboard = Keyboard()
monitor = Monitor(monitorRefreshRate)
computer = Computer(monitor, keyboard)

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
