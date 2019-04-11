"""
先通过前序遍历找到根节点(第一个)，再在中序遍历中将整个树分为左子树和右子树。再在前序遍历中找到左右子树，重复以上操作（递归）
"""
from collections import deque


class TreeNode:
    def __init__(self, x):
        self.x = x
        self.left = None
        self.right = None


class Tree:
    def __init__(self):
        self.root = None

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


def construct_tree(preorder, inorder):
    if not preorder or not inorder:
        return None
    first = preorder[0]
    first_index_in_inorder = inorder.index(first)
    root = TreeNode(preorder[0])
    root.left = construct_tree(preorder[1:first_index_in_inorder + 1], inorder[:first_index_in_inorder + 1])
    root.right = construct_tree(preorder[first_index_in_inorder + 1:], inorder[first_index_in_inorder + 1:])
    return root


t = Tree()
root = construct_tree([1, 2, 4, 7, 3, 5, 6, 8], [4, 7, 2, 1, 5, 3, 8, 6])
t.root = root
print(t.print_tree())
print(t.bfs())
