"""
这个问题依旧是可以转换为斐波拉契数列 分为四种情况
1:target<=0 大矩形为2*0, return None
2:target=1 大矩形为 2*1， 只有一种摆放。return 1
3:target=2 大矩形为 2*2, 有两种摆放方法。return 2
4:target>2
    分为两种情况：
        情况一：第一次竖着放则剩下的大矩形就是2*(n-1)
        情况二：第一次横着放，那么第二次也是横着放填满下面的空隙。那么剩下的大矩形2*(n-2)
"""


def rect_place(n):
    """
    :param n: 矩形个数
    :return: 摆放方法数
    """
    if n <= 2:
        return n
    else:
        return rect_place(n - 1) + rect_place(n - 2)


print(rect_place(1))
print(rect_place(2))
print(rect_place(3))
print(rect_place(4))
print(rect_place(5))
print(rect_place(6))
