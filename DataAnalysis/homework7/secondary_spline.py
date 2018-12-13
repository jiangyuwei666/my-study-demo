"""
样条插值法 二次样条插值

通过二次样条插值来拟合曲线

假设在有n+1个点，那么就有n条曲线，每条曲线是应该要满足ax**2+bx+c的，每个式子有一组abc所以一共就有3n个未知数。要解这3n个未知数就要3n个方程
下面是找方程的过程：
（1）抛去两个端点的内点，满足链接其的左右两个式子 这里就有 （n-1）*2 个
（2）内点在左右的一阶倒数是相等的 这里有 n-1 个
（3）两端的端点分别满足第一个和最后一个函数 这里有 2 个
上面的加起来就有 3n-1 个方程，还差一个
令a1 = 0(第一段为直线)
所以要用这 3n-1 个方程解出剩下 3n-1 个系数

思路是，先通过方程构建出系数矩阵（未知数是abc），因为是方阵，所以左乘逆，就可以得到未知数矩阵的解
"""


def get_internal_point(xi_list, yi_list):
    """
    获取内点
    :param xi_list:
    :param yi_list:
    :return:
    """
    return xi_list[1:-1], yi_list[1:-1]


def get_formulate(xi_list, yi_list):
    xi, yi = get_internal_point(xi_list, yi_list)
    formulate = []
    for i in range(len(xi)):
        formulate.append([xi[i] ** 2, xi[i], 1])
    return formulate


def init_matrix(formulate, xi_list, yi_list):
    """
    初始化系数矩阵
    :param xi_list:
    :param yi_list:
    :return:
    """
    # 获取系数矩阵，一共是 3n-1 行
    coefficient_matrix = [[0] * (len(xi_list) * 3 - 1)] * (len(xi_list) * 3 - 1)

    for i in range(len(formulate)):
        pass







if __name__ == "__main__":
    xi_list = [3, 4.5, 7, 9]
    yi_list = [2.5, 1, 2.5, 0.5]
    print(get_formulate(xi_list, yi_list))