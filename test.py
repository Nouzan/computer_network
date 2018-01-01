import os, time, fcntl

PIDS = []
R, W = os.pipe()
# fcntl.fcntl(R, fcntl.F_SETFL, os.O_NONBLOCK)


def child():
    count = 0
    while True:
        # os.close(W)
        # time.sleep(1)
        line = os.read(R, 64)
        # print(int(line))
        if int(line) == os.getpid() or count >= 50:
            print('STOP %s' % os.getpid())
            break
        count += 1
        print("[%s, %s, count=%s]" % (os.getpid(), os.getppid(), count))


def parent():
    w = os.fdopen(W, 'w')
    print(PIDS, os.getpid())
    for pid in PIDS:
        print("killing %s" % pid)
        w.write(str(pid))
        w.flush()


pid = None
count = 2

while pid != 0 and count > 0:
    pid = os.fork()
    PIDS.append(pid)
    count -= 1

if pid == 0:
    child()
else:
    parent()
    os.wait()
