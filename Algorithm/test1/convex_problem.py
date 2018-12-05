"""
凸包问题

随机输入点(第一象限)，求出这些点组成得凸包问题

解决方案：蛮力法，遍历所有两个点组成的组合，判断剩下的点是否在这条直线的同侧或者直线上
如果全部在同侧，就将这两个点记录下来
如果这个点在直线上看横坐标连线的左边还是右边还是中间，如果是左边（右边）就把右边（左边）交换。如果在中间就跳过
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
        # 生成直线列表
        self.line_list = [[x, y] for x in self.point_list for y in self.point_list]
        # 去掉里面不能构成直线的两个点（即一个点）
        for line in self.line_list:
            if line[0] == line[1]:
                self.line_list.remove(line)

    def judge(self):
        """
        判断这两个点是不是土包的边界
        判断另外所有点是否在直线的同一侧
        """
        flag = ''
        for line in self.line_list:
            for point in self.point_list:
                if line[0][0] == line[1][0]:  # 先判断这条直线是不是垂直于x轴，如果垂直就看横坐标不看纵坐标
                    if (self.point_list.index(point) == 0 and point[0] > line[0][0]) or (
                            flag == '>' and point[0] > line[0][0]):
                        flag = '>'
                    elif (self.point_list.index(point) == 0 and point[0] < line[0][0]) or (
                            flag == '<' and point[0] < line[0][0]):
                        flag = '<'
                    elif (self.point_list.index(point) == 0 and point[0] == line[0][0]) or (
                            flag == '=' and point[0] == line[0][0]):
                        flag = '='
                        if point[1] > max(line[0][1], line[1][1]):
                            # 如果在两个点上面，就把上面那个点（大的）换成这个点
                            if line[0][1] > line[1][1]:
                                line[0] = point
                            else:
                                line[1] = point
                        elif point[1] < min(line[0][1], line[1][1]):
                            # 如果在两个点下面，就把小的换成这个点
                            if line[0][1] < line[1][1]:
                                line[0] = point
                            else:
                                line[1] = point

                else:
                    if (self.point_list.index(point) == 0 and point[1] > self.get_function(line[0], line[1],
                                                                                           point)) or (
                            flag == '>' and point[1] > self.get_function(line[0], line[1], point)):
                        flag = '>'
                    elif (self.point_list.index(point) == 0 and point[1] < self.get_function(line[0], line[1],
                                                                                             point)) or (
                            flag == '<' and point[1] < self.get_function(line[0], line[1], point)):
                        flag = '<'
                    elif (self.point_list.index(point) == 0 and point[1] == self.get_function(line[0], line[1],
                                                                                              point)) or (
                            flag == '=' and point[1] == self.get_function(line[0], line[1], point)):
                        flag = '='
                        if point[0] > max(line[0][0], line[1][0]):
                            # 如果在两个点右边就把右边那个点(大的那个)换成这个点
                            if line[0][0] > line[1][0]:
                                line[0] = point
                            else:
                                line[1] = point
                        elif point[0] < min(line[0][0], line[1][0]):
                            # 如果在两个点左边就把左边那个(小的那个)换成这个点
                            if line[0][0] < line[1][0]:
                                line[0] = point
                            else:
                                line[1] = point

                    else:
                        break
                    if self.point_list.index(point) == len(self.point_list) - 1:
                        self.result.append(line)

    def get_function(self, x_1, x_2, x):
        """
        得到对应点的在这条直线上的纵坐标
        :param x_1:
        :param x_2:传进来用来得到直线
        :param x: 需要判断的点的坐标
        :return:用纵坐标去和点的纵坐标比
        """
        if x_1[1] == x_2[1]:
            return x_1[1]
        else:
            return ((x_1[1] - x_2[1]) / (x_1[0] - x_2[0])) * (x[0] - x_1[0]) + x_1[1]


if __name__ == '__main__':
    s = Solution(10)
    print(s.point_list)
    print(s.line_list)
    s.judge()
    print(s.result)
