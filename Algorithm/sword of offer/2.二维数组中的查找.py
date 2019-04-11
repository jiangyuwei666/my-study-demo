def solution(arr, target):
    """
    :param arr: 传入的二维数组
    :param target: 需要从二维数组中找出的元素
    :return: boolean
    """
    row = len(arr)
    column = len(arr[0])
    i = 0
    j = column - 1
    while True:
        if target == arr[i][j]:
            return True
        elif target > arr[i][j] and i < row - 2:
            i += 1
            continue
        elif target < arr[i][j] and j > 0:
            j -= 1
            continue
        else:
            return False


test_arr = [[1, 3, 5, 7], [2, 4, 7, 8], [3, 5, 8, 9], [8, 9, 10, 11], [10, 12, 13, 14]]
print(solution(test_arr, 1))
