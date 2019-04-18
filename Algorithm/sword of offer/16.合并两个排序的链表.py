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


def togayther(head1, head2):
    if not head1:
        return head2
    elif not head2:
        return head1
    result_head = None

    if head1.x < head2.x:
        result_head = head1
        result_head.next = togayther(head1.next, head2)
    else:
        result_head = head2
        result_head.next = togayther(head1, head2.next)
    return result_head


def togayther_loop(head1, head2):
    """
    同时还有非递归写法
    看起来好像有点乱，先这样把
    """
    if head1.x < head2.x:
        result_head = head1
        head1 = head1.next
    else:
        result_head = head2
        head2 = head2.next
    result = result_head
    while head1 and head2:
        if head1.x < head2.x:
            result.next = head1
            result = result.next
            head1 = head1.next
        else:
            result.next = head2
            result = result.next
            head2 = head2.next
    if head1:
        while head1:
            result.next = head1
            result = result.next
            head1 = head1.next
    elif head2:
        while head2:
            result.next = head2
            result = result.next
            head2 = head2.next
    return result_head


head1 = init_list([1, 3, 5, 7, 9])
head2 = init_list([2, 4, 6, 8])
print(print_list(togayther(head1, head2)))

head1 = init_list([1, 3, 5, 7, 9])
head2 = init_list([2, 4, 6, 8])
print(print_list(togayther_loop(head1, head2)))
