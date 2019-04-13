"""
运用双指针
"""


def is_odd(n):
    """
    判断一个数是不是奇数
    :return:True for odd.
    """
    return False if abs(n) % 2 == 0 else True


def order(arr):
    length = len(arr)
    l = 0
    r = length - 1
    while l < r:
        while is_odd(arr[l]):
            l += 1
        while not is_odd(arr[r]):
            r -= 1
        arr[l], arr[r] = arr[r], arr[l]
        l += 1
        r -= 1
    return arr


print(order([1, 2, 4, 4, 5, 6, 7, 8, 9, 0]))
print(order([-1, 2, 4, -4, 5, -6, -7, 8, -9, 0]))
