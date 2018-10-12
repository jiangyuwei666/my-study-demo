class Handle:
    """
    parser中的handler调用的就是这个类里面的方法，也就相当于这个类是整个程序的处理器。
    """

    def callback(self, prefix, name, *args):
        """
        :param prefix: 函数前缀
        :param name: 函数名
        :param args: 接收剩下的参数
        :return:
        """
        method = getattr(self, prefix + name, None)  # 通过函数前缀和名称来查找某一个方法，若果找不到就用None作为默认值
        if callable(method):
            return method(*args)  # 如果能被调用，那么允许添加而外的参数*args
        # 比如调用handler.callback('start_', 'document')，就会去找handler.start_document()方法。没有参数的

    """
    start和end都是辅助方法，帮助handler对象调用callback()，要是不嫌麻烦可以像rules文件里那样直接调用callback方法
    当然也可以像markup那样调用start和end方法。
    """
    def start(self, name):
        self.callback('start_', name)

    def end(self, name):
        self.callback('end_', name)

    def sub(self, name):
        """
        :param name:
        :return: 返回新的函数，这个函数会作为替换函数传递给re.sub()的第二个参数
        """
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None:
                match.group(0)
                return result

        return substitution


class HTMLRenderer(Handle):
    """
    根据上面的回调
    具体怎么操作的类
    比如上面传入的两个参数是'start_'和'document'就调用第一个方法
    """

    def start_document(self):
        print('<html><head><title>测试测试测试</title></head><body>')

    def end_document(self):
        print('</body></html>')

    def start_paragraph(self):
        print('<p>')

    def end_paragraph(self):
        print('</p>')

    def start_heading(self):
        print('<h2>')

    def end_heading(self):
        print('</h2>')

    def start_list(self):
        print('<ul>')

    def end_list(self):
        print('</ul>')

    def start_listitem(self):
        print('<li>')

    def end_listitem(self):
        print('</li>')

    def start_title(self):
        print('<h1>')

    def end_title(self):
        print('</h1>')

    def sub_emphasis(self, match):
        return '<em>{}</em>'.format(match.group(1))

    def sub_url(self, match):
        return '<a href = "{}">{}</a>'.format(match.group(1), match.group(1))

    def sub_mail(self, match):
        return '<a href = "mailto:{}">{}</a>'.format(match.group(1), match.group(1))

    def feed(self, data):
        print(data)
