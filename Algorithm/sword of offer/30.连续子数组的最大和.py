"""
扫描法
当前子数组的和如果是负数的话，势必会造成后面的和更小，这个时候就直接舍弃当前子数组，从后面开始
"""


def get_sum(arr):
    p1 = p2 = 0
    current = 0  # 当前和
    ret = 0  # 最终结果
    for i in range(len(arr)):
        if current <= 0:
            current = arr[i]
            p1 = i
        else:
            current += arr[i]
            p2 = i - 1
        if ret < current:
            p2 += 1  # 如果是执行了上面那个if是不可能执行这个，当又加了一个数后，说明是加的正数，当前的最终结果因为这个整数变得更大，此时后标应该往后移动
            ret = current
    print(ret, "索引范围({},{})".format(p1, p2))


get_sum([1, -2, 3, 10, -4, 7, 2, -5])
get_sum([-2, 1, 2, 3, 4, 5])
get_sum([1, 2, 3, 4, 5, -2])
get_sum([1, 2, 3, 4, 5])
get_sum([1, 2, -4, 3, 4, 5])

