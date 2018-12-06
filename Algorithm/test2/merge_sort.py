"""
合并排序

分为两个阶段，拆分的阶段和合并（排序）的阶段
拆分阶段：将这n个数的集合拆开，拆成n个
合并阶段：将这些数两两一组从大到小进行组合
"""
from random import randint


class Solution:
    def __init__(self, n):
        self.nums = []
        for i in range(n):
            self.nums.append(randint(0, 10))

    def merge(self, left, mid, right, temp):
        """
        合并
        :param left:
        :param mid:
        :param right:
        :param temp:
        :return:
        """
        i = left
        j = mid + 1

        # 先将其按大小顺序塞进去
        while i <= mid and j <= right:
            if self.nums[i] <= self.nums[j]:
                temp.append(self.nums[i])
                i += 1
            else:
                temp.append(self.nums[j])
                j += 1
        # 再将没有放进去的全部放进去
        while i <= mid:
            temp.append(self.nums[i])
            i += 1
        while j <= right:
            temp.append(self.nums[j])

        self.nums.clear()
        self.nums.extend(temp)


    def merge_sort(self, left, right, temp):
        if left >= right:
            return
        mid = (right + left) // 2
        self.merge_sort(left, mid, temp)
        self.merge_sort(mid + 1, right, temp)
        self.merge(left, mid, right, temp)


# if __name__ == '__main__':
#     s = Solution(10)
#     print(s.merge_sort())
if __name__ == '__main__':
    