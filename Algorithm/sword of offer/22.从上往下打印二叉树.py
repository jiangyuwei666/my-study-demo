"""
二叉树的层序遍历
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
            __add(self.root, node)
        else:
            self.root = node

    def bfs(self):
        ret = []
        queue = []
        queue.append(self.root)
        while queue:
            node = queue.pop(0)
            if node:
                ret.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
        return ret


tree = Tree(arr_list=[6, 3, 5, 9, 7, 10, 1])
print(tree.bfs())
