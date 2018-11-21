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


def func_(x):
    """
    一阶导数
    """
    return exp(x) + x * exp(x)


def get_root(x):
    """
    求附近的根
    """
    x1 = x
    # 初始化x0，保证第一次能够进入循环
    x0 = x1 - 0.000000000002
    while abs(x1 - x0) >= 0.000000000001:
        x0 = x1
        x1 = x0 - (func(x0) / func_(x0))
        print(x0, x1)
        yield [x1, func(x1)]


def draw(generation):
    s = []
    for i in generation:
        s.append(i[1])
    scatter = Scatter('牛顿法')
    # 因为牛顿法收敛很快，所以用横坐标表示不明显，故用次数表示
    scatter.add('', list(range(len(s))), s)
    scatter.render('牛顿法.html')


def draw_loss(generator):
    line = Line('牛顿法loss')
    s = []
    last = 0
    for i in generator:
        s.append(get_loss(last=last, next=i[0]))
        last = i[0]
    line.add('', list(range(len(s))), s, is_smooth=True)
    line.render('牛顿法loss.html')


def get_loss(last, next):
    if 0 == next:
        return abs(next - last)
    else:
        return abs(next - last) / abs(next)


if __name__ == '__main__':
    draw(get_root(0.5))
    draw_loss(get_root(0.5))

