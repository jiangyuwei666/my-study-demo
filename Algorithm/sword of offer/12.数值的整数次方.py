"""
考虑代码的完整性  幂的定义：指数个底数相乘
1.指数=0，返回1
2.底数=0，返回0
3.底数指数同时为0，返回
4.指数<0，返回累乘的倒数
# 5.浮点型不能直接比较  高版本使用math.isclose()
"""

# import math
#
# print(math.isclose(0.0, 0.00000000000000000000001))


def power(base, n):
    result = 1
    if base == 0:
        if n == 0:
            raise ZeroDivisionError
        return 0
    if n == 0:
        if base == 0:
            raise ZeroDivisionError
        return 1
    for i in range(abs(n)):
        result *= base
    if n < 0:
        return 1.0 / result
    return result


print(power(2.0, 3))
print(power(2.0, -3))
print(power(-2.0, -3))
print(power(1.0, 0))
print(power(0.0, 1))
# print(power(0.0, 0))

