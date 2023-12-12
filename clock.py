import time 

def clockThread(clockFrequency, computer):
    clockTime = 1/clockFrequency
    while True:
        # TODO time the task and sleep clockTime - tie
        state = computer.nextState
        start = time.time()
        computer.nextState()
        end = time.time()
        if clockTime > end - start:
            time.sleep(clockTime - (end - start))
        else:
            print("Overclocked", end - start, "for state", state)


