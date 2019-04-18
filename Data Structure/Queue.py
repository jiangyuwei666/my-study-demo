class Queue:

    def __init__(self):
        self.queue = []

    def push(self, item):
        self.queue.append(item)
        print("添加成功")

    def pop(self):
        print("弹出成功")
        return self.queue.pop(0)

    def size(self):
        return len(self.queue)

    def __str__(self):
        return str(self.queue)

    def __iter__(self):
        pass
