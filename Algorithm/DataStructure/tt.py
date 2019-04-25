def main():
    color_dict = {}
    tup = get_input()
    n = tup[0]
    if n % 2 != 0:
        return 0
    balls = tup[1]
    for i in range(len(balls)):
        if balls[i] in color_dict.keys():
            color_dict[balls[i]] += 1
        else:
            color_dict[balls[i]] = 1
    x = min(color_dict.values())
    if x == 1:
        return 0
    ret = 0
    for i in color_dict.keys():
        if color_dict[i] % x != 0:
            return 0
        else:
            ret += color_dict[i] // x
    return ret


def get_input():
    n = int(input())
    s = input()
    s = s.split(' ')
    for i in range(len(s)):
        s[i] = int(s[i])
    return (n, s)


# ******************************结束写代码******************************


res = main()

print(str(res) + "\n")
