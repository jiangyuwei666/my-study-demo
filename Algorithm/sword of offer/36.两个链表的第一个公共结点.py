"""
两个链表有公共节点说明两个链表一定是一个Y字型，如下所示：
1-2-3-4
       \
        5-6-7-8
       /
    1-2
所以可以先遍历两个链表，然后判断长度，比如上面，第一个长度为8，第二个长度为6，则先让第一个链表走两步，然后两个链表同时走，走到节点相同时停止
时间复杂度为O(m+n)
"""


class Node:
    def __init__(self, x=None):
        self.val = x
        self.next = None


class NodeList:
    def __init__(self, arr=None):
        self.head = Node()
        head = self.head
        if arr:
            for i in arr:
                head.next = Node(i)
                head = head.next

    def print_list(self):
        head = self.head.next
        ret = []
        while head:
            ret.append(head.val)
            head = head.next
        print(ret)

    def create_common(self, node_list):
        s = self.head
        while True:
            s = s.next
            if not s.next:
                s.next = node_list.head.next
                break


def get_common(node1, node2):
    # print(id(node1), id(node2))
    len1 = 0
    len2 = 0
    # 计算两个链表长度差
    s = node1
    while s:
        len1 += 1
        s = s.next
    s = node2
    while s:
        len2 += 1
        s = s.next
    if len1 > len2:
        for i in range(len1 - len2):
            node1 = node1.next
        while node1 is not node2:
            node1 = node1.next
            node2 = node2.next
        print(node1.val)
    else:
        for i in range(len2 - len1):
            node2 = node2.next
        while node1 is not node2:
            node1 = node1.next
            node2 = node2.next
        print(node1.val)


common_nodes = NodeList([123123, -2, -3])
node_list1 = NodeList([1, 2, 3, 4, 5, 6])
node_list1.create_common(common_nodes)
node_list1.print_list()
node_list2 = NodeList([1, 2, 3])
node_list2.create_common(common_nodes)
node_list2.print_list()
get_common(node_list1.head, node_list2.head)
