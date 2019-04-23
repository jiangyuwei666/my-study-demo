from sort.my_sort import *
import time


class Tester:

    def __init__(self, method="random", swap_times=1, n=0, sorter_list=[]):
        self.sorters = []
        for item in sorter_list:
            if method == 'random' and callable(item):
                s = item(n)
                if isinstance(s, BaseSort):
                    self.sorters.append(s)
            elif method == 'nearly' and callable(item):
                s = item(n, swap_times=swap_times)
                if isinstance(s, BaseSort):
                    self.sorters.append(s)
            elif method == 'repeat' and callable(item):
                s = item(n, repeat=True)
                if isinstance(s, BaseSort):
                    self.sorters.append(s)

    def test_sort(self):
        time_list = []
        for sorter in self.sorters:
            start_time = time.time()
            print(sorter.name, sorter.sort)
            end_time = time.time()
            time_list.append(sorter.name + ':' + str(end_time - start_time))
        print(time_list)


# tester = Tester(n=10000, sorter_list=[InsertSort, MergeSort], method='nearly', swap_times=1)
tester = Tester(n=10, sorter_list=[QuickSortjj])
tester.test_sort()
