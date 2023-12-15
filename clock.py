import time 

def clockThread(clockFrequency, computer, quitFlag):
    clockTime = 1/clockFrequency
    while True:
        state = computer.nextState
        if not state or quitFlag.is_set():
            time.sleep(clockTime)
            continue
        start = time.time()
        computer.smallStep()
        end = time.time()
        if clockTime > end - start:
            time.sleep(clockTime - (end - start))
        else:
            print("Overclocked by", end - start - clockTime, "seconds for state", state)

