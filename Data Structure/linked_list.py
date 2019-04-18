"""
python实现单链表
"""


class Node:

    def __init__(self, x):
        self.val = x
        self.next = None


class NodeList:

    def __init__(self, *args):
        self.head = None
        self.size = 0
        if args:
            if isinstance(args[0], NodeList):
                self.head = args[0].head
                self.size = args[0].size

    def add_first(self, node):
        node.next = self.head
        self.head = node
        self.size += 1

    def add_tail(self, node):
        p = self.head
        while p.next:
            p = p.next
        p.next = node

    def add_node(self, index, node):
        p = self.head
        for i in range(index - 1):
            p = p.next
        node.next = p.next
        p.next = node

    def del_node(self, index):
        pass

    def print_list(self):
        p = self.head
        ret = []
        while p:
            ret.append(p.val)
            p = p.next
        print(ret)


if __name__ == "__main__":
    nl = NodeList()
    nl.add_first(Node(0))
    nl.print_list()
    nl.add_tail(Node(1))
    nl.add_tail(Node(2))
    nl.print_list()
    nl.add_tail(Node(3))
    nl.add_tail(Node(4))
    nl.add_tail(Node(6))
    nl.print_list()
    nl.add_node(2, Node(99))
    nl.print_list()
