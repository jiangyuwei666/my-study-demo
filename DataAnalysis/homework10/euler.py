"""
使用欧拉法解常微分方程

关键是估计斜率，然后利用迭代来算每次步长对应的函数值

公式：y(x + 1) = y(x) + 斜率(该点导数) x 步长

例如：计算 dy/dx = -2x^3 + 12x^2 + 20x + 8.5   从x=0到x=4，取步长为0.5，x=0处y=1

这类方法解题时，首先对微分方程进行积分，易得
y = -0.5x^4 + 4x^3 - 10x^2 + 8.5x + c 再将y = f(0) = 1代入解出c = 1
在利用迭代公式计算出每次跳过步长那个点的值
"""
import numpy as np
import matplotlib.pyplot as plt


def get_integral(coefficient, x, y):
    """
    求积分
    :param x: x,y 用于求常数c
    :param y:
    :param coefficient: 一个列表，一次表示常数项，一次项，二次项...如[1, 2, 3]表示1 + 2x + 3x^2
    :return: 返回列表。表示每一项系数
    """
    p = np.polynomial.Polynomial(coefficient)
    p = list(p.integ())
    # 求常数项c
    sum = 0
    for i in range(len(p)):
        sum += p[i] * (x ** i)
    p[0] = y - sum
    return p


def get_slope(coefficient, x):
    """
    求斜率
    :param coefficient: 微分方程的系数，传入的系数
    :param x: 某一点
    :return:
    """
    slope = 0  # 斜率
    for i in range(len(coefficient)):
        slope += coefficient[i] * (x ** i)
    return slope


def get_func_value(original_coefficient, x):
    """
    求原函数(积分)的函数值
    :param original_coefficient: 积分后的系数
    :param x: 某一点
    :return: 函数值
    """
    value = 0  # 函数值
    for i in range(len(original_coefficient)):
        value += original_coefficient[i] * (x ** i)
    return value


def euler(step, n, original_coefficient, coefficient):
    """
    用迭代求解
    :param step: 每一步的步长
    :param n: 目标区间
    :param original_coefficient: 原函数的系数
    :param coefficient: 导数的系数
    :return:
    """
    num = 0
    x_result = []
    y_result = []
    real_y_result = []
    while num < n:
        x_result.append(num)
        # 真实解
        real_y_result.append(get_func_value(original_coefficient, num))
        if num == 0:
            # 第一个解
            y_result.append(get_slope(coefficient, num) * step + get_func_value(original_coefficient, num))
        else:
            # 后面的若干个解
            y_result.append(get_slope(coefficient, num) * step + y_result[-1])
        num += step
    y_result.pop()
    y_result.insert(0, 1.1)
    print("x:", x_result)
    print("欧拉法得到的y:", y_result)
    print("真实y:", real_y_result)
    return x_result, y_result, real_y_result


def draw(xi, yi, real_yi):
    """
    画图
    :param xi:
    :param yi:
    :param real_yi:
    :return:
    """
    plt.scatter(xi, yi)
    plt.scatter(xi, real_yi, color="#8B0000")
    plt.title("blue scatters for euler")
    plt.show()


if __name__ == '__main__':
    print("姓名：蒋昱葳\n学号：1607094156\n示例采用的微分方程为：8.5-20x+12x^2-2x^3\n步长为：0.25\n可修改主函数第二行修改")
    xi, yi, real_yi = euler(step=0.25, n=4, original_coefficient=get_integral([8.5, -20, 12, -2], 0, 1),
                            coefficient=[8.5, -20, 12, -2])  # 修改此行两个列表改变参数
    draw(xi, yi, real_yi)
