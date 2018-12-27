"""
原始高斯消去法求解线性方程组

原始高斯消去分两步：
    第一步：先从上到下，化为上三角形
    第二步：再从下到上的回溯，求得所有解

增广矩阵用二维列表分两部分表示，比如

        1 1 2 4
     [  3 2 1 5  ]
        2 1 4 1

    test_matrix = [[1.0, 1.0, 2.0], [3.0, 2.0, 1.0], [2.0, 1.0, 4.0]]
    test_coefficient = [4.0, 5.0, 1.0]

"""


def func_input():
    n = int(input("请入输入你要解几元方程组："))
    matrix = []
    coefficient = []
    for i in range(n):
        row = input("依次输入系数和常数：")
        row = row.split()
        if len(row) < n + 1:
            raise Exception('输入格式有误')
        for j in range(len(row)):
            row[j] = float(row[j])
        matrix.append(row)
        coefficient.append(row.pop())
    print(matrix, coefficient)
    return matrix, coefficient


def gauss_1(matrix, coefficient):
    """
    化为上三角形
    :param matrix: 系数矩阵
    :param coefficient: 常数项
    :return:
    """
    n = len(matrix) - 1
    for k in range(n):
        # print(matrix[k])
        for i in range(k + 1, n + 1):
            # print(matrix[i][k], matrix[k][k])
            if matrix[k][k] == 0:
                raise Exception("矩阵中有0项")
            factor = matrix[i][k] / matrix[k][k]
            # print(factor)
            for j in range(k, n + 1):
                matrix[i][j] = matrix[i][j] - (factor * matrix[k][j])
            coefficient[i] = coefficient[i] - factor * coefficient[k]
    print(matrix)
    print(coefficient)
    return matrix, coefficient


def gauss_2(matrix, coefficient):
    n = len(matrix) - 1
    result = []
    result.append(coefficient[n] / matrix[n][n])
    for i in range(n - 1, -1, -1):
        sum_ = coefficient[i]
        for j in range(i + 1, n):
            sum_ -= matrix[i][j] * result[-1]
        result.append(sum_ / matrix[i][i])
    print("所有的解:", result)


if __name__ == '__main__':
    # 测试数据
    test_matrix = [[1, 1, 1, 1], [2, 4, 3, 1], [3, 4, 1, 2], [1, 4, 3, 5]]
    test_coefficient = [3.0, 6.0, 7.0, 2.0]
    # test_matrix = [[1.0, 1.0, 2.0], [3.0, 2.0, 1.0], [2.0, 1.0, 4.0]]
    # test_coefficient = [4.0, 5.0, 1.0]
    a, b = gauss_1(test_matrix, test_coefficient)
    gauss_2(a, b)
    print('姓名：蒋昱葳\n学号：1607094156')
