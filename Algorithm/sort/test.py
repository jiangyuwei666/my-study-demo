from sort.select_sort import *
import time


def test_sort(sort, n):
    start_time = time.time()
    s = sort(n)
    end_time = time.time()
    print(s.sort)
    print(end_time - start_time)


test_sort(SelectSort, 10000)
