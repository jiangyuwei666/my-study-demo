from concurrent.futures import ThreadPoolExecutor
import time


# 线程池
# 主线程中可以获取某一个线程的状态或者一个任务大的状态，以及返回值
# 当一个线程完成后，我们主线程能立即知道
# futures可以让多线程和多进程编码接口一致

def get_html(t, a):
    print(a)
    time.sleep(t)
    print("get page {} success".format(t))
    return t


# max_workers 最大容量
executor = ThreadPoolExecutor(max_workers=2)
# 通过submit函数提交执行的函数到线程池中，submit是立即返回，非阻塞的，主线程会立即往下面执行
task1 = executor.submit(get_html, (5, "1"))
task2 = executor.submit(get_html, (2, "2"))
print(task1.done())
