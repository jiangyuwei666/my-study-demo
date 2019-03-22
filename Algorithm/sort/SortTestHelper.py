import numpy as np
import random


class Helper:
    @classmethod
    def get_int_list(cls, n):
        return list(np.random.randint(low=-n, high=n, size=n))

    @classmethod
    def get_nearly_list(cls, n, m):
        """
        生成几乎有序的一个数列
        :param n: 生成多少位数
        :param m: 交换其中多少个数
        :return:
        """
        num_list = list(range(0, n))
        for i in range(0, m):
            a = random.randint(0, n - 1)
            b = random.randint(0, n - 1)
            num_list[a], num_list[b] = num_list[b], num_list[a]
        return num_list
