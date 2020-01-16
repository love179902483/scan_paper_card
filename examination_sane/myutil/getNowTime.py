import time

def getNowTime():
    curtime = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time())) 
    return curtime

