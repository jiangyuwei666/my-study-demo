"""
两个指针

首先两个指针都在头部，然后让第一个指针移动k-1个位置，此时第一个指针指向+k个位置的那个节点。
这个时候再同时移动两个节点当第一个指针移动到最后一个节点是时，第二个指针就指向了-k位置的节点。
"""


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def get_value(head, k):
    """
    :param head: 传入链表的头节点
    :param k:传入k
    :return: 返回-k位置的
    """
