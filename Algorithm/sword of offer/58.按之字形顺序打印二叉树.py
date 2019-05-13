from collections import deque


class TreeNode:
    def __init__(self, x):
        self.x = x
        self.left = None
        self.right = None


class Tree:
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
        """
        通过队列实现二叉树的层序遍历

        每次从队列中取出一个节点，同时把它的左右儿子节点入队列
        """
        result = []
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            if node:
                result.append(node.x)
                queue.append(node.left)
                queue.append(node.right)
        return result

    def print_z(self):
        ret = []
        flag = 1
        if not self.root:
            return ret

