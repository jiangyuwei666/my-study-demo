import random


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def init_node_list(n):
    head = ListNode(random.randint(0, 10))
    p = ListNode(random.randint(0, 10))
    head.next = p
    for i in range(n - 2):
        q = ListNode(random.randint(0, 10))
        p.next = q
        p = q
    return head


def solution(node):
    arr = []
    while node:
        arr.append(node.val)
        node = node.next
    return arr


print(solution(init_node_list(5)))
