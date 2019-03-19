from sort.SortTestHelper import Helper


class BaseSort:
    def __init__(self, n):
        self.num_list = Helper.get_int_list(n)
        print(self.num_list)

    @property
    def num_len(self):
        return len(self.num_list)


class SelectSort(BaseSort):
    """
    选择排序
    """
    @property
    def sort(self):
        for i in range(0, self.num_len):
            min_index = i
            for j in range(i + 1, self.num_len):
                if self.num_list[j] < self.num_list[min_index]:
                    min_index = j
            self.num_list[min_index], self.num_list[i] = self.num_list[i], self.num_list[min_index]
        return self.num_list
