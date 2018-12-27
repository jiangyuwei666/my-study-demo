"""
LU分解
LU分解简化了高斯消去法的一些复杂的步骤，是高斯消元的一种表达方式
LU分解的基本原理：
一个多元一次方程组可以看作 [A]{X}={B}
首先对A进行杜利特尔分解成上三角形矩阵（U阵）和下三角形矩阵（L阵）
即[L][U]{X}={B}
令[U]{X}={Y}
先解出{Y}
再通过[U]{Y}解出{X}
"""
import numpy as np


def summation(i, j, matrix1, matrix2):
    """
    求和函数
    """
    s = 0
    for k in range(1, i):
        s += matrix1[i][k] * matrix2[k][j]
    return s


def LU_break(matrix):
    """
    LU分解
    :param matrix:系数矩阵A
    :return: L矩阵和U矩阵
    """
    n = len(matrix)
    matrix_l = np.eye(n)
    matrix_u = np.zeros((n, n))
    matrix_u[0] = matrix[0]
    for m in range(1, n):
        matrix_l[m][0] = matrix[m][0] / matrix[0][0]
    # 因为U阵第一行和J阵第一列已知，故从第二行（列）开始
    for i in range(1, n):

        # U阵
        for j in range(i, n):
            sum = 0
            for k in range(j):
                sum += matrix_l[i][k] * matrix_u[k][j]
            matrix_u[i][j] = matrix[i][j] - sum

        # J阵
        if i == n - 1:
            pass
        else:
            # 因为对角线上全是1，所以从i + 1开始计算
            for j in range(i + 1, n):
                sum = 0
                for k in range(i):
                    sum += matrix_l[j][k] * matrix_u[k][i]
                # print(sum)
                # print(matrix_u[i][i])
                matrix_l[j][i] = (matrix[j][i] - sum) / matrix_u[i][i]

    return matrix_u, matrix_l


def func_input():
    n = int(input("请入输入你要解几元方程组："))
    matrix = []
    for i in range(n):
        row = input("依次输入系数(用空格隔开)：")
        row = row.split()
        for j in range(len(row)):
            row[j] = float(row[j])
        matrix.append(row)
    return np.array(matrix)


if __name__ == '__main__':
    print(" 学号：1607094156 \n 姓名：蒋昱葳")
    # 课本例3-7示例
    test_matrix = [[2, 2, 3], [4, 7, 7], [-2, 4, 5]]
    # 课本例3-10示例
    # test_matrix = [[1, 1, -1], [1, 2, -2], [-2, 1, 1]]
    # 自定义输入矩阵
    # test_matrix = func_input()  # 取消注释使用
    U, L = LU_break(test_matrix)
    print("系数矩阵为：\n", np.array(test_matrix))
    print("U阵为：\n", U)
    print("L阵为：\n", L)
