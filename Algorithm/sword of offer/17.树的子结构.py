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

    def print_tree(self):
        """
        先序遍历，如果是一样的就说明生成成功了
        """
        result = []

        def _print(head):
            if not head:
                return None
            result.append(head.x)
            _print(head.left)
            _print(head.right)

        _print(self.root)
        return result


def sub_tree(tree1, tree2):
    if tree1 and tree2:
        if tree1.x == tree2.x:
            return sub_tree(tree1.left, tree2.left) and sub_tree(tree1.right, tree2.right)
        else:
            return sub_tree(tree1.left, tree2) or sub_tree(tree1.right, tree2)
    if not tree1 and tree2:
        return False
    return True

t1 = Tree()
t1.construct_tree([1, 2, 3, None, 4, 5])
print(t1.bfs())
t2 = Tree()
t2.construct_tree([2, None, 4])
print(t2.bfs())
print(sub_tree(t1.root, t2.root))
