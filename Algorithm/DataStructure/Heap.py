import random


class MaxHeap:

    def __init__(self):
        print('__init__')
        self.heap = [0]
        self.__count = 0

    @property
    def count(self):
        return self.__count

    @property
    def get_heap(self):
        return self.heap[1:]

    @property
    def is_empty(self):
        return self.count == 0

    def insert(self, item):
        self.heap.append(item)
        self.__count += 1
        self.__shift_up(self.__count)

    def __shift_up(self, k):
        while self.heap[k] > self.heap[k // 2] and k > 1:
            self.heap[k], self.heap[k // 2] = self.heap[k // 2], self.heap[k]
            k //= 2

    def __shift_down(self, k):
        while 2 * k <= self.count:
            j = 2 * k
            if j + 1 <= self.count and self.heap[2 * k + 1] > self.heap[2 * k]:
                j += 1
            if self.heap[k] > self.heap[j]:
                break
            self.heap[k], self.heap[j] = self.heap[j], self.heap[k]
            k = j

    def extract_max(self):
        """
        取出最大元素
        :return: 返回最大元素
        """
        self.heap[1], self.heap[self.count] = self.heap[self.count], self.heap[1]
        ret = self.heap.pop(-1)
        k = 1
        self.__shift_down(k)
        return ret

    def __del__(self):
        print('__del__')


m = MaxHeap()

for i in range(15):
    m.insert(random.randint(0, 100))
if not m.is_empty:
    print(m.get_heap)
if not m.is_empty:
    print(m.extract_max())
    print(m.get_heap)
