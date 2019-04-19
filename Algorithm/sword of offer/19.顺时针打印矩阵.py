"""
循环打印，可以看作打印多次一圈，因此可将代码分成两部分，一部分是控制输出一圈，一部分是控制输出哪一圈

每一圈的起始位置是(0,0),(1,1),(2,2)...到多少的时候不行了呢？

可以发现start*2<rows,start*2<cols。其中start是0,1,2...等起始位置

打印一圈分为4步：1.打印上面的一行2.打印右边的一列3.打印下边的一行4.打印左边的一列
    1.
    2. 终止行号大于起始行号
    3. 终止列号大于起始列号，终止行号大于起始行号
    4. 终止列号大于起始列号，终止行号比其实行号至少大2

"""


def print_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if matrix else 0
    start = 0
    ret = []
    while start * 2 < rows and start * 2 < cols:
        circle_matrix(matrix, start, rows, cols, ret)
        # print_circle(matrix, start, rows, cols, ret)
        start += 1
    print(ret)


def circle_matrix(matrix, start, rows, cols, ret):
    row = rows - start - 1  # 表示这一圈循环的最后一行
    col = cols - start - 1  # 表示最后一列
    # 最上面一行，从左到右
    for i in range(start, col + 1):
        ret.append(matrix[start][i])
    # 右边一行，从上到下
    if start < row:
        for i in range(start + 1, row + 1):  # start+1表示下一个，然后到最下面哪一行
            ret.append(matrix[i][col])
    # 下面一行，从右到左
    if start < row and start < col:
        for i in range(col - 1, start - 1, -1):
            ret.append(matrix[row][i])
    # 左边一行，从下到上
    if start < row and start < col:
        for i in range(row - 1, start, -1):
            ret.append(matrix[i][start])


mat =[  [1, 2, 3, 4, 5],
        [16, 17, 18, 19, 6],
        [15, 24, 25, 20, 7],
        [14, 23, 22, 21, 8],
        [13, 12, 11, 10, 9]]
print_matrix(mat)
mat =[  [1],
        [2],
        [3],
        [4],
        [5],
        [6],
        [7],
        [8]]
print_matrix(mat)
mat =[  [0, 1],
        [15, 2],
        [14, 3],
        [13, 4],
        [12, 5],
        [11, 6],
        [10, 7],
        [9, 8] ]
print_matrix(mat)
