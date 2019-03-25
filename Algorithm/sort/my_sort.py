from sort.SortTestHelper import *


class BaseSort:
    def __init__(self, n, swap_times=None, repeat=False):
        """
        :param n:
        :param swap_times: 有swap_times表示要生成几乎有序得数列
        """
        if swap_times:
            self.num_list = Helper.get_nearly_list(n, swap_times)
        elif repeat:
            self.num_list = Helper.get_repeat_list(n)
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
        # if left >= right:
        #     return

        # 这里不能用len(num_list),边界会出错，比如len为10，算出来mid=5此时mid靠后一位，而通过索引计算0+9算出mid=4

        # 优化二：对于小数组可以使用插入排序或者选择排序，避免递归调用
        if right - left < 2:
            for i in range(left + 1, right + 1):
                temp = num_list[i]
                index = 0
                # 注意这里left的边界
                for j in range(i, left - 1, -1):
                    if num_list[j] < temp:
                        num_list[j] = num_list[j - 1]
                    else:
                        index = j
                        break
                num_list[index] = temp
            return

        mid = (left + right) // 2
        self.__merge_sort(num_list, left, mid)
        self.__merge_sort(num_list, mid + 1, right)
        # self.__merge(num_list, left, mid, right) # 优化之前
        # 优化一：只对前面比后面大得进行排序
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


class MergeSortUp(BaseSort):
    """
    自底向上的归并
    适用于对链表进行排序
    """
    pass


class QuickSort(BaseSort):
    """
    快排
    快拍不适合近乎有序的
    快速排序不适合大量重复的
    """

    @property
    def sort(self):
        self.before_sort()
        self.__quick_sort(self.num_list, 0, self.num_len - 1)
        return self.num_list

    def __quick_sort(self, num_list, l, r):
        # 优化一：还是可以减少递归层数，在最后面的时候改为插入排序或者选择排序
        if r - l < 10:
            for i in range(l + 1, r + 1):
                temp = num_list[i]
                index = 0
                # 注意这里left的边界
                for j in range(i, l - 1, -1):
                    if num_list[j] < temp:
                        num_list[j] = num_list[j - 1]
                    else:
                        index = j
                        break
                num_list[index] = temp
            return
        p = self.__partition(num_list, l, r)
        self.__quick_sort(num_list, l, p - 1)
        self.__quick_sort(num_list, p + 1, r)

    def __partition(self, num_list, l, r):
        # 优化二：因为快拍不适合几乎有序，所以我们可以随机选择一个数出来，并且将它放在第一个位置
        s = random.randint(l, r)
        num_list[s], num_list[l] = num_list[l], num_list[s]
        v = num_list[l]
        j = l
        for i in range(l + 1, r + 1):
            if num_list[i] < v:
                # 与当前j的下一位进行交换
                num_list[i], num_list[j + 1] = num_list[j + 1], num_list[i]
                j += 1
        num_list[l], num_list[j] = num_list[j], num_list[l]
        return j

    @property
    def name(self):
        return "快速排序"


class QuickSort2(BaseSort):
    """
    快排针对于大量重复元素的优化
    """

    @property
    def sort(self):
        self.before_sort()
        self.__quick_sort(self.num_list, 0, self.num_len - 1)
        return self.num_list

    def __quick_sort(self, num_list, l, r):
        # 优化一：还是可以减少递归层数，在最后面的时候改为插入排序或者选择排序
        if r - l < 10:
            for i in range(l + 1, r + 1):
                temp = num_list[i]
                index = 0
                # 注意这里left的边界
                for j in range(i, l - 1, -1):
                    if num_list[j] < temp:
                        num_list[j] = num_list[j - 1]
                    else:
                        index = j
                        break
                num_list[index] = temp
            return
        p = self.__partition(num_list, l, r)
        self.__quick_sort(num_list, l, p - 1)
        self.__quick_sort(num_list, p + 1, r)

    def __partition(self, num_list, l, r):
        # 优化二：因为快拍不适合几乎有序，所以我们可以随机选择一个数出来，并且将它放在第一个位置
        # 优化三: 大量重复的优化是采用从两头往中间进行烧火棍的方式，这样可以跳过重复元素
        s = random.randint(l, r - 1)
        num_list[s], num_list[l] = num_list[l], num_list[s]
        v = num_list[l]
        j = r
        i = l + 1
        while True:
            while i <= r and num_list[i] < v:
                i += 1
            while j >= l + 1 and num_list[j] > v:
                j -= 1
            if j < i:
                break
            num_list[i], num_list[j] = num_list[j], num_list[i]
            j -= 1
            i += 1
        num_list[l], num_list[j] = num_list[j], num_list[l]
        return j

    @property
    def name(self):
        return "快速排序2"


class QuickSort3(BaseSort):
    """
    三路快拍
    三路快拍适用于有大量重复元素的数列
    原理：把一个数列分成三部分 大于v 等于v 小于v 这样每次递归只对大于和小于v的部分进行排序，节省了时间
    """

    @property
    def sort(self):
        self.before_sort()
        self.__quick_sort(self.num_list, 0, self.num_len - 1)
        return self.num_list

    def __quick_sort(self, num_list, l, r):
        # 优化一：还是可以减少递归层数，在最后面的时候改为插入排序或者选择排序
        if r - l < 10:
            for i in range(l + 1, r + 1):
                temp = num_list[i]
                index = 0
                # 注意这里left的边界
                for j in range(i, l - 1, -1):
                    if num_list[j] < temp:
                        num_list[j] = num_list[j - 1]
                    else:
                        index = j
                        break
                num_list[index] = temp
            return
        s = random.randint(l, r - 1)
        num_list[s], num_list[l] = num_list[l], num_list[s]
        v = num_list[l]
        lt = l
        gt = r + 1
        i = l + 1
        while i < gt:
            if num_list[i] < v:
                num_list[i], num_list[lt + 1] = num_list[lt + 1], num_list[i]
                lt += 1  # 此时lt指向 等于v那一部分的第一个
                i += 1
            elif num_list[i] > v:
                num_list[i], num_list[gt - 1] = num_list[gt - 1], num_list[i]
                gt -= 1
            else:
                i += 1
        num_list[l], num_list[lt] = num_list[lt], num_list[l]
        self.__quick_sort(num_list, l, lt - 1)
        self.__quick_sort(num_list, gt, r)

    @property
    def name(self):
        return "快速排序3"


class HeapSort(BaseSort):
    """
    原地堆排序
    先将数组变成一个最大堆，将最大元素放在堆的最后，再使剩下的变成最大堆
    左子节点：2 * i + 1
    右子节点：2 * i + 2
    父节点：（i - 1）//2
    最后一个非叶子节点的索引：（count - 1）//2
    """

    @property
    def sort(self):
        self.before_sort()
        # 找所有非叶子节点
        # 将数组构建成一个堆
        for i in range((self.num_len - 1) // 2, -1, -1):
            # 因为每个叶子节点可以看作是一个最大堆，所以网上走，将每个非叶子节点何其子节点也变成最大堆，就是用shift_down操作，将子树的根节点与其子节点进行交换
            self.__shift_down(self.num_list, self.num_len, i)
        for j in range(self.num_len - 1, 0, -1):
            # 交换最后一个和根节点
            self.num_list[0], self.num_list[j] = self.num_list[j], self.num_list[0]
            # 将顶部不是最大的那个值往下调，一直要调到当前不是最大的j那个位置
            self.__shift_down(self.num_list, j, 0)
        return self.num_list

    def __shift_down(self, num_list, num_len, k):
        """

        :param num_list: 操作的数组
        :param num_len: 总共要操作多少个
        :param k: 需要交换的索引
        :return:
        """
        while 2 * k + 1 < num_len:
            j = 2 * k + 1
            # 如果存在右子节点并且右子节点比左子节点大
            if j + 1 < num_len and num_list[j + 1] > num_list[j]:
                j += 1
            if num_list[k] > num_list[j]:
                break
            num_list[k], num_list[j] = num_list[j], num_list[k]
            k = j

    @property
    def name(self):
        return "堆排序"
