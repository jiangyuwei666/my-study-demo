from sort.SortTestHelper import Helper


class BaseSort:
    def __init__(self, n, swap_times=None):
        """
        :param n:
        :param swap_times: 有swap_times表示要生成几乎有序得数列
        """
        if swap_times:
            self.num_list = Helper.get_nearly_list(n, swap_times)
        else:
            self.num_list = Helper.get_int_list(n)

    @property
    def num_len(self):
        return len(self.num_list)

    @property
    def name(self):
        return

    def before_sort(self):
        print(self.name, self.num_list)


class SelectSort(BaseSort):
    """
    选择排序
    从每一个位置开始往后找最小的放在这个位置
    """

    @property
    def sort(self):
        self.before_sort()
        for i in range(0, self.num_len):
            min_index = i
            for j in range(i + 1, self.num_len):
                if self.num_list[j] < self.num_list[min_index]:
                    min_index = j
            self.num_list[min_index], self.num_list[i] = self.num_list[i], self.num_list[min_index]
        return self.num_list

    @property
    def name(self):
        return '选择排序'


class InsertSort(BaseSort):
    """
    插入排序
    从第二个元素开始，倒着遍历前面的所有元素，看当前位置的元素是否比前面的元素要小，小就交换
    """

    @property
    def sort(self):
        self.before_sort()
        for i in range(1, self.num_len):
            for j in range(i, 0, -1):
                if self.num_list[j - 1] > self.num_list[j]:
                    self.num_list[j - 1], self.num_list[j] = self.num_list[j], self.num_list[j - 1]
                else:
                    break
        return self.num_list

    @property
    def name(self):
        return '插入排序'


class InsertSortOp(BaseSort):
    """
    优化插入排序
    只交换一次，记录比较位置的数，比较后如果前一个比后一个大，就将前一个后移，小的话就直接赋值给当前位置
    优化原因：提前终止内层循环，取消交换，而是使用赋值
    适用：近乎有序数组（大量相同）
    """

    @property
    def sort(self):
        self.before_sort()
        for i in range(1, self.num_len):
            temp = self.num_list[i]
            index = 0
            for j in range(i, 0, -1):
                # 注意判断条件必须用temp而不能使用self.num_list[i]，因为再不断地赋值过程中，self.num_list[i]已经改变
                if self.num_list[j - 1] > temp:
                    self.num_list[j] = self.num_list[j - 1]
                else:
                    index = j
                    break
            self.num_list[index] = temp

        return self.num_list

    @property
    def name(self):
        return '插入排序优化'


class BubbleSort(BaseSort):
    """
    冒泡排序
    """

    @property
    def sort(self):
        self.before_sort()
        for i in range(0, self.num_len):
            for j in range(1, self.num_len - i):
                if self.num_list[j] < self.num_list[j - 1]:
                    self.num_list[j], self.num_list[j - 1] = self.num_list[j - 1], self.num_list[j]
        return self.num_list

    @property
    def name(self):
        return '冒泡排序'


class ShellSort(BaseSort):
    """
    希尔排序
    """

    @property
    def name(self):
        return '选择排序'


class MergeSort(BaseSort):
    """
    归并排序
    """

    @property
    def sort(self):
        self.before_sort()
        self.__merge_sort(self.num_list, 0, self.num_len - 1)
        return self.num_list

    def __merge_sort(self, num_list, left, right):
        """
        递归使用归并排序
        """
        if left >= right:
            return
        # 这里不能用len(num_list),边界会出错，比如len为10，算出来mid=5此时mid靠后一位，而通过索引计算0+9算出mid=4
        mid = (left + right) // 2
        self.__merge_sort(num_list, left, mid)
        self.__merge_sort(num_list, mid + 1, right)
        # self.__merge(num_list, left, mid, right) # 优化之前
        # 优化一：
        if num_list[mid] > num_list[mid + 1]:
            self.__merge(num_list, left, mid, right)

    def __merge(self, num_list, l, mid, r):
        """
        将num_list[l, mid]和num_list[mid + 1, r]进行归并
        """
        aux = []
        for i in num_list:
            aux.append(i)

        i = l
        j = mid + 1
        # 因为我传入的时索引，所以如果我想要遍历到最后一个索引，必须用r+1
        for k in range(l, r + 1):
            # 这里写成 i == mid会显示越界  为什么还没想通，挖个坑
            # 想通了，是因为每次判断条件后把对应位置上的数放进去了 i++
            if i > mid:
                num_list[k] = aux[j]
                j += 1
            elif j > r:
                num_list[k] = aux[i]
                i += 1
            elif aux[i] < aux[j]:
                num_list[k] = aux[i]
                i += 1
            else:
                num_list[k] = aux[j]
                j += 1

    @property
    def name(self):
        return '归并排序'
