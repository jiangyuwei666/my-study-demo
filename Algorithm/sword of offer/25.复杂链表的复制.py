"""
需要遍历三次链表
第一次:将每个节点后面都复制一个相同的节点，next指针指向下一个元素，随机指针为空
第二次:将每个复制的节点的随即指针指向前一个节点的随即指针指向的节点的下一个几点
第三次:分离两个链表
"""


class Node:
    def __init__(self, x):
        self.val = x
        self.next = None
        self.sib = None


class List:
    def __init__(self, arr_list=None):
        self.head = Node(None)
        if arr_list:
            head = self.head
            for i in arr_list:
                node = Node(i)
                head.next = node
                head = node
            self.set_sibling()  # 针对于[1,2,3,4,5,6]进行一个指向

    def set_sibling(self):
        head = self.head.next
        for i in range(4):
            head.sib = head.next.next
            head = head.next

    def copy_list(self):
        self.step1()
        self.step2()
        return self.step3()

    def step1(self):
        """
        在每个节点后加一个新节点
        """
        s = self.head.next
        while s:
            node = Node(s.val + 100)
            node.next = s.next
            s.next = node
            s = node.next

    def step2(self):
        """
        设置新增节点的sib指针
        """
        s = self.head.next
        while s:
            node = s.next
            if s.sib:
                node.sib = s.sib.next
            s = node.next

    def step3(self):
        """
        分离两段
        """
        new_list = List()
        head = new_list.head
        s = self.head.next
        while s:
            head.next = s.next
            head = head.next
            s = s.next.next if s.next else None
        return new_list

    def show(self):
        ret = []
        s = self.head.next
        while s:
            ret.append(s.val)
            s = s.next
        print(ret)


node_list = List(arr_list=[1, 2, 3, 4, 5, 6])
node_list.show()
new_list = node_list.copy_list()
new_list.show()
print(node_list.head.next.sib.val)  # 输出3
print(new_list.head.next.sib.val)  # 输出103
