"""
采用滑动窗口的思想来实现
用两个数字left和right分别表示序列的最小值和最大值，
首先将left初始化为1，right初始化为2，
如果从left到right的和大于sum，我们就从序列中去掉较小的值(即增大left), 相反，只需要增大right。
终止条件为：一直增加left到(1+sum)/2 两个数，如果left比其一半还大，就不能满足要求
"""


def get_nums(s):
    if s < 0:
        return
    ret = []
    left = 1
    right = 2
    while right > left and left <= (1 + s) / 2:
        current = (left + right) * (right - left + 1) / 2  # 差为1的等差数列，求和公式：（首项+末项）*项数:(right - left + 1)/2
        if current == s:
            res = []
            for i in range(left, right + 1):
                res.append(i)
            ret.append(res)
            left += 1
            right += 1
        elif current < s:
            right += 1
        else:
            left += 1
    print(ret)

get_nums(100)

