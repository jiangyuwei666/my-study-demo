"""
合并排序

分为两个阶段，拆分的阶段和合并（排序）的阶段
拆分阶段：将这n个数的集合拆开，拆成n个
合并阶段：将这些数两两一组从大到小进行组合
"""
def MergeSort(num_list):
    """
    归并排序
    :param num_list:
    :return:
    """

    def merge(num_list, left, mid, right, temp):
        """
        合并函数
        :param num_list:
        :param left:
        :param mid:
        :param right:
        :param temp:
        :return:
        """
        i = left
        j = mid + 1
        k = 0

        while i <= mid and j <= right:
            if num_list[i] <= num_list[j]:
                temp[k] = num_list[i]
                i += 1
            else:
                temp[k] = num_list[j]
                j += 1
            k += 1

        while i <= mid:
            temp[k] = num_list[i]
            i += 1
            k += 1
        while j <= right:
            temp[k] = num_list[j]
            j += 1
            k += 1

        k = 0
        while left <= right:
            num_list[left] = temp[k]
            left += 1
            k += 1

    def merge_sort(num_list, left, right, temp):
        """
        排序函数
        :param num_list:
        :param left:
        :param right:
        :param temp:
        :return:
        """
        if left >= right:
            return
        mid = (right + left) // 2
        merge_sort(num_list, left, mid, temp)
        merge_sort(num_list, mid + 1, right, temp)

        merge(num_list, left, mid, right, temp)

    if len(num_list) == 0:
        return []
    sorted_list = num_list
    temp = [0] * len(sorted_list)
    merge_sort(sorted_list, 0, len(sorted_list) - 1, temp)
    return sorted_list


if __name__ == '__main__':
    num_list = input("请输入多个数(用空格隔开)：")
    nums = num_list.split(' ')
    for i in range(len(nums)):
        nums[i] = float(nums[i])
    print('排序前:', nums)
    sorted_list = MergeSort(nums)
    print('排序后:', sorted_list)
