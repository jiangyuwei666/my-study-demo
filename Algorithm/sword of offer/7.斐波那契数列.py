"""
同跳台阶，推荐使用循环来做
"""


def init_fibonacci(n):
    if n == 1 or n == 2:
        return 1
    else:
        return init_fibonacci(n - 2) + init_fibonacci(n - 1)


print(init_fibonacci(3))
