"""

"""


def left_rotate(string, n):
    s1 = string[:n]
    s2 = string[n:]
    print(s2 + s1)


left_rotate("abcXYZdef", 3)
