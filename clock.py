import time 

def clockThread(clockFrequency, computer):
    clockTime = 1/clockFrequency
    while True:
        time.sleep(clockTime)
        # computer.next()


