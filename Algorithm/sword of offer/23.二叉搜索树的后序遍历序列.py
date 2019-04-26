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

    def order_traversal(self):
        ret = []

        def inner(tree):
            if tree.left:
                inner(tree.left)
            if tree.right:
                inner(tree.right)
            ret.append(tree.val)

        inner(self.root)
        return ret


tree = Tree(arr_list=[6, 3, 5, 9, 7, 10, 1])
print(tree.order_traversal())
