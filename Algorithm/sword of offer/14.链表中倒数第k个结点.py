"""
两个指针

首先两个指针都在头部，然后让第一个指针移动k-1个位置，此时第一个指针指向+k个位置的那个节点。
这个时候再同时移动两个节点当第一个指针移动到最后一个节点是时，第二个指针就指向了-k位置的节点。
"""

class ListNode:
    def __init__(self, x):
        self.x = x
        self.next = None


def init_list(num_list):
    node_list = []
    for i in num_list:
        node = ListNode(i)
        node_list.append(node)
    for j in range(len(node_list)):
        if j == len(node_list) - 1:
            return node_list[0]
        node_list[j].next = node_list[j + 1]


def print_list(head):
    result = []
    while head:
        result.append(head.x)
        head = head.next
    return result



def get_value(head, k):
    """
    :param head: 传入链表的头节点
    :param k:传入k
    :return: 返回-k位置的值
    """
    if k < 0:
        return "你输你🐎个🔨"
    first = head
    second = head
    for i in range(k - 1):
        if not first:
            return "k比他🐎滴链表还长"
        first = first.next  # 此时first指向第+k个元素
    while first.next:
        first = first.next
        second = second.next
    return second.x


head = init_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(get_value(head, 3))
print(get_value(head, -1))
print(get_value(head, 123))
print(get_value(head, 10))

