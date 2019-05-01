"""
扫描法
当前子数组的和如果是负数的话，势必会造成后面的和更小，这个时候就直接舍弃当前子数组，从后面开始
"""


def get_sum(arr):
    p1 = p2 = 0
    current = 0  # 当前和
    ret = 0  # 最终结果
    for i in range(len(arr)):
        if current < 0:
            current = arr[i]
            p1 = i
        else:
            current += arr[i]
            p2 = i - 1
        if ret < current:
            ret = current
    print(ret, "索引范围({},{})".format(p1, p2))


get_sum([1, -2, 3, 10, -4, 7, 2, -5])
get_sum([-2, -8, -1, -5, -9])
get_sum([2, 8, 1, 5, 9])
