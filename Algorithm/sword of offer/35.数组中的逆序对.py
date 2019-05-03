"""
在归并排序的过程中进行计数，已达到求逆序对的目的

将数组分成两个子数组，先求子数组中逆序对的个数，再求两个子数组间逆序队的个数
"""


def get_number_num(arr):
    print(merge(arr, 0, len(arr) - 1))


def merge(arr, left, right):
    def __merge(arr, left, mid, right):
        # 初始化三个指针，分别指向[left, mid]的最后，[mid + 1, right]的最后，临时数组的最后(在python中不需要，因为不用声明数组空间)
        temp = []
        p1 = mid
        p2 = right
        count = 0  # 逆序对的个数
        while p1 >= left and p2 >= mid + 1:  # 两个指针从后面往前面走
            if arr[p1] > arr[p2]:  # 说明前面的比后面的大 能组成逆序对
                temp.insert(0, arr[p1])
                p1 -= 1
                count += p2 - mid  # 因为此时已经排好序，最后一个肯定是当前数组中最大的一个元素，所以此时可以直接加入当前指针前面的个数

            else:
                temp.insert(0, arr[p2])  # 说明前面的没有后面的大，直接加入到数组中
                p2 -= 1
        # 将剩下的加入到temp中
        while p1 >= left:
            temp.insert(0, arr[p1])
            p1 -= 1
        while p2 >= mid + 1:
            temp.insert(0, arr[p2])
            p2 -= 1

        arr[left: right + 1] = temp
        return count

    if left >= right:
        return 0
    mid = (left + right) // 2
    left_count = merge(arr, left, mid)
    right_count = merge(arr, mid + 1, right)
    count = __merge(arr, left, mid, right)

    return left_count + right_count + count


get_number_num([5, 1, 2, 3, 4])  # 4
get_number_num([6, 5, 4, 3, 2, 1])  # 15
get_number_num([1, 2, 3, 4, 7, 6, 5])  # 3
get_number_num([1, 2, 3, 4, 5, 6])  # 0
get_number_num([5])  # 0
