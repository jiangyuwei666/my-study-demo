"""
拉格朗日插值法

另外一种插值拟合曲线的插值方法，通过给定点集使用，对每个点满足l(x)，然后求和
"""
import logging
from matplotlib import pyplot as plt


def get_yi(yi_list, i):
    """
    获取每一项的y部分
    :param yi_list: 测试纵坐标点集
    :param i: 索引
    :return: yi
    """
    return yi_list[i]


def get_func_l(xi, xi_list):
    """
    求每一项的l(x)部分
    :param xi:
    :param xi_list:
    :return:
    """

    def func_l(x):
        # 分子
        numerator = 1
        # 分母
        denominator = 1
        for i in range(len(xi_list)):
            # 跳过该项
            if xi_list.index(xi) == i:
                continue
            numerator *= (x - xi_list[i])
            denominator *= (xi - xi_list[i])
        return numerator / denominator

    # 返回这个函数地址
    return func_l


def get_func_L(x, xi_list, yi_list):
    """
    求每一项
    :param x: 要求的值
    :param xi_list:
    :param yi_list:
    :return:
    """
    Lx = 0
    for i in range(len(xi_list)):
        # 计算每一项
        Lx += get_func_l(xi_list[i], xi_list)(x) * get_yi(yi_list, i)

    return Lx


def draw(xi_list, yi_list, x, y):
    """
    画图
    """
    plt.scatter(xi_list, yi_list)
    plt.scatter(x, y, color='#8B0000')
    plt.title("lagrangian_interpolation")
    plt.show()


if __name__ == '__main__':
    # 测试数据 课本p125例4-3
    xi_list = [1, 3, 2]
    yi_list = [1, 2, -1]
    x = float(input("请输入想要查看的点值："))
    y = get_func_L(x, xi_list, yi_list)
    print('点{x}的函数值y={y}'.format(x=x, y=y))
    draw(xi_list, yi_list, x, y)
    logging.error('\n 学号：1607094156 \n 姓名：蒋昱葳')
