"""
在归并排序的过程中进行计数，已达到求逆序对的目的

将数组分成两个子数组，先求子数组中逆序对的个数，再求两个子数组间逆序队的个数
"""


def get_number_num(arr):
    return merge(arr, 0, len(arr) - 1)


def merge(arr, left, right):
    def __merge(arr, left, mid, right):
        # 初始化三个指针，分别指向[left, mid]的最后，[mid + 1, right]的最后，临时数组的最后(在python中不需要，因为不用声明数组空间)
        temp = []
        p1 = mid
        p2 = right
        count = 0  # 逆序对的个数

    mid = (left + right) // 2
    merge(arr, left, mid)
    merge(arr, mid + 1, right)
    __merge(arr, left, mid, right)

    return
