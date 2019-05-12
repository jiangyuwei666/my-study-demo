# GIL global interpreter lock 全局解释器锁

import threading

total = 0


def add():
    global total
    for i in range(1000000):
        total += 1


def desc():
    global total
    for i in range(1000000):
        total -= 1


thread1 = threading.Thread(target=add)
thread2 = threading.Thread(target=desc)
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print(total)
# total每次都不一样，是因为GIL释放了(字节码执行了行数或者说时间等元素，然后将GIL释放)
