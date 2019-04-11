"""
通过二分查找法找到最小数字，两个指针一个在头一个在尾。因为是旋转数组，所以尾部指针必定<=头部指针。接着看中间如果说中间那个数
大于头部说明最小数再后半部分，如果小于尾部，说明在前半部分，以此作为判断条件进行递归
"""


# def search_min(arr):
#     if len(arr) == 1:
#         return arr[0]
#     l = 0
#     r = len(arr) - 1
#     mid = (l + r) // 2
#     if arr[l] > arr[mid]:
#         search_min(arr[mid + 1:])
#     elif arr[mid] < arr[r]:
#         search_min(arr[:mid + 1])

def search_min(arr):
    l = 0
    r = len(arr) - 1
    while arr[l] >= arr[r]:
        if r - l == 1:
            return arr[r]
        mid = (l + r) // 2
        if arr[r] >= arr[mid]:
            r = mid
        if arr[l] <= arr[mid]:
            l = mid
    return arr[0]


print(search_min([3, 4, 5, 1, 2]))
print(search_min([1, 0, 0, 1]))
print(search_min([0, 0, 1, 0]))
