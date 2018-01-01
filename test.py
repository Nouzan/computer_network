import multiprocessing
import time
import os

PS = []
# R, W = os.pipe()
# fcntl.fcntl(R, fcntl.F_SETFL, os.O_NONBLOCK)


def child(pipe):
    count = 0
    while True:
        # os.close(W)
        time.sleep(1)
        msg = pipe.recv()
        # print(int(line))
        if int(msg) == os.getpid() or count >= 50:
            print('STOP %s' % os.getpid())
            break
        count += 1
        print("[%s, %s, count=%s]" % (os.getpid(), os.getppid(), count))


def parent(pipes):
    # print(PIDS, os.getpid())
    for i in range(len(PS)):
        print("killing %s" % PS[i].pid)
        time.sleep(4)
        pipes[i].send(str(PS[i].pid))
        # w.flush()

pipes = []

for i in range(4):
    pipe = multiprocessing.Pipe()
    p = multiprocessing.Process(target=child, args=(pipe[0],))
    pipes.append(pipe[1])
    PS.append(p)
    # pipe[0].close()
    p.start()

parent(pipes)
os.wait()
