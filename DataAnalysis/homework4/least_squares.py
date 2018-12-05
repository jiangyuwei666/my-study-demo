"""
用最小二乘法拟合直线 y = a + b * x

首先给出几个点比如（0.0, 0.9), (0.2, 1.9), (0.4, 2.8), (0.6, 3.3), (0.8, 4.2)

这几个点就分布在直线 y = 1.02 + 4 * x 两侧

已知点求拟合的直线方程（系数）
"""
import numpy as np
from scipy.linalg import solve
from pyecharts import Scatter, Line, Overlap


def get_coordinate():
    """
    键盘输入坐标
    :return:
    """
    x_list = input("输入几个横坐标(用空格隔开)：")
    y_list = input("输入几个纵坐标(用空格隔开)：")
    x_list = x_list.split(' ')
    y_list = y_list.split(' ')
    if len(x_list) != len(y_list):
        print("横纵坐标数量不等")
        get_coordinate()
    else:
        for i in range(len(x_list)):
            x_list[i] = float(x_list[i])
            y_list[i] = float(y_list[i])
        return x_list, y_list


def get_coefficient_matrix(x_list, y_list):
    """
    获取系数矩阵
    """
    # 变量的系数矩阵
    s = []
    for i in range(len(x_list)):
        s.append(x_list[i] * y_list[i])
    variable = np.array([[len(x_list), sum(x_list)],
                         [sum(x_list), sum([x * x for x in x_list])]])
    constant = np.array([[sum(y_list)], [sum(s)]])
    result = solve(variable, constant)
    if result[0][0] and result[1][0]:
        return result[0][0], result[1][0]
    else:
        raise Exception("wwwwwwwrong！！！")


def draw(a, b, x_list, y_list):
    """
    画图
    """

    s = Scatter('最小二乘法')
    s.add('散点', x_list, y_list)
    l = Line()
    l.add('y = {a} + {b}x'.format(a=a, b=b),
          [x_list[0], x_list[-1]],
          [a + (x_list[0] * b), a + (x_list[-1] * b)])
    o = Overlap()
    o.add(s)
    o.add(l)
    o.render('最小二乘法.html')


if __name__ == '__main__':
    x_list, y_list = get_coordinate()
    a, b = get_coefficient_matrix(x_list, y_list)
    draw(a, b, x_list, y_list)
