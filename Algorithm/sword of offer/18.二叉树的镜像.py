from collections import deque


class TreeNode(object):
    def __init__(self, x):
        self.x = x
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

    def mirror_bfs(self):
        ret = []
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            if node:
                ret.append(node.x)
                queue.append(node.right)
                queue.append(node.left)
        self.construct_tree(ret)
        return ret

    def bfs(self):
        ret = []
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            if node:
                ret.append(node.x)
                queue.append(node.left)
                queue.append(node.right)
        return ret


t1 = Tree()
t1.construct_tree([8, 6, 10, 5, 7, 9, 11])
print(t1.bfs())
print(t1.mirror_bfs())
print(t1.bfs())
