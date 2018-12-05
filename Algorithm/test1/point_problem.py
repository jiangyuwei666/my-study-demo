"""
最近对点问题
"""

from random import randint


class Solution(object):

    def __init__(self, n):
        """
        self.line_list就是直线集合
        """
        self.point_list = []
        self.result = []
        # 生成列表
        for i in range(n):
            self.point_list.append((randint(0, 10), randint(0, 10)))
        # 生成所有两点组合
        self.two_point_list = [(point1, point2) for point1 in self.point_list for point2 in self.point_list]
        for j in self.two_point_list:
            if j[0] == j[1]:
                self.two_point_list.remove(j)
        self.min = 0
        self.get_min_distance()

    def get_min_distance(self):
        for two_point in self.two_point_list:
            if self.two_point_list.index(two_point) == 0:
                self.min = self.compute_distance(two_point)
            else:
                if self.min > self.compute_distance(two_point):
                    self.min = self.compute_distance(two_point)

    def compute_distance(self, two_point):
        return abs((two_point[0][0] - two_point[1][0]) ** 2 + (two_point[0][1] - two_point[1][1]) ** 2)

if __name__ == '__main__':
    s = Solution(3)
    print(s.two_point_list)
    print(s.min)
