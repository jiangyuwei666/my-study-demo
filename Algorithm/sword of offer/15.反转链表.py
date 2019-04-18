"""

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



def revers_list(head):
    """
    反转链表
    :param head:传入的头节点
    :return: 返回反转后的头节点
    """
    if not head or not head.next:  # 空列表或者只有一个node的列表
        return head
    pre_node = None  # 前一个节点初始时是空
    while head:  # 因为head在一次循环后会指向下一个节点，当最后一次循环执行完后，它会指向None
        next_node = head.next   # 1.先拷贝一个下一个节点存在next_node中
        head.next = pre_node    # 2.然后将当前节点的下一个node指向前一个node
        pre_node = head         # 3.此时当前节点操作完成，先将前一个node设置为当前node
        head = next_node        # 4.将当前node后移
    return pre_node  # 最后一次循环，将head指向None，将pre_node移动至当前节点

if __name__ == "__main__":
    head = init_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(print_list(revers_list(head)))
    head = init_list([1])
    print(print_list(revers_list(head)))
