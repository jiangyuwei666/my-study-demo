"""
两个序列，按照第一个的顺序往栈里push，然后看栈顶的元素在不在顺序序列的第一个，如果是，弹出栈顶
的元素，并删除掉第二个序列中的元素，如果最后能完全弹出返回True
"""


def solution(arr1, arr2):
    stack = []
    k = 0
    for i in arr1:
        stack.append(i)
        if arr2[k] == stack[-1]:
            stack.pop()
            k += 1

    while len(stack) > 0:
        if stack.pop() == arr2[k]:
            k += 1
        else:
            return False
    return True


print(solution([1, 2, 3, 4, 5], [3, 5, 4, 2, 1]))
print(solution([1, 2, 3, 4, 5], [4, 3, 5, 1, 2]))
print(solution([1, 2, 3, 4, 5], [3, 5, 4, 1, 2]))
print(solution([1], [1]))
print(solution([1], [3]))
