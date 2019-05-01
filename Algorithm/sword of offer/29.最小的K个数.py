"""
topK问题 前k小的数
使用最大堆实现
只允许堆中存k个元素，遍历这个数组，有以下几种情况
堆中没有装满: 直接将当前元素放进堆中
堆中已经装满:
    当前元素比最大堆中最大的元素还要大: 说明当前元素不可能是不可能是前k小的
    否则: 将最大堆的最大元素和当前元素进行交换，并且生成新的最大堆
"""


# 父亲节点: (i - 1) // 2
# 左孩子:  2 * i + 1
# 右孩子:  2 * i + 2

# 首先实现一个最大堆
class MaxHeap:

    def __init__(self, size=None):
        if size:
            self.size = size
        self.heap = []

    @staticmethod
    def parent(i):
        """
        这个堆中当前节点父亲节点的索引
        """
        if i == 0:
            print("这是顶点了index={}".format(i))
            return
        return (i - 1) // 2

    @staticmethod
    def left(i):
        """
        左孩子的索引
        """
        return i * 2 + 1

    @staticmethod
    def right(i):
        """
        右孩子的索引
        """
        return i * 2 + 2

    def add(self, i):
        """
        依次找父亲节点，并进行Sift Up操作
        """
        if len(self.heap) >= self.size:
            if self.heap[0] > i:
                self.extract_max()
                self.heap.append(i)
                self.__sift_up(len(self.heap) - 1)
        else:
            self.heap.append(i)
            self.__sift_up(len(self.heap) - 1)

    def __sift_up(self, k):
        """
        上浮函数
        """
        while k > 0 and self.heap[k] >= self.heap[MaxHeap.parent(k)]:  # 不是顶节点，并且当前节点的值大于等于父亲节点的值，因为一组元素中可能存在相同的元素，所以要考虑等于的情况
            # 交换两个节点
            self.heap[k], self.heap[MaxHeap.parent(k)] = self.heap[MaxHeap.parent(k)], \
                                                         self.heap[k]
            # 修改k的值
            k = MaxHeap.parent(k)

    def extract_max(self):
        # 1.交换堆顶和最后一个节点
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        # 2.删除最后一个元素(最大元素)
        m = self.heap.pop(-1)
        # 3.将堆顶的元素进行Sift Down操作
        self.__sift_down()
        return m

    def __sift_down(self):
        """
        下沉函数
        """
        k = 0
        while MaxHeap.left(k) < len(self.heap):  # 考察当前节点是否有孩子节点：通过看其左孩子理论索引值是否在数组范围内
            j = MaxHeap.left(k)
            # 如果j + 1在数组范围内，说明有右孩子，并且如果比左孩子大，令j为右孩子索引，并交换
            if j + 1 < len(self.heap) and self.heap[MaxHeap.left(k)] <= self.heap[MaxHeap.right(k)]:
                j += 1
            self.heap[j], self.heap[k] = self.heap[k], self.heap[j]
            k = j  # 最后修改成下一个要比较的节点


def get_top_k(arr, k):
    h = MaxHeap(size=k)
    for i in arr:
        h.add(i)
    print(h.heap)


get_top_k([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 2)
get_top_k([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3)
get_top_k([12, 3, 4, 5, 34, 12, 40, 0, 431, 111, -1, 1, 9], 3)
get_top_k([12, 3, 4, 5, 34, 12, 40, 0, 431, 111, -1, 1, 9], 5)
