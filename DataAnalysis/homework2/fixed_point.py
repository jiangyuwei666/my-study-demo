"""
教材p39 例2-15 用牛顿法求 x = e ** (-x) 在 0.5 处的根
"""
from math import exp
from pyecharts import Scatter, Line


def func(x):
    # 这里的func就和其他的不一样了
    return x * exp(x) - 1


def gunc(x):
    return exp(-x)


def get_root(x):
    x1 = x
    x0 = x1 - 0.000002
    while abs(x1 - x0) >= 0.000001:
        x0 = x1
        x1 = gunc(x0)
        print(x1, func(x1))
        yield [x1, func(x1)]


def draw(generation):
    scatter = Scatter('定点法')
    s = []
    s1 = []
    for i in generation:
        s.append(i[0])
        s1.append(i[1])
    scatter.add('', s, s1)
    scatter.render('定点迭代法.html')


def draw_loss(generator):
    line = Line('定点法loss')
    s = []
    last = 0
    for i in generator:
        s.append(get_loss(last=last, next=i[0]))
        last = i[0]
    line.add('', list(range(len(s))), s, is_smooth=True)
    line.render('定点法loss.html')


def get_loss(last, next):
    if 0 == next:
        return abs(next - last)
    else:
        return abs(next - last) / abs(next)


if __name__ == '__main__':
    draw(get_root(0.5))
    draw_loss(get_root(0.5))
