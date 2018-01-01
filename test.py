import os
import time

PIDS = []

def child():
    print("I am a child %s, my parent is %s" % (os.getpid(), os.getppid()))


def parent():
    print(PIDS, os.getpid())

pid = None
count = 100

while pid != 0 and count > 0:
    pid = os.fork()
    PIDS.append(pid)
    count -= 1

if pid == 0:
    child()
else:
    parent()
