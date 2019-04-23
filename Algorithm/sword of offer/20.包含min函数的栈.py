"""
这里利用两个栈来实现这个函数，分别是数据栈和最小栈
每次执行push和pop操作的时候，数据栈和普通栈一样执行相应的操作，
在执行push操作的时候，最小栈将push的元素和自身栈顶的元素相比较
如果>的话，就再将最小栈栈顶的元素push进最小栈，而数据栈push push进来的元素
如果<的话，就将最小栈push push进来的元素
"""


class MinStack:

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, item):
        if not self.stack and not self.min_stack:
            self.min_stack.append(item)
            self.stack.append(item)
        else:
            if self.min_stack[-1] > item:
                self.min_stack.append(item)
                self.stack.append(item)
            else:
                self.min_stack.append(self.min_stack[-1])
                self.stack.append(item)
        print(self.stack, "此时最小元素", self.min())

    def pop(self):
        if not self.stack and not self.min_stack:
            print("已经是空了")
            return None
        else:
            self.min_stack.pop(-1)
            s = self.stack.pop(-1)
            print(self.stack, "此时最小元素", self.min())
            return s

    def min(self):
        return self.min_stack[-1]


ms = MinStack()
ms.push(3)
ms.push(4)
ms.push(2)
ms.push(1)
ms.pop()
ms.pop()
ms.push(0)

