import customtkinter as ctk
from PIL import Image
import time 

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
            self.grid_columnconfigure(column, weight=1)
            attribute.configure(font=("Arial", 13, "bold"), height=5, width=40)
            attribute.grid(row=0, padx=5, column=column, pady=7)

        self.update(value)
        self.grid(row=position, sticky="news")

    def update(self, value):
        self.binary = value
        self.display()

    def display(self):
        value = int(self.binary, 2)
        self.label.configure(text=self.name)
        self.binaryLabel.configure(text=self.binary)
        self.hexLabel.configure(text="x" + format(value, "04x"))
        self.integerLabel.configure(text=format(value, "05"))

class MemoryCell(Register):
    def __init__(self, window, value, address, position):
        super().__init__(window, value, address, position)

        # TODO Add translation to code

    def updateCell(self, value, address):
        self.name = address
        super().update(value)
            
def setup(computer, clockRoutine, quitFlag):
    window = ctk.CTk()
    window.title("LC3 Simulator")
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=2)
    window.grid_columnconfigure(0, weight=1)

    # Buttons Setup
    buttonSection = ctk.CTkFrame(window, fg_color="transparent")

    for i in range(3):    
       buttonSection.grid_columnconfigure(i, weight=1)

    reset = ctk.CTkImage(light_image=Image.open('reset.png'), size=(25, 25))
    run = ctk.CTkImage(light_image=Image.open('play.png'), size=(25, 25))
    pause = ctk.CTkImage(light_image=Image.open('pause.png'), size=(25, 25))
    next = ctk.CTkImage(light_image=Image.open('next.png'), size=(25, 25))

    nextButton = ctk.CTkButton(buttonSection, text="Next State", image=next, command=lambda: nextState(variables, computer))
    runButton = ctk.CTkButton(buttonSection, text="Run", image=run, command=lambda: runComputer(clockRoutine, runButton, run, pause, quitFlag, variables, computer, disableEntries, disableFrames))
    # TODO Disable everything except monitor when the code is running
    stepInButton = ctk.CTkButton(buttonSection, text="Reset", image=reset, command=lambda: resetComputer(computer, variables))

    buttons = [nextButton, runButton, stepInButton]

    for index, button in enumerate(buttons):
        button.configure(width=80, anchor="center", fg_color="transparent", hover_color="#b6b6b6", text_color="black", compound="top")
        button.grid(row=0, column=index, padx=10, pady=(20, 0))

    # Computer Display Setup
    secondRow = ctk.CTkFrame(window, fg_color="transparent")
    secondRow.grid_columnconfigure(0, weight=1)
    secondRow.grid_columnconfigure(1, weight=1)
    secondRow.grid_rowconfigure(0, weight=1)

    # Create Registers
    registerSection = ctk.CTkFrame(secondRow, fg_color="transparent")
    registerSection.grid(row=0, column=0, padx=30, pady=10, sticky="news")
    registerSection.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(registerSection, text="Registers").grid(row=0)

    registers = []
    for i in range(8):
        registerBlock = Register(registerSection, computer.registers[i], "R" + str(i), i + 1)
        registers.append(registerBlock)

    PCBlock = Register(registerSection, format(computer.PC, "016b"), "PC", 9)
    registers.append(PCBlock)

    # TODO set up FSM visualization

    monitors = ctk.CTkFrame(secondRow, fg_color="transparent")
    monitors.grid(row=0, column=1, padx=30, pady=10, sticky="news")
    monitors.grid_columnconfigure(0, weight=1)

    # Setup Monitor
    displayLabel = ctk.CTkLabel(monitors, text="Monitor")
    displayLabel.grid(row=0, sticky="news")
    display = ctk.CTkTextbox(monitors, border_color="black", border_width=2, activate_scrollbars=False)
    display.grid(row=1, pady=10, sticky="news")

    display.bind('<Key>', lambda event: key_press(event, computer, variables, quitFlag))
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

    # Memory Visualization Setup
    memoryRow = ctk.CTkFrame(window, fg_color="transparent")
    memoryRow.grid_columnconfigure(0, weight=1)
    memoryRow.grid_rowconfigure(2, weight=1)

    memoryLabel = ctk.CTkLabel(memoryRow, text="Memory")
    memoryLabel.grid(row=0, pady=(0, 5))

    memorySection = ctk.CTkFrame(memoryRow, fg_color="transparent")
    memorySection.grid(row=1, pady=(0, 20), sticky="news")
    memorySection.grid_columnconfigure(0, weight=1)
    memorySection.grid_columnconfigure(1, weight=1)

    memoryCells1 = ctk.CTkFrame(memorySection, fg_color="transparent")
    memoryCells1.grid(row=0, column=0, padx=(30, 5), sticky="news")
    memoryCells1.grid_columnconfigure(0, weight=1)

    memoryCells = []
    memoryStart = 0
    for i in range(6):
        memoryCell = MemoryCell(memoryCells1, computer.memory.memory[memoryStart + i], "x" + format(memoryStart + i, "04x"), i) 
        memoryCells.append(memoryCell)

    memoryCells2 = ctk.CTkFrame(memorySection, fg_color="transparent")
    memoryCells2.grid(row=0, column=1, padx=(5, 30), sticky="news")
    memoryCells2.grid_columnconfigure(0, weight=1)

    for i in range(6, 12):
        memoryCell = MemoryCell(memoryCells2, computer.memory.memory[memoryStart + i], "x" + format(memoryStart + i, "04x"), i) 
        memoryCells.append(memoryCell)

    memoryControl = ctk.CTkFrame(memoryRow, fg_color="transparent")
    memoryControl.grid(row=2, sticky="news")
    memoryControl.grid_columnconfigure(0, weight=1)
    memoryControl.grid_columnconfigure(1, weight=1)

    memoryScroll = ctk.CTkFrame(memoryControl, fg_color="transparent")
    memoryScroll.grid(row=0, column=0, sticky="news")
    memoryScroll.grid_columnconfigure(0, weight=1)
    memoryScroll.grid_columnconfigure(1, weight=1)
   
    down = ctk.CTkImage(light_image=Image.open('down.png'), size=(25, 25))
    up = ctk.CTkImage(light_image=Image.open('up.png'), size=(25, 25))

    memoryDecrease = ctk.CTkButton(memoryScroll, image=down, text="", fg_color="transparent", hover_color="#b6b6b6", command=lambda: shiftMemoryUp(False, variables, computer))
    memoryDecrease.grid(row=0, column=0)

    memoryIncrease = ctk.CTkButton(memoryScroll, image=up, text="", fg_color="transparent", hover_color="#b6b6b6", command=lambda: shiftMemoryUp(True, variables, computer))
    memoryIncrease.grid(row=0, column=1)

    memoryChoose = ctk.CTkFrame(memoryControl, height=3, fg_color="transparent")
    memoryChoose.grid(row=0, column=1, sticky="news")

    memoryAddress = ctk.CTkEntry(memoryChoose, height=30)
    memoryAddress.place(relx=0.1, relwidth=0.6)
    memoryAddress.bind("<Return>", lambda event: shiftMemory(memoryAddress.get(), variables, computer))

    searchButtonContainer = ctk.CTkFrame(memoryChoose, fg_color="transparent")
    searchButtonContainer.place(relx=0.7, relwidth=0.2)
    searchButtonContainer.grid_columnconfigure(0, weight=1)
    searchButtonContainer.grid_rowconfigure(0, weight=1)

    search = ctk.CTkImage(light_image=Image.open('search.png'), size=(25, 25))
    searchMemory = ctk.CTkButton(searchButtonContainer, width=30, height=30, image=search, text="", hover_color="#b6b6b6", fg_color="transparent", command=lambda: shiftMemory(memoryAddress.get(), variables, computer))
    searchMemory.grid(row=0, column=0, padx=5, sticky="news")

    disableEntries = [nextButton, stepInButton, searchMemory, memoryIncrease, memoryDecrease, memoryAddress]
    disableFrames = [*registers, *memoryCells, stateInfo]

    variables = {
        "registers": registers,
        "state": [state, clockCount],
        "memory": [memoryCells, memoryStart]
    }

    # Place Sections
    buttonSection.grid(row=0, sticky="news", pady=(0, 10), column=0)
    secondRow.grid(row=1, column=0, sticky="news")
    memoryRow.grid(row=2, column=0, pady=(0, 30), sticky="news")

    return display, window

def shiftMemory(address, variables, computer):
    try:
        if address[0] == "x":
            address = int(address[1:], 16)
        else:
            address = int(address)
        variables["memory"][1] = max(min(int("FFFF", 16) - 11, address), int("0000", 16))
        updateDisplay(variables, computer)
    except:
        return

def shiftMemoryUp(up, variables, computer):
    if up:
        variables["memory"][1] += 12
        variables["memory"][1] = min(int("FFFF", 16) - 11, variables["memory"][1])
    else:
        variables["memory"][1] -= 12
        variables["memory"][1] = max(int("0000", 16), variables["memory"][1])

    updateDisplay(variables, computer)

def resetComputer(computer, variables):
    computer.reset()
    updateDisplay(variables, computer)

def nextState(variables, computer):
    computer.smallStep()
    updateDisplay(variables, computer)

def updateDisplay(variables, computer):
    registers = variables["registers"]
    state = variables["state"]
    memory = variables["memory"]

    state[0].set("FSM State: " + computer.nextState.__name__)
    state[1].set("Clock Cycles: " + str(computer.clockCount))

    for index, register in enumerate(registers[:8]):
        register.update(computer.registers[index])

    registers[8].update(format(computer.PC, "016b"))

    for index, memoryCell in enumerate(memory[0]):
        memoryIndex = memory[1] + index
        memoryCell.updateCell(computer.memory.getMemory(memoryIndex), "x" + format(memoryIndex, "04x"))

def key_press(event, computer, variables, quitFlag):
    key = event.char
    if not key:
        return
    computer.keyboard.writeCharacter(key)
    if quitFlag.is_set():
        updateDisplay(variables, computer)

def runComputer(clockRoutine, runButton, run, pause, quitFlag, variables, computer, entries, registers):
    if not quitFlag.is_set():
        runButton.configure(image=run, text="Run")
        quitFlag.set()
        updateDisplay(variables, computer)
        state = "normal"
        color = "black"
    else:
        runButton.configure(image=pause, text="Pause")
        quitFlag.clear()
        if not clockRoutine.is_alive():
            clockRoutine.start()
        state = "disabled"
        color = "gray"

    for entry in entries:
        entry.configure(state=state)

    for register in registers:
        attributes = register.winfo_children()
        for label in attributes:
            label.configure(text_color=color)
