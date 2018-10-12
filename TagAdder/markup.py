"""
这里通过sys来读写文件，当然也可以用open
"""

import re
from util import *
from rules import *


class Parser:
    """
    整个程序的主类，用于对文本进行相应的语法分析
    """

    def __init__(self, handler):
        self.handler = handler
        self.__rules = []
        self.filters = []

    def addFilter(self, pattern, name):
        """
        在添加filter时，就调用以下这个方法，创建这个filter。
        filter是调用re.sub的一个函数，传入name不同，调用的方法也就不同。
        最后再把这个filter放到列表里，所以列表里的每个元素都是一个函数。
        """

        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)

        self.filters.append(filter)

    @property
    def rules(self):
        return self.__rules

    @rules.setter
    def rules(self, rules):  # 这里我用装饰器来完成，其实完全没有必要，但是就是学以致用，不用怕忘记了
        self.__rules = rules

    def parse(self, file):
        self.handler.start('document')
        # 下面的循环表示处理为所有的文本块打上标签
        for block in blocks(file):
            for each_filter in self.filters:
                block = each_filter(block, self.handler)  # 首先通过过滤器筛选出是内容、URL、还是Email
            for rule in self.rules:
                if rule.condition(block):  # 然后再判断是否符合某一类规则
                    last = rule.action(block, self.handler)  # 最后调用action打上标签，传出真值，退出循环
                    if last:
                        break
        self.handler.end('document')


class BasicTextParser(Parser):
    """
    构造函数里添加rules和filter的子类
    """

    def __init__(self, handler):
        Parser.__init__(self, handler)  # 先用父类的构造函数
        self.rules = [ListRule(), ListItemRule(), TitleRule(), HeadingRule(), ParagraphRule()]
        self.addFilter(r'\*(.+?)\*', 'emphasis')  # 非贪婪匹配
        self.addFilter(r'(http://[\.a-zA-Z/]+)', 'url')
        self.addFilter(r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'mail')
