"""
由题意已知，可以将其中的A中某一位取出来保存，然后将其置为1，就可跳过这一位，之后再换回来
"""
from functools import reduce


def get_B(A):
    B = []
    for i in range(len(A)):
        t = A[i]
        A[i] = 1
        B.append(reduce(lambda x, y: x * y, A))
        A[i] = t
    print(B)


get_B([1, 1, 1, 1, 1])
get_B([1, 2, 3, 4, 5])
