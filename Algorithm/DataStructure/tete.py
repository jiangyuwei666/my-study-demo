def string2int(str):
    dict = {
        '0': 0,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '.': 1,
        '-': -1,
    }

    str = list(str)
    if not str or len(str) < 0:
        return 0
    while str[0] == '0':
        if len(str) > 1:
            str = str[1:]
        else:
            return 0
    flag = 1
    if str[0] == '-':
        flag = -1
        str = str[1:]
    ret = 0
    stack = []
    for i in range(len(str)):
        if str[i] not in dict.keys():
            return 0
        elif str[i] == '.':
            break
        else:
            stack.append(int(str[i]))
    n = 1
    while stack:
        ret += stack.pop(-1) * n
        n *= 10
    return ret * flag







try:
    _str = input()
except:
    _str = None

res = string2int(_str)

print(str(res) + "\n")