class Heap:

    def __init__(self, nums=None):
        self.data = []
        if isinstance(nums, list):
            self.data = nums
            self.heapify()

    def __sizeof__(self):
        return len(self.data)

    def is_empty(self):
        return True if self.__sizeof__() else False

    @staticmethod
    def parent(index):
        if index == 0:
            return
        return (index - 1) // 2

    @staticmethod
    def left_child(index):
        return index * 2 + 1

    @staticmethod
    def right_child(index):
        return index * 2 + 2

    def swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def add(self, item):
        self.data.append(item)

        def _sift_up(k):
            while k > 0 and self.data[Heap.parent(k)] < self.data[k]:
                self.swap(Heap.parent(k), k)
                k = Heap.parent(k)

        _sift_up(self.__sizeof__() - 1)

    def extract_max(self):
        if self.__sizeof__() == 0:
            return
        self.data[-1], self.data[0] = self.data[0], self.data[-1]

        result = self.data.pop()

        def _sift_down(k):
            while Heap.left_child(k) < self.__sizeof__():  # 先看有没有越界（有没有左孩子）
                j = Heap.left_child(k)
                if j + 1 < self.__sizeof__() - 1:
                    if self.data[j + 1] > self.data[j]:
                        j += 1
                if self.data[k] > self.data[j]:
                    break
                self.swap(k, j)

        _sift_down(0)
        return result

    def heapify(self):
        i = Heap.parent(self.__sizeof__() - 1)

        def _sift_down(k):
            while Heap.left_child(k) < self.__sizeof__():  # 先看有没有越界（有没有左孩子）
                j = Heap.left_child(k)
                if j + 1 < self.__sizeof__() - 1:
                    if self.data[j + 1] > self.data[j]:
                        j += 1
                if self.data[k] > self.data[j]:
                    break
                self.swap(k, j)

        for j in range(i, -1, -1):
            _sift_down(j)


heap = Heap([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

print(heap.data)
for i in range(heap.__sizeof__()):
    print(heap.extract_max())
