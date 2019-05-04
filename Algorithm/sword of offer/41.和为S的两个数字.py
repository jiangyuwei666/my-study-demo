"""
leetcode上的twosum问题
"""


def get_nums(arr, s):
    d = {}
    ret = None
    for i in arr:
        target = s - i
        if target in d.keys():
            ret = (target, i)  # 使乘积最小的被返回出来
        d[i] = target
    return ret


print(get_nums([1, 2, 3, 4, 5, 6, 7, 8, 9], 10))
