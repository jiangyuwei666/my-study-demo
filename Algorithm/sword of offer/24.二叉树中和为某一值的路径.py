"""

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

    def add_path(self, target):

        path_stack = []

        def __path(tree):
            if tree:
                path_stack.append(tree)
                current_sum = Tree.calculate(path_stack)
                if current_sum < target:
                    __path(tree.left)
                    __path(tree.right)

    @staticmethod
    def calculate(path_list):
        result = 0
        for i in path_list:
            result += i.val
        return result
