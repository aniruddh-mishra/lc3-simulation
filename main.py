from inputOutput import *
from computer import *
from clock import *
import threading
import gui

# Computer Specs
clockFrequency = 5000 # Hz
monitorRefreshRate = 120 # Hz
keyboard = Keyboard()
monitor = Monitor(monitorRefreshRate)
computer = Computer(monitor, keyboard)

quitFlag = threading.Event()
quitFlag.set()
clockRoutine = threading.Thread(target=clockThread, args=[clockFrequency, computer, quitFlag])
clockRoutine.daemon = True

monitorValue, window = gui.setup(computer, clockRoutine, quitFlag)

monitorRoutine = threading.Thread(target=updateMonitor, args=[monitor, monitorValue])
monitorRoutine.daemon = True

monitorRoutine.start()

window.mainloop()
