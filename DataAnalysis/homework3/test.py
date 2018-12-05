# from sympy import *
from scipy.linalg import solve
import numpy as np

a = np.array([[-4.875, 10.75], [-16.375, -4.875]])
b = np.array([10.5, -11.375])
print(solve(a, b))

# def mmm():
#     return 1, 2
#
# s = []
# s.extend(mmm())
# print(s)

m = np.array([1, -3.5, 2.75, 2.125, -3.875, 1.25])
p = np.poly1d(m)
for i in (p / [1, 0.5, -0.5])[0]:
    print(i)
# print((p / [1, 0.5, -0.5])[0])