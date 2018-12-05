"""
使用贝尔斯托法求下面多项式的跟：
f(x) = x^5 - 3.5x^4 + 2.75x^3 + 2.125x^2 - 3.875x + 1.25
使用初始估计为r=s=-1, 并迭代满足条件ep = 1%
"""
import numpy as np
from scipy.linalg import solve
from math import sqrt


def get_abc(a, r, s):
    """
    获取b，c
    """
    b = [None] * len(a)
    c = [None] * (len(b) - 1)
    a.reverse()
    for m in range(len(a) - 1, -1, -1):
        if len(a) - 1 == m:
            b[m] = a[m]
        elif len(a) - 2 == m:
            b[m] = a[m] + r * b[m + 1]
        else:
            b[m] = a[m] + r * b[m + 1] + s * b[m + 2]
    print('b:', b)
    for n in range(len(b) - 1, 0, -1):
        if len(b) - 1 == n:
            c[n - 1] = b[n]
        elif len(b) - 2 == n:
            c[n - 1] = b[n] + r * c[n]
        else:
            c[n - 1] = b[n] + r * c[n] + s * c[n + 1]
    print('c:', c)
    return b, c


def get_dr_ds(b, c):
    """
    求derta r 和 derta s
    """
    coe_1 = np.array([[c[1], c[2]], [c[0], c[1]]])
    coe_2 = np.array([-b[1], -b[0]])
    d_r, d_s = solve(coe_1, coe_2)[0], solve(coe_1, coe_2)[1]
    return d_r, d_s


def get_ep(d_r, d_s, r, s):
    """
    近似误差
    """
    a_r = abs(d_r / (r + d_r))
    a_s = abs(d_s / (s + d_s))
    return a_r, a_s


def get_root(r, s):
    """
    通过r,s求根
    """
    # return (r + sqrt(abs(r ** 2 + 4 * s))) / 2, (r - sqrt(abs(r ** 2 + 4 * s))) / 2
    if r ** 2 + 4 * s >= 0:
        return (r + sqrt(r ** 2 + 4 * s)) / 2, (r - sqrt(r ** 2 + 4 * s)) / 2
    else:
        return '{real}+{plural}i'.format(real=r / 2, plural=sqrt(abs(r ** 2 + 4 * s)) / 2), '{real}-{plural}i'.format(real=r / 2, plural=sqrt(abs(r ** 2 + 4 * s)) / 2)

def get_division(a, r, s):
    a = np.array(a)
    p = np.poly1d(a)
    e = []
    for i in (p/[1, -r, -s])[0]:
        e.append(i)
    print('e', e)
    return e

def draw():
    pass


if __name__ == '__main__':
    result = []
    a = [1, -3.5, 2.75, 2.125, -3.875, 1.25]
    r = s = -1
    d_r = d_s = 100
    while len(a) > 2:
        for i in range(999):
            b, c = get_abc(a, r, s)
            d_r, d_s = get_dr_ds(b, c)
            r, s = d_r + r, d_s + s
            print(r, s)
            if max(get_ep(d_r, d_s, r, s)) < 0.01:
                result.append(get_root(r, s))
                break
        a = get_division(a, r, s)
    # while len(a) > 2:
    #     while max(get_ep(d_r, d_s, r, s)):
    #         b, c = get_abc(a, r, s)
    #         d_r, d_s = get_dr_ds(b, c)
    #         r, s = d_r + r, d_s + s
    #     result.append(get_root(r, s))
    #     a = get_division(a, r, s)
    result.append(-(s / r))
    print('result', result)
