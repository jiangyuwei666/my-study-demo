"""
两步反转，先反转
"""


def reverse_words(s):
    # 将整个字符串反转
    s = s.strip()
    s = s[::-1]
    print(s)
    ret = ""
    start = 0
    for i in range(len(s)):
        if s[i] == " ":
            m = s[start:i]
            m = m[::-1] + " "
            ret += m
            start = i + 1
        if i == len(s) - 1:
            m = s[start::]
            m = m[::-1]
            ret += m
    print(ret)


reverse_words('student. a am I')
