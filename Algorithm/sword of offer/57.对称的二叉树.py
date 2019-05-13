"""
通常我们有三种不同的二叉树遍历算法，即前序遍历、中序遍历和后序遍历。在这三种遍历算法中，都是先遍历左子结点再遍历右子结点。
我们是否可以定义一种遍历算法，先遍历右子结点再遍历左子结点？
比如我们针对前序遍历定义一种对称的遍历算法，即先遍历父节点，再遍历它的右子结点，最后遍历它的左子结点。
"""


class Node:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Tree:
    def __init__(self, num_list=None):
        if num_list:
            self._create_tree(num_list)
        else:
            self.head = None

    def _create_tree(self, num_list):
        self.head = Node(num_list.pop(0))
        s = []
        s.append(self.head)
        while s:
            node = s.pop(0)
            if node and node.val and num_list:
                node.left = Node(num_list.pop(0))
                s.append(node.left)
                if num_list:
                    node.right = Node(num_list.pop(0))
                    s.append(node.right)

    def bfs(self):
        node = self.head
        s = []
        ret = []
        s.append(node)
        while s:
            node = s.pop(0)
            if node:
                ret.append(node.val)
                s.append(node.left)
                s.append(node.right)
        print("层序遍历", ret)
        return ret

    def r_bfs(self):
        node = self.head
        s = []
        ret = []
        s.append(node)
        while s:
            node = s.pop(0)
            if node:
                ret.append(node.val)
                s.append(node.right)
                s.append(node.left)
        print("层序遍历", ret)
        return ret

    def is_symmetry(self):
        return self.bfs() == self.r_bfs()

    def pre(self):
        ret = []

        def __inner(t):
            ret.append(t.val)
            if t.left:
                __inner(t.left)
            if t.right:
                __inner(t.right)

        __inner(self.head)
        print("先序遍历", ret)
        return ret

    def r_pre(self):
        ret = []

        def __inner(t):
            ret.append(t.val)
            if t.left:
                __inner(t.right)
            if t.right:
                __inner(t.left)

        __inner(self.head)
        print("先序遍历", ret)
        return ret

    def is_symmetry2(self):
        return self.r_pre() == self.pre()


tree = Tree([1, 2, 2, 3, None, None, 3])
print(tree.is_symmetry())
print(tree.is_symmetry2())
