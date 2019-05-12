"""
1.如果此节点有右子树，下一个节点为右子节点的最左边的节点。
2.如果此节点没有右子树，并且如果此节点是其父节点的左子节点，则下一个节点为父节点。
3.如果此节点没有右子树，并且如果此节点是其父节点的右子节点，则一直向上找，直到找到第一个是其父节点左节点的节点，下一个节点就为此节点。
"""


class Node:
    def __init__(self, x, pre=None):
        self.val = x
        self.left = None
        self.right = None
        self.pre = pre


class Tree:
    def __init__(self, head=None, node_list=None):
        self.head = head
        if node_list:
            self.create_tree(node_list)

    def create_tree(self, node_list):
        s = []
        head = Node(node_list.pop(0))
        self.head = head
        s.append(head)
        while s:
            node = s.pop(0)
            if node_list:
                node.left = Node(node_list.pop(0), pre=node)
                s.append(node.left)
                if node_list:
                    node.right = Node(node_list.pop(0), pre=node)
                    s.append(node.right)

    def bfs(self):
        head = self.head
        m = []
        ret = []
        m.append(head)
        while m:
            node = m.pop(0)
            if node:
                ret.append(node.val)
                m.append(node.left)
                m.append(node.right)
        print(ret)

    def get_nodes(self):
        """
        获取所有节点
        """
        head = self.head
        m = []
        ret = []
        m.append(head)
        while m:
            node = m.pop(0)
            if node:
                ret.append(node)
                m.append(node.left)
                m.append(node.right)
        return ret

    def find_next(self, node):
        if node.right:
            n = node.right
            if n.left:
                while n.left:
                    n = n.left
            return n
        else:
            if node.pre.left == node:  # 当前节点是父节点的左子节点
                return node.pre
            elif node.pre.right == node:  # 当前节点是父节点的右子节点，并且当前节点没有右子树的话
                n = node.pre
                while not n.left:
                    n = n.pre
                return n.pre

tree = Tree(node_list=[1, 2, 3, 4, 5])
node_list = tree.get_nodes()
print(tree.find_next(node_list[0]).val)
tree.bfs()
