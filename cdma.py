import multiprocessing
import time
import os


def t(pipe, C, B):
    cs = C.split(' ')
    for i in range(len(cs)):
        cs[i] = str(B * int(cs[i]))
    print('[%s]sending:%s' % (os.getpid(), ' '.join(cs)))
    pipe.send(' '.join(cs))


def r(pipe, C):
    cs = C.split(' ')
    result = 0
    msg = pipe.recv()
    bs = msg.split(' ')
    for i in range(len(cs)):
        result += int(bs[i]) * int(cs[i])
    result = result // len(cs)
    print('[%s]recving:%s' % (os.getpid(), result))


if __name__ == '__main__':
    pipe1s = []
    pipe2s = []
    # Cs = []
    Bs = []
    cs = []
    Cs = ['-1 -1 -1 1 1 -1 1 1',
          '-1 -1 1 -1 1 1 1 -1',
          '-1 1 -1 1 1 1 -1 -1',
          '-1 1 -1 -1 -1 -1 1 -1']
    # for i in range(4):
    #     Cs.append(input())

    Bs = input().split(' ')

    for i in range(4):
        pipe1 = multiprocessing.Pipe()
        pipe2 = multiprocessing.Pipe()
        p1 = multiprocessing.Process(target=t, args=(pipe1[1], Cs[i], int(Bs[i])))
        p2 = multiprocessing.Process(target=r, args=(pipe2[0], Cs[i]))
        pipe1s.append(pipe1[0])
        pipe2s.append(pipe2[1])
        p1.start()
        p2.start()

    for p in pipe1s:
        cs.append(p.recv())

    msgs = [0] * len(cs[0].split())

    for c in cs:
        cc = c.split(' ')
        for i in range(len(cc)):
            msgs[i] += int(cc[i])

    for i in range(len(msgs)):
        msgs[i] = str(msgs[i])

    print('[parent]sending:', ' '.join(msgs))
    for p in pipe2s:
        p.send(' '.join(msgs))
