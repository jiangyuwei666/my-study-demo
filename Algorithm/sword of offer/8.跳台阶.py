"""
如果只有一级台阶的话，只有一种跳法
如果有两级台阶，就有两种跳法。一次跳一级跳两次，一次跳两级跳一次
如果台阶有n级(n>2)那么可以选择第一次跳一级，则剩下的n-1跳法为f(n-1),如果第一次跳两级，则剩下的n-2级跳法为f(n-2)，所以此时总共跳法为f(n) = f(n-1)+f(n-2)
很明显是斐波拉契数列
"""


# def jump(n):
#     """
#     使用递归的方法会有很多重复的计算，大大降低了算法的效率问题
#     :param n: n级台阶
#     :return: 多少种跳法
#     """
#     if n <= 2:
#         return n
#     else:
#         return jump(n - 1) + jump(n - 2)


def jump(n):
    """
    使用循环从下往上进行计算，可以减少重复项的计算
    :param n:
    :return:
    """
    if n <= 2:
        return n
    else:
        pre1 = 1
        pre2 = 2
        next = 0
        for i in range(3, n + 1):
            next = pre1 + pre2
            pre1 = pre2
            pre2 = next
        return next



print(jump(0))
print(jump(1))
print(jump(2))
print(jump(10))