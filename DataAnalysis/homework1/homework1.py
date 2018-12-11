"""
二分法和试位法求根
相对误差loss
"""
import math
from pyecharts import Scatter, Line


def bisection(a, b, min):
    """
    二分法求根
    示例函数为 f(x) = (x - 1) ** 3
    :param a: 传入左区间
    :param b: 传入右区间
    :param min: 最小区间范围
    """
    if a > b:
        raise Exception('a > b')
    count = 0
    while min < b - a:
        count += 1
        print("第{count}次二分".format(count=count))
        # 先求出区间端点和中点的函数值
        f_a = (a - 1) ** 3
        f_b = (b - 1) ** 3
        # 判断首次输入是否在根同侧
        if 0 < f_a * f_b:
            raise Exception('两个点在一边了')
        elif 0 == f_a * f_b:
            raise Exception('找到根了')
        # 查找根范围
        else:
            f_half = (((a + b) / 2) - 1) ** 3
            yield [(a + b) / 2, f_half]
            if 0 > f_half * f_a:
                b = (a + b) / 2
            elif 0 > f_half * f_b:
                a = (a + b) / 2


def dm(a, b, min):
    """
    试位法求根
    示例函数为f(x) = log e x
    必要条件，f(a) < 0 , f(b) > 0
    这里要注意一点：如果两个区间范围特别小的时候，连接出来的直线的斜率就越接近该点的导数，而这个函数在x=1处的导数值为1。而这个函数在根两边的斜率
    到不了零点的斜率的
    :param a:
    :param b:
    :param min:
    :return:
    """
    if a > b:
        raise Exception('a > b')
    count = 0
    while min < b - a:
        count += 1
        print("第{count}次试位".format(count=count))
        # 计算函数两点的函数值
        f_a = math.log(a)
        f_b = math.log(b)
        if f_a > 0 or f_b < 0:
            raise Exception('f_a > 0 or f_b < 0')
        else:
            # 根据相似三角形求出p点坐标
            p = (f_b * a - f_a * b) / (f_b - f_a)
            # 求出p点的函数值
            f_p = math.log(p)
            yield [p, f_p]
            if 0 > f_a * f_p:
                b = p
            elif 0 > f_b * f_p:
                a = p


def get_loss(last, next):
    """
    计算相对误差
    :param last: 上一个数
    :param next: 下一个数
    :return:
    """
    if 0 == next:
        return abs(next - last)
    else:
        return abs((next - last) / next)


def draw(generator, name):
    scatter = Scatter(name)
    s1 = []
    s2 = []
    for i in generator:
        s1.append(i[0])
        s2.append(i[1])
    scatter.add('', s1, s2)
    scatter.render(name + '.html')


def draw_loss(generator, name):
    """
    画loss图
    :param generator: 传入的生成器
    :param name: 图表名
    :return:
    """
    line = Line(name)
    s = []
    last = 0
    for i in generator:
        s.append(get_loss(last=last, next=i[0]))
        last = i[0]
    line.add('', list(range(len(s))), s, is_smooth=True)
    line.render(name + '.html')



if __name__ == '__main__':
    draw(bisection(-1, 4, 0.00001), "二分法")
    draw_loss(bisection(0.7, 1.4, 0.00000001), "二分法loss")
    draw(dm(0.01, 11, 1), "试位法")
    draw_loss(dm(0.01, 11, 1), "试位法loss")


