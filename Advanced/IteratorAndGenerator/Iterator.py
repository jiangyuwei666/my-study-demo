# 迭代器满足迭代协议
# 什么是迭代器？迭代器是访问集合内元素的一种方式，一般用来遍历数据
# 迭代器和以下表访问方式不一样，迭代器是不能返回的
from collections.abc import Iterator


class Company:
    def __init__(self, employee_list):
        self.employee = employee_list

    def __iter__(self):
        return MyIterator(employee_list=self.employee)  # 迭代器设计模式


class MyIterator(Iterator):
    def __init__(self, employee_list):
        self.iter_list = employee_list
        self.index = 0

    def __next__(self):
        try:
            a = self.iter_list[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return a


if __name__ == "__main__":
    company = Company([1, 2, 3, 4, 5])
    my_iter = iter(company)
    while True:
        try:
            print(next(my_iter))
        except StopIteration:
            break
    for i in company:  # 实现了__iter__方法，说明是一个可迭代类型
        print(i)
