class Stack:

    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)
        print("添加成功")

    def pop(self):
        self.stack.pop(-1)
        print("弹出成功")

    def size(self):
        return len(self.stack)

    def __str__(self):
        return str(self.stack)

    def __iter__(self):
        pass


