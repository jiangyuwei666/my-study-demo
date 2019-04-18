"""
思路：在矩阵外面加一层0，可以避免越界问题。遍历矩阵中所有是2的位置，判断其四周是否有1，如果有时间+1，如果没有返回当前时间
"""
import sys

def get_input():
    """
    获取输入
    """
    rect = []
    while True:
        line = sys.stdin.readline().strip()
        if not line:
            break
        values = list(map(int, line.split()))
        rect.append(values)
    return rect


def have_1(rect, i, j):
    """
    判断上下左右是否有1
    i, j表示位置
    return:True for have
    """
    if rect[i][j - 1] == 1 or rect[i][j + 1] == 1 or rect[i - 1][j] == 1 or rect[i + 1][j] == 1:
        return True
    else:
        return False


def change_1(rect, i, j):
    if rect[i][j - 1] == 1:
        rect[i][j - 1] = 2
    if rect[i][j + 1] == 1:
        rect[i][j + 1] = 2
    if rect[i - 1][j] == 1:
        rect[i - 1][j] = 2
    if rect[i + 1][j] == 1:
        rect[i + 1][j] = 2
    return rect


def get_new_rect(rect):
    """
    在矩阵外面加一层0，可以避免越界问题
    """
    zero = [0 for i in range(len(rect[0]) + 2)]
    for j in range(len(rect)):
        rect[j].insert(0, 0)
        rect[j].append(0)
    rect.insert(0, zero)
    rect.append(zero)
    return rect


def solution(func):
    min = 0
    rect = func()
    length = len(rect)
    height = len(rect[0])
    rect = get_new_rect(rect)
    for i in range(1, length + 1):
        for j in range(1, height + 1):
            if rect[i][j] == 2:
                if have_1(rect, i, j):
                    rect = change_1(rect, i, j)
                    min += 1
    if min == 0:
        return -1
    else:
        return min


if __name__ == "__main__":
    print(solution(get_input))
