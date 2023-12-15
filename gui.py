import customtkinter as ctk
from PIL import Image
import time 

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LC3 Simulator")

class Register(ctk.CTkFrame):
    def __init__(self, window, value, name, position):
        super().__init__(window, fg_color="transparent", border_width=2, border_color="black")

        self.name = name
        self.binary = value
        self.label = ctk.CTkLabel(self, text=self.name)
        self.binaryLabel = ctk.CTkLabel(self)
        self.hexLabel = ctk.CTkLabel(self)
        self.integerLabel = ctk.CTkLabel(self)

        attributes = [self.label, self.binaryLabel, self.hexLabel, self.integerLabel]
        for column, attribute in enumerate(attributes):
            attribute.configure(font=("Arial", 13, "bold"), height=10)
            attribute.grid(row=0, column=column, padx=10, pady=10)

        self.update(value)
        self.pack()

    def update(self, value):
        self.binary = value
        self.display()

    def display(self):
        value = int(self.binary, 2)
        self.binaryLabel.configure(text=self.binary)
        self.hexLabel.configure(text="x" + format(value, "04x"))
        self.integerLabel.configure(text=format(value, "05"))
            
def setup(computer, clockRoutine, quitFlag):
    window = App()

    secondRow = ctk.CTkFrame(window)
    secondRow.grid(row=1, padx=30, sticky="news")
    secondRow.grid_columnconfigure(0, weight=1)
    secondRow.grid_columnconfigure(1, weight=1)

    # Create registers
    registerSection = ctk.CTkFrame(secondRow, fg_color="transparent")
    registerSection.grid(row=0, column=0, padx=30, pady=10, sticky="news")
    
    ctk.CTkLabel(registerSection, text="Registers").pack()

    registers = []
    for i in range(8):
        registerBlock = Register(registerSection, computer.registers[i], "R" + str(i), [i, 1])
        registers.append(registerBlock)

    PCBlock = Register(registerSection, format(computer.PC, "016b"), "PC", [8, 1])
    registers.append(PCBlock)

    # TODO set up memory visualization
    # TODO set up FSM visualization

    monitors = ctk.CTkFrame(secondRow, fg_color="transparent")
    monitors.grid(row=0, column=1, padx=10, pady=10, sticky="news")
    monitors.grid_rowconfigure(1, weight=1)

    # Setup Monitor
    displayLabel = ctk.CTkLabel(monitors, text="Monitor")
    displayLabel.grid(row=0, sticky="news")
    display = ctk.CTkTextbox(monitors, activate_scrollbars=False)
    display.grid(row=1, padx=10, pady=10, sticky="news")

    display.bind('<Key>', lambda event: key_press(event, computer.keyboard))
    display.configure(state="disabled")

    # FSM visualization
    stateInfo = ctk.CTkFrame(monitors)
    stateInfo.grid(row=2, sticky="news")

    state = ctk.StringVar()
    state.set("FSM State: state18")
    stateLabel = ctk.CTkLabel(stateInfo, textvariable=state)
    stateLabel.pack()

    clockCount = ctk.StringVar()
    clockCount.set("Clock Cycles: 0")
    clockCountLabel = ctk.CTkLabel(stateInfo, textvariable=clockCount)
    clockCountLabel.pack()

    variables = {
        "registers": registers,
        "state": [state, clockCount]
    }

    # Buttons Setup
    buttonSection = ctk.CTkFrame(window, fg_color="transparent")
    buttonSection.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    for i in range(3):    
       buttonSection.grid_columnconfigure(i, weight=1)

    reset = ctk.CTkImage(light_image=Image.open('reset.png'), size=(35, 35))
    run = ctk.CTkImage(light_image=Image.open('play.png'), size=(35, 35))
    pause = ctk.CTkImage(light_image=Image.open('pause.png'), size=(35, 35))
    next = ctk.CTkImage(light_image=Image.open('next.png'), size=(35, 35))

    nextButton = ctk.CTkButton(buttonSection, text="Next State", image=next, command=lambda: nextState(variables, computer))
    runButton = ctk.CTkButton(buttonSection, text="Run", image=run, command=lambda: runComputer(clockRoutine, runButton, run, pause, quitFlag, variables, computer))
    stepInButton = ctk.CTkButton(buttonSection, text="Reset", image=reset, command=lambda: resetComputer(computer, variables))

    buttons = [nextButton, runButton, stepInButton]

    for index, button in enumerate(buttons):
        button.configure(height=50, width=80, anchor="center", fg_color="transparent", hover_color="#b6b6b6", text_color="black", compound="top")
        button.grid(row=0, column=index, padx=10, pady=10)


    return display, window

def resetComputer(computer, variables):
    computer.reset()
    updateDisplay(variables, computer)

def nextState(variables, computer):
    computer.smallStep()
    updateDisplay(variables, computer)

def updateDisplay(variables, computer):
    registers = variables["registers"]
    state = variables["state"]

    state[0].set("FSM State: " + computer.nextState.__name__)
    state[1].set("Clock Cycles: " + str(computer.clockCount))

    for index, register in enumerate(registers[:8]):
        register.update(computer.registers[index])

    registers[8].update(format(computer.PC, "016b"))

def key_press(event, keyboard):
    key = event.char
    if not key:
        return
    keyboard.writeCharacter(key)

def runComputer(clockRoutine, runButton, run, pause, quitFlag, variables, computer):
    if not quitFlag.is_set():
        runButton.configure(image=run, text="Run")
        quitFlag.set()
    else:
        runButton.configure(image=pause, text="Pause")
        quitFlag.clear()
        if not clockRoutine.is_alive():
            clockRoutine.start()

    updateDisplay(variables, computer)

