class Rule:
    """
    所有规则的父类
    如果condition方法返回的是True说明满足某一类文本的要求
    比如满足HeadingRule的condition,就说明是head
    """
    type_ = None

    def action(self, block, handler):
        handler.callback('start_', self.type_)
        handler.feed(block)
        handler.callback('end_', self.type_)
        return True


class HeadingRule(Rule):
    """
    <head>
    标题只能有一行，而且不超过70个字符，不能以冒号结尾
    """
    type_ = 'heading'  # type是默认方法，最好避免使用

    def condition(self, block):
        return '\n' not in block and len(block) < 70 and not block[-1] == ':'  # 是一个bool值


class TitleRule(HeadingRule):
    """
    <h1>
    标题的标准类，是文本中的第一个块
    """
    type_ = 'title'
    first = True

    def condition(self, block):
        if not self.first:
            return False
        self.first = False
        return HeadingRule.condition(self, block)


class ListItemRule(Rule):
    """
    <li>
    列表项是以连字符开头的段落，所以要把连字符删掉
    """
    type_ = 'listitem'

    def condition(self, block):
        return block[0] == '-'

    # 重写action方法，去掉连字符
    def action(self, block, handler):
        handler.callback('start_', self.type_)
        handler.feed(block[1:].strip())
        handler.callback('end_', self.type_)
        return True


class ListRule(ListItemRule):
    """
    <ul>
    列表是以跟在非列表项文本块后面的的列表项开头，以最后一个列表项结尾
    """
    type_ = 'list'
    inside = False

    def condition(self, block):
        return True

    def action(self, block, handler):
        """
        重写action方法
        如果inside的值为False且符合condition规则，说明刚进入列表，调用start方法，将inside置为True
        如果inside的值为True且不符合condition规则，说明这是列表尾部，调用end方法，将inside置为False
        最后再返回False
        """
        if not self.inside and ListItemRule.condition(self, block):
            handler.callback('start_', self.type_)
            self.inside = True
        elif self.inside and not ListItemRule.condition(self, block):
            handler.callback('end_', self.type_)
            self.inside = False
        return False


class ParagraphRule(Rule):
    """
    <p>
    不符合其他文本块的rule的都是段落
    """
    type_ = 'paragraph'

    def condition(self, block):
        return True
