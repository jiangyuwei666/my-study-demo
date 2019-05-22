"""
二叉搜索树中使用中序遍历
"""


class Node:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Tree:
    def __init__(self, num_list=None):
        self.root = None
        if num_list:
            for i in num_list:
                self.add_node(Node(i))

    def add_node(self, node):
        if not self.root:
            self.root = node
        else:
            root = self.root
            while root:
                if node.val < root.val:
                    if root.left:
                        root = root.left
                    else:
                        root.left = node
                        break
                elif node.val > root.val:
                    if root.right:
                        root = root.right
                    else:
                        root.right = node
                        break

    def bfs(self):
        ret = []
        s = [self.root]
        while s:
            node = s.pop(0)
            if node:
                ret.append(node.val)
                s.append(node.left)
                s.append(node.right)
        print(ret)

    def get_top_k(self, k):
        root = self.root
        ret = []
        s = []
        def __inner(root):
            if root:
                __inner(root.left)
                ret.append(root.val)
                __inner(root.right)

        __inner(root)
        return ret[k - 1]


tree = Tree([5, 3, 7, 2, 4, 6, 8])
tree.bfs()
print(tree.get_top_k(3))
