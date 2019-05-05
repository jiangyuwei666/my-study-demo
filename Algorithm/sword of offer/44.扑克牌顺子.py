"""
先将取出来的排进行排序
先计算出0的个数，再遍历每一张牌计算出牌间相差几张，如果两者相等则使顺子
"""


def is_snake(arr):
    arr.sort()
    count_zero = 0
    for i in arr:
        if i == 0:
            count_zero += 1
        else:
            break
    start = count_zero
    big = start + 1
    count = 0
    while big <= len(arr) - 1:
        if arr[big] == arr[start]:  # 表示有对子
            return False
        count += arr[big] - arr[start] - 1
        start = big
        big += 1

    print(count == count_zero)


is_snake([1, 3, 2, 5, 4])  # T
is_snake([1, 3, 2, 6, 4])  # F
is_snake([0, 3, 2, 6, 4])  # T
is_snake([1, 3, 0, 5, 0])  # T
is_snake([1, 3, 0, 7, 0])  # F
