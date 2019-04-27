"""
考虑到要从头到尾去遍历树来查找路径，就只能选择前序遍历
采用栈的思想，遍历某个节点的时候，进行入栈，再对其左子树进行考察，直至根节点，然后是右子树，是一个递归的过程
入栈后计算当前站内节点值的总和，如果当前值小于目标值，就这递归遍历
否则如果当前值等于目标值，先判断是否走到了根节点(否则就不是一条路径)，如果是就将其添加到相应结果集当中
"""


class Node:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Tree:
    def __init__(self, root=None, arr_list=None):
        self.root = root
        if arr_list:
            for i in arr_list:
                self.add(Node(i))

    def add(self, node):

        def __add(tree, node):
            if tree.val == node.val:
                return
            elif node.val > tree.val:
                if tree.right:
                    __add(tree.right, node)
                else:
                    tree.right = node
            else:
                if tree.left:
                    __add(tree.left, node)
                else:
                    tree.left = node

        if self.root:
            s = self.root
            __add(s, node)
        else:
            self.root = node

    def find_path(self, target):

        path_stack = []
        ret = []

        def __path(tree):
            if tree:
                path_stack.append(tree)
                current_sum = Tree.calculate(path_stack)
                if current_sum < target:
                    __path(tree.left)
                    __path(tree.right)
                elif current_sum == target:
                    if not tree.left and not tree.right:
                        s = []
                        for i in path_stack:
                            s.append(i.val)
                        ret.append(s)
                path_stack.pop()

        __path(self.root)
        return ret

    @staticmethod
    def calculate(path_list):
        result = 0
        for i in path_list:
            result += i.val
        return result


tree = Tree(arr_list=[10, 5, 4, 12, 7])
print(tree.find_path(22))
tree = Tree(arr_list=[5, 4, 3, 2, 1])
print(tree.find_path(12))
