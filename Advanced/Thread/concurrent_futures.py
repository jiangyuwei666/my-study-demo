from concurrent.futures import ThreadPoolExecutor, as_completed
import time


# 线程池
# 主线程中可以获取某一个线程的状态或者一个任务大的状态，以及返回值
# 当一个线程完成后，我们主线程能立即知道
# futures可以让多线程和多进程编码接口一致

def get_html(t):
    time.sleep(t)
    print("get page {} success".format(t))
    return t


"""
# max_workers 最大容量
executor = ThreadPoolExecutor(max_workers=2)
# 通过submit函数提交执行的函数到线程池中，submit是立即返回，非阻塞的，主线程会立即往下面执行
task1 = executor.submit(get_html, 5)
task2 = executor.submit(get_html, 2)
print(task1.done())
print(task2.done())
time.sleep(2)
print("2s后", task1.done())
print("2s后", task2.done())
time.sleep(3)
print("5s后", task1.done())
print("5s后", task2.done())
#  在task执行之前可以用cancel()取消，比如这里max_workers=2，在设置一个task3就可以将task3取消
"""

# 获取已经成功的task返回
executor = ThreadPoolExecutor(max_workers=2)
urls = [3, 2, 4]
all_task = [executor.submit(get_html, url) for url in urls]
for future in as_completed(all_task):
    data = future.result()  # 返回结果
    print(data)
# for data in executor.map(get_html, urls):
#     print(data)
