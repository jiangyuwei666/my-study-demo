"""
如果第一个顶点是重复的节点，那么第一个节点可能被删除，这里考虑使用头节点为空的链表
我们要做的就是先要记录前一个节点，如果后面的相同就跳过这两个节点到后面的后面
"""


class Node:
    def __init__(self, x):
        self.val = x
        self.next = None

    def print_node_list(self):
        head = self.next
        res = []
        while head:
            res.append(head.val)
            head = head.next
        print(res)


def delete_common(head):
    pre = head  # 记录前面的一个节点
    n = head.next
    while n and n.next:
        flag = 0
        val = n.val
        while n.next and n.next.val == val:
            flag = 1  # 这里使用一个flag来判断是否经过了这个循环
            n = n.next
        if flag == 1:
            n = n.next
        pre.next = n
        pre = n
        if n:
            n = n.next
    return head


node = Node(None)
node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node4 = Node(3)
node5 = Node(3)
node6 = Node(6)
node7 = Node(7)
node8 = Node(8)
node.next = node1
node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5
node5.next = node6
node6.next = node7
node7.next = node8
node = delete_common(node)
node.print_node_list()

node = Node(None)
node1 = Node(3)
node2 = Node(3)
node3 = Node(3)
node4 = Node(3)
node5 = Node(3)
node6 = Node(3)
node7 = Node(7)
node8 = Node(8)
node.next = node1
node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5
node5.next = node6
node6.next = node7
node7.next = node8
node = delete_common(node)
node.print_node_list()

node = Node(None)
node1 = Node(3)
node2 = Node(3)
node3 = Node(3)
node4 = Node(3)
node5 = Node(3)
node6 = Node(3)
node7 = Node(3)
node8 = Node(3)
node.next = node1
node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5
node5.next = node6
node6.next = node7
node7.next = node8
node = delete_common(node)
node.print_node_list()