from collections import deque


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Tree(object):
    def __init__(self):
        self.root = None

    def construct_tree(self, values=None):
        if not values:
            return None
        self.root = TreeNode(values[0])
        queue = deque([self.root])
        leng = len(values)
        nums = 1
        while nums < leng:
            node = queue.popleft()
            if node:
                node.left = TreeNode(values[nums]) if values[nums] else None
                queue.append(node.left)
                if nums + 1 < leng:
                    node.right = TreeNode(values[nums + 1]) if values[nums + 1] else None
                    queue.append(node.right)
                    nums += 1
                nums += 1

    def bfs(self):
        ret = []
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            if node:
                ret.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
        return ret

    def pre_traversal(self):
        ret = []

        def traversal(head):
            if not head:
                return
            ret.append(head.val)
            traversal(head.left)
            traversal(head.right)

        traversal(self.root)
        return ret

    def in_traversal(self):
        ret = []

        def traversal(head):
            if not head:
                return
            traversal(head.left)
            ret.append(head.val)
            traversal(head.right)

        traversal(self.root)
        return ret

    def post_traversal(self):
        ret = []

        def traversal(head):
            if not head:
                return
            traversal(head.left)
            traversal(head.right)
            ret.append(head.val)

        traversal(self.root)
        return ret


def sub_tree(tree1, tree2):
    if tree1 and tree2:
        if tree1.val == tree2.val:
            return tree1_has_tree2(tree1, tree2)
        else:
            return sub_tree(tree1.left, tree2) or sub_tree(tree1.right, tree2)
    else:
        return False


def tree1_has_tree2(tree1, tree2):
    if not tree2:  # 表示tree2已经遍历到头了
        return True
    if not tree1:  # 表示tree1已经遍历到根节点了，说明没有找到tree2，失败
        return False
    if tree1.val != tree2.val:  # 表示某个节点相等，但是其子树不等，失败
        return False
    # 上诉递归出口不满足，就继续往下匹配
    return tree1_has_tree2(tree1.left, tree2.left) and tree1_has_tree2(tree1.right, tree2.right)


if __name__ == '__main__':
    t1 = Tree()
    t1.construct_tree([1, 2, 3, None, 4, 5])
    print(t1.bfs())
    t2 = Tree()
    t2.construct_tree([2, None, 4])
    print(t2.bfs())
    print(sub_tree(t1.root, t2.root))
