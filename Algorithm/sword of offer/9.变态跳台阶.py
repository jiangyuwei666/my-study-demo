"""
同样的道理
那么有n级台阶就是f(n)=f(n-1)+f(n-2)+···+f(2)+f(1)
同理f(n-1) = f(n-2)+···+f(2)+f(1)
所以f(n)= 2*f(n-1)
"""


# def crazy_jump(n):
#     if n <= 1:
#         return n
#     else:
#         return crazy_jump(n - 1) * 2

def crazy_jump(n):
    if n <= 1:
        return n
    else:
        result = 1
        for i in range(1, n):
              result = result * 2

    return result

print(crazy_jump(1))
print(crazy_jump(2))
print(crazy_jump(3))
print(crazy_jump(4))
print(crazy_jump(5))
