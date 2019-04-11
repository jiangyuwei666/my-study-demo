import time


def my_decorator(is_time=True):
    def inner1(func):
        def inner2(*args):
            t1 = time.time()
            m = func(*args)
            t2 = time.time()
            if is_time:
                print("用时: {} s".format(t2 - t1))
            return m

        return inner2

    return inner1


@my_decorator(is_time=False)
def my_test(a, b):
    """
    假装这是个算法
    """
    print("正在执行算法...", a, b)
    time.sleep(2)
    return "这是返回值"


# 调用这个算法
s = my_test("哈哈哈哈哈", "6666666666")
print(s)
