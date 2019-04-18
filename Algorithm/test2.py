class Singleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            _instance = super().__new__(cls, *args, **kwargs)
            cls._instance = _instance
        return cls._instance


class MyClass:
    pass


class SubSingleton(Singleton):
    pass

c1 = MyClass()
c2 = MyClass()

s1 = SubSingleton()
s2 = SubSingleton()
s3 = Singleton()
s4 = Singleton()
print(c1 is c2)
print(s1 is s2)
print(s1 is s3)
print(s3 is s4)
