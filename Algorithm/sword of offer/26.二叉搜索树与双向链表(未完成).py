"""
中序遍历左右子树，将左右子树通过根节点连接起来
"""


class Node:

    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Tree:

    def __init__(self, arr_list=None):
        self.tree = None
        if arr_list:
            for i in arr_list:
                self.insert(Node(i))

    def insert(self, node):

        def __insert(tree):
            if node.val < tree.val:
                if tree.left:
                    __insert(tree.left)
                else:
                    tree.left = node
            elif node.val > tree.val:
                if tree.right:
                    __insert(tree.right)
                else:
                    tree.right = node
        if not self.tree:
            self.tree = node
        else:
            m = self.tree
            __insert(m)

    def bfs(self):
        t = self.tree
        queue = []
        ret = []
        queue.append(t)
        while queue:
            node = queue.pop(0)
            if node:
                ret.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
        print(ret)


    def create_list(self):
        pass



tree = Tree(arr_list=[10, 6, 14, 4, 8, 12, 16])
tree.bfs()
