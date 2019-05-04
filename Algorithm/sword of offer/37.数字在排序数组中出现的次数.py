"""
利用二分法的思想
设要统计的数是k
首先与中间的那个数比较，如果中间那个数比k要大，说明k在前半段，反之在后半段，只需要去相应的区间查找
如果此时中间那个数与k相等，那么就需要看这个数是否是开头的那一个，就看它前面的一个是不是k，如果是，记录索引，不是就继续在前半段找
同理，找到最后一个k，相差即为个数
"""


def get_num_of_k(arr, k):
    left = 0
    right = len(arr) - 1
    mid = (left + right) // 2

    def __get_left_index(arr, k, left, right):
        if left > right:
            return -1
        mid = (left + right) // 2
        if arr[mid] == k:
            if (mid > 0 and arr[mid - 1] != k) or mid == 0:
                return mid
            else:
                return __get_left_index(arr, k, left, mid - 1)
        elif arr[mid] > k:
            return __get_left_index(arr, k, left, mid - 1)
        else:
            return __get_left_index(arr, k, mid + 1, right)

    def __get_right_index(arr, k, left, right):
        if left > right:  # 注意不能设置成了>=
            return -1
        mid = (left + right) // 2
        if arr[mid] == k:
            if (mid < len(arr) - 1 and arr[mid + 1] != k) or mid == len(arr) - 1:
                return mid
            else:
                return __get_right_index(arr, k, mid + 1, right)
        elif arr[mid] > k:
            return __get_right_index(arr, k, left, mid - 1)
        else:
            return __get_right_index(arr, k, mid + 1, right)

    left_index = __get_left_index(arr, k, left, right)
    # print(left_index)
    right_index = __get_right_index(arr, k, left, right)
    # print(right_index)
    print(right_index - left_index + 1)


get_num_of_k([1, 2, 3, 3, 3, 3, 3, 4, 5], 3)  # 5
get_num_of_k([3, 3, 3, 3, 4, 5], 3)  # 4
get_num_of_k([1, 2, 3, 3, 3, 3], 3)  # 4
