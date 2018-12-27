import numpy as np

a = np.array([[1, 1, 1, 1], [2, 4, 3, 1], [3, 4, 1, 2], [1, 4, 3, 5]])
b = np.array([[3], [6], [7], [2]])
c = np.array([[1, 1, 2], [3, 2, 1], [2, 1, 5]])
d = np.array([[4], [5], [1]])
print(np.linalg.solve(a, b))
