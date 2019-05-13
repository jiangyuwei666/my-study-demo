"""
通过变量来记录当前层数，并计算该层节点个数
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

    def bfs_level(self):
        level = 1
        level_count = 1
        result = []
        current = []
        s = []
        s.append(self.head)
        while s:
            node = s.pop(0)
            if node:
                current.append(node.val)
                # level += 1 if len(current) > level_count else 0
                # level_count = 2 ** (level - 1) if len(current) > level_count else level_count
                if len(current) == level_count:
                    result.append(current)
                    level += 1
                    level_count = 2 ** (level - 1)
                    current = []  # 这里不能使用clear，因为可变类型传进去后，还能改变值，相当于浅拷贝
                s.append(node.left)
                s.append(node.right)
        result.append(current)

        for i in result:
            print(i)


tree = Tree([1, 2, 3, 4, 5, 6, 7, 8, 9])
tree.bfs_level()
