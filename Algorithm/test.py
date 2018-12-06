# -*- coding:utf-8 -*-

def MergeSort(input_list):
    '''
    函数说明:归并排序（升序）
    Author:
        www.cuijiahua.com
    Parameters:
        input_list - 待排序列表
    Returns:
        sorted_list - 升序排序好的列表
    '''

    def merge(input_list, left, mid, right, temp):
        '''
        函数说明:合并函数
        Author:
            www.cuijiahua.com
        Parameters:
            input_list - 待合并列表
            left - 左指针
            right - 右指针
            temp - 临时列表
        Returns:
            无
        '''
        i = left
        j = mid + 1
        k = 0

        while i <= mid and j <= right:
            if input_list[i] <= input_list[j]:
                temp[k] = input_list[i]
                i += 1
            else:
                temp[k] = input_list[j]
                j += 1
            k += 1

        while i <= mid:
            temp[k] = input_list[i]
            i += 1
            k += 1
        while j <= right:
            temp[k] = input_list[j]
            j += 1
            k += 1

        k = 0
        while left <= right:
            input_list[left] = temp[k]
            left += 1
            k += 1

    def merge_sort(input_list, left, right, temp):
        if left >= right:
            return
        mid = (right + left) // 2
        merge_sort(input_list, left, mid, temp)
        merge_sort(input_list, mid + 1, right, temp)

        merge(input_list, left, mid, right, temp)

    if len(input_list) == 0:
        return []
    sorted_list = input_list
    temp = [0] * len(sorted_list)
    merge_sort(sorted_list, 0, len(sorted_list) - 1, temp)
    return sorted_list


if __name__ == '__main__':
    input_list = [6, 4, 8, 9, 2, 3, 1]
    print('排序前:', input_list)
    sorted_list = MergeSort(input_list)
    print('排序后:', sorted_list)
