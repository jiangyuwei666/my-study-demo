"""
教材p39 例2-15 用牛顿法求 x = e ** (-x) 在 0.5 处的根
"""
from math import exp
from pyecharts import Scatter, Line


def func(x):
    """
    函数
    """
    return x * exp(x) - 1


def get_root(x, x_):
    """
    求附近的根
    """
    x1 = x
    # 初始化x0，保证第一次能够进入循环
    x0 = x1 - 0.000002
    while abs(x1 - x0) > 0.000001:
        x0 = x1
        x1 = x0 - (func(x0) * (x0 - x_) / (func(x0) - func(x_)))
        print(x0, x1)
        yield [x1, func(x1)]


def draw(generation):
    s1 = []
    s2 = []
    for i in generation:
        s1.append(i[0])
        s2.append(i[1])
    scatter = Scatter('弦截法')
    scatter.add('', s1, s2)
    scatter.render('弦截法.html')


if __name__ == '__main__':
    draw(get_root(0, 1))
