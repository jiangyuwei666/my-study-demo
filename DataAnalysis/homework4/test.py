from scipy.linalg import solve
import numpy as np

a = np.array([
    [5, 2],
    [2, 1.2]
])
b = np.array([
    [13.1],
    [6.84]
])
# s = input()
# s = s.split(' ')
# for i in range(len(s)):
#     s[i] = float(s[i])
# print(s, type(s))
m = solve(a, b)
print(type(m), m)
print(m[0][0], m[1][0])
print(type(m[0][0]), type(m[1][0]))
