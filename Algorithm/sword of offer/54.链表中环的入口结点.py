# -*- encoding:utf-8 -*-
"""
方法一：可以用一个hash表存遍历过的节点，这个当下次遍历到的时候就将这个节点返回就可以了
方法二：
假设环长度为n，进入环之前结点个数为x,slow在环内走了k个结点,fast绕环走了m圈,则有2(x+k)=x+mn+k 可以得出x = mn - k。此时slow距入口结点还剩 n-k个结点,x=(m−1)n+n−k，即一个指针从链表头节点走到环入口的长度等于另一个指针从相遇的位置走 m-1圈后再走n-k的长度，也就是说两个指针相遇后，让一个指针回到头节点，另一个指针不动，然后他们同时往前每次走一步，当他们相遇时，相遇的节点即为环入口节点
    1. 首先判断是否有环:可以定义快、慢两个指针，快指针依次走两步，慢指针一次走一步，然后如果快指针走到None了，说明没有环，反之就有环
    2. 如果有，此时再将一个指针(快)放在头部，然后一起每次走一步，两个指针再次相遇的时候，即为入口
"""


class Node:
    def __init__(self, x):
        self.val = x
        self.next = None


class NodeList:
    pass


def solution(head):
    # 先定义快慢两个指针
    fast = head
    slow = head
    while fast.next and fast.next.next:
        fast = fast.next.next
        slow = slow.next

        if fast is slow:
            fast = head
            while fast is not slow:
                fast = fast.next
                slow = slow.next
            return fast
    return None


node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node4 = Node(4)
node5 = Node(5)
node6 = Node(6)
node7 = Node(7)
node8 = Node(8)
node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5
node5.next = node6
node6.next = node7
node7.next = node8
node8.next = node3
print(solution(node1).val)
