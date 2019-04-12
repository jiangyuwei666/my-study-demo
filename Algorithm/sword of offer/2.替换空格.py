def solution_by_py(s):
    s = s.replace(' ', '%20')
    return s


def solution_by_py1(s):
    s = s.split(' ')
    s = '%20'.join(s)
    return s


# def solution_by_re(s):
#

print(solution_by_py('a b c'))
print(solution_by_py1('a b c'))
