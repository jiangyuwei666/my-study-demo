"""
折半查找法
"""
def search(dataSource, find_n):
    mid = int(len(dataSource) / 2)
    if len(dataSource) >= 1:
        if dataSource[mid] > find_n:
            print("data in left of [%s]" % (dataSource[mid]))
            search(dataSource[:mid], find_n)
        elif dataSource[mid] < find_n:
            print("data in right of [%s]" % (dataSource[mid]))
            search(dataSource[mid:], find_n)
        else:
            print("find data is : [%s]" % (dataSource[mid]))
    else:
        print("not find data ...")


if __name__ == '__main__':
    search([1, 3, 4, 23, 5, 6, 2, 6, 873, 2], int(input("请输入查找的数：")))
