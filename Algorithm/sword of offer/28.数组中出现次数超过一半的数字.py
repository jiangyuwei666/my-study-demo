"""
数组中有一个数字出现的次数超过数组长度的一半，它出现的次数比其他所有数字出现的次数的和还要多。
在遍历数组的时候保存两个值：一个是数组中的一个数字，一个是次数。
当遍历到下一个数字的时候，如果下一个数字和之前保存的数字相同，则次数加1；
如果下一个数字和之前保存的数字不同，则次数减1。如果次数为0，保存下一个数字，并把次数设置为1。
肯定是最后遍历完成后保存的那个数字，且次数大于等于1
"""


def get_num(arr):
    if not arr:
        print("wrong")
        return
    num = arr[0]
    count = 1
    for i in arr[1:]:
        if count == 0:
            num = i
            count = 1
        if num == i:
            count += 1
        else:
            count -= 1
    count = 0
    for j in arr:
        if j == num:
            count += 1
    if count > len(arr) / 2:
        return num
    else:
        print(arr, '不存在')
        return 0


print(get_num([1, 2, 3, 2, 2, 2, 5, 4, 2]))
print(get_num([2, 2, 2, 2, 2, 1, 3, 4, 5]))
print(get_num([1, 3, 4, 5, 2, 2, 2, 2, 2]))
print(get_num([1, 3, 4, 5, 2, 2, 2, 2]))
print(get_num([2]))
print(get_num([]))