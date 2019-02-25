"""
用牛顿插值法拟合曲线

最小二乘法拟合的是数据测量误差较大的，插值法则是拟合较准确的

目标：给定几个点及其函数值，求出曲线上某一点的函数值
n个点：Nn(x) = f(x0) + f[x0, x1](x - x0) + f[x0, x1, x2](x - x1)(x - x0) + ··· + f[x0, ···, xn](x - x0)···(x - xn-1)
"""
import matplotlib.pyplot as plt
import logging


# 每一项都有两个部分，一个是f(x):f(x0)f(x0, 1)等，一个是w(x):(x - x0)(x - x1)···
def interpolation_f(xi, yi):
    """
    做插值项的f(x)部分，传入的是每次截取的前n个x和y
    """
    if len(xi) > 2:  # 因为xi和yi一样长的
        return (interpolation_f(xi[1:len(xi)], yi[1:len(yi)]) - interpolation_f(xi[:len(xi) - 1], yi[:len(xi) - 1])) / \
               (xi[-1] - xi[0])
    else:
        return (yi[1] - yi[0]) / (xi[1] - xi[0])


def interpolation_w(xi):
    """
    返回函数get_w()
    :param xi: 传入的x[]
    :return:
    """

    def get_w(x):
        result = 1.0
        for i in range(len(xi) - 1):  # 注意这里减一，因为第n项的Wn是(x - x0)···(x - xn-1)
            result *= (x - xi[i])
        return result

    return get_w


def interpolation(xi, yi):
    """
    返回计算某一点值的方法
    :param xi:
    :param yi:
    :return:
    """

    def get_interpolation(x):
        result = yi[0]
        for i in range(2, len(xi)):  # 从二开始，避免传入一个数没法计算
            result += interpolation_w(xi[:i])(x) * interpolation_f(xi[:i], yi[:i])
        return result

    return get_interpolation


def draw(xi, yi, x, y):
    plt.plot(xi, yi)
    plt.scatter(xi, yi)
    plt.scatter(x, y, color='#8B0000')
    plt.title("newton_interpolation")
    plt.show()


if __name__ == '__main__':
    logging.error('\n 学号：1607094156 \n 姓名：蒋昱葳 \n 之前使用的库是pyecharts，可视化会生成一个html文件，需要点开查看。。。抱歉造成不便')
    # 测试点集 来自例4-14 求f(0.596)
    xi = [0.4, 0.55, 0.65, 0.80, 0.90, 1.05]
    yi = [0.41075, 0.57815, 0.69675, 0.88811, 1.02652, 1.25382]
    draw(xi, yi, 0.596, interpolation(xi, yi)(0.596))
    print(interpolation(xi, yi)(0.596))
