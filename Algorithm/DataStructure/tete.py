def get_input():
    s = input()
    s = s.split(' ')
    x, y = int(s[0]), int(s[1])
    ret = []
    for i in range(x):
        m = input()
        m = m.split(' ')
        for j in range(len(m)):
            m[j] = int(m[j])
        ret.append(m)
    print(ret)
get_input()