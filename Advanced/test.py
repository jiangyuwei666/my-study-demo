class User:
    def __init__(self):
        self.x = 1
    def __getattribute__(self, item):
        return 2

s = User()
print(s.x)

class A:
    pass
class B(A):
    pass
print(issubclass(B,A))