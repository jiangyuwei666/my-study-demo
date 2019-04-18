class Node:

    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class BST:

    def __init__(self):
        self.root = None
        self.size = 0

    def get_size(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def add_node(self, node):
        if not self.root:
            self.root = node
            self.size += 1

        def __add_node(root):
            if root.val == node.val:
                return
            elif root.val > node.val:
                if not root.left:
                    root.left = node
                    self.size += 1
                    return
                __add_node(root.left)
            elif root.val < node.val:
                if not root.right:
                    root.right = node
                    self.size += 1
                    return
                __add_node(root.right)

        __add_node(self.root)

    def add_node2(self, node):
        """
        有返回值的add node方法
        """

        def __add_node(root):
            if not root:
                self.size += 1
                return node
            if root.val > node.val:
                root.left = __add_node(root.left)
            elif root.val < node.val:
                root.right = __add_node(root.right)

            return root

        self.root = __add_node(self.root)

    def has_node(self, x):

        node = Node(x)

        def __has_node(root):
            if not root:
                return False
            if root.val == node.val:
                return True
            elif root.val > node.val:
                return __has_node(root.left)
            else:
                return __has_node(root.right)

        return __has_node(self.root)

    def print_tree(self):
        """
        前序遍历
        """
        result = []

        def __print(root):
            if not root:
                return
            result.append(root.val)
            __print(root.left)
            __print(root.right)

        __print(self.root)

        return result

    def print_tree2(self):
        """
        中序遍历
        """
        result = []

        def __print(root):
            if not root:
                return
            __print(root.left)
            result.append(root.val)
            __print(root.right)

        __print(self.root)

        return result

    def print_tree3(self):
        """
        后序遍历
        """
        result = []

        def __print(root):
            if not root:
                return

            __print(root.left)
            __print(root.right)
            result.append(root.val)

        __print(self.root)

        return result


if __name__ == '__main__':
    bst = BST()
    nums = [5, 3, 6, 6, 8, 4, 2]
    for i in nums:
        bst.add_node(Node(i))
    print(bst.print_tree3())
    print(bst.size)
    print(bst.has_node(0))
