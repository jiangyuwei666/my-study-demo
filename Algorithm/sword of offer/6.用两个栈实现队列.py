"""
两个栈，一个是stack1，另外一个是stack2，首先将所有元素push进stack1里，再以此pop到stack2中，这样再从stack2中pop的
时候就可以就能实现先进先出的。这里要注意的是，pop的时候，如果stack2中没有元素了，这个时候才将stack1中的所有元素pop到
stack2中，push的时候，直接push到stack1中就行

python中利用list的append和pop方法就能实现栈的功能
"""


class MyQueue:
    def __init__(self, *args):
        self.stack1 = []
        self.stack2 = []
        if args:
            self.stack1 += list(args)

    def push(self, item):
        self.stack1.append(item)

    def pop(self):
        if len(self.stack2) == 0:
            if len(self.stack1):
                while len(self.stack1) > 1:
                    self.stack2.append(self.stack1.pop())
                return self.stack2.pop()
            else:
                print("已经空了透你妈")
        else:
            return self.stack2.pop()


