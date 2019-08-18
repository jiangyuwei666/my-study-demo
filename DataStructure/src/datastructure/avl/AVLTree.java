package datastructure.avl;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;

/**
 * Created By Jiangyuwei on 2019/8/1 11:24
 * Description:
 */
public class AVLTree<K extends Comparable<K>, V> {

    private class Node {
        public K key;
        public V value;
        public Node left;
        public Node right;
        public int height;

        public Node(K key, V value) {
            this.key = key;
            this.value = value;
            left = null;
            right = null;
            height = 1;//维护当前节点的高度
        }
    }

    private Node root;
    private int size;

    public AVLTree() {
        root = null;
        size = 0;
    }

    public int getSize() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    private int getHeight(Node node) {
        if (node == null)
            return 0;
        return node.height;
    }

    // 获取平衡因子(左右子树的高度差)
    private int getBalanceFactor(Node node) {
        if (root == null)
            return 0;
        return getHeight(node.left) - getHeight(node.right);
    }

    public boolean isBalanced() {
        return isBalanced(root);
    }

    private boolean isBalanced(Node node) {
        if (node == null)
            return true;
        if (Math.abs(getBalanceFactor(node)) > 1)
            return false;
        return isBalanced(node.left) && isBalanced(node.right);
    }

    public void add(K key, V value) {
        root = add(key, value, root);
    }

    //向树中递归插入节点
    private Node add(K key, V value, Node node) {
        if (node == null) {
            return new Node(key, value);
        }
        if (key.compareTo(node.key) < 0)
            node.left = add(key, value, node.left);
        else if (key.compareTo(node.key) > 0)
            node.right = add(key, value, node.right);
        else
            node.value = value;

        node.height = 1 + Math.max(getHeight(node.left), getHeight(node.right));

        //当前节点不平衡，因为左边子树高度比右边子树高度超过了1，且左子树的平衡因子大于0（这个时候整个树是向左倾斜，左子树高了）
        if (getBalanceFactor(node) > 1 && getBalanceFactor(node.left) >= 0) {
            node = rightRotate(node);
        } else if (getBalanceFactor(node) < -1 && getBalanceFactor(node.right) <= 0) {
            node = leftRotate(node);
        } else if (getBalanceFactor(node) > 1 && getBalanceFactor(node.left) < 0) {
            node.left = leftRotate(node.left);
            node = rightRotate(node);
        } else if (getBalanceFactor(node) < -1 && getBalanceFactor(node.right) > 0) {
            node.right = rightRotate(node.right);
            node = leftRotate(node);
        }
        return node;
    }

    // 对节点y进行向右旋转操作，返回旋转后新的根节点x
    //        y                              x
    //       / \                           /   \
    //      x   T4     向右旋转 (y)        z     y
    //     / \       - - - - - - - ->    / \   / \
    //    z   T3                       T1  T2 T3 T4
    //   / \
    // T1   T2
    private Node rightRotate(Node y) {
        Node x = y.left;
        Node T3 = x.right;
        x.right = y;
        y.left = T3;
        y.height = Math.max(getHeight(y.left), getHeight(y.right)) + 1;
        x.height = Math.max(getHeight(x.left), getHeight(x.right)) + 1;
        return x;
    }

    // 对节点y进行向左旋转操作，返回旋转后新的根节点x
    //    y                             x
    //  /  \                          /   \
    // T1   x      向左旋转 (y)       y     z
    //     / \   - - - - - - - ->   / \   / \
    //   T2   z                    T1 T2 T3 T4
    //       / \
    //      T3 T4
    private Node leftRotate(Node y) {
        Node x = y.right;
        Node T2 = x.left;
        x.left = y;
        y.right = T2;
        y.height = Math.max(getHeight(y.left), getHeight(y.right)) + 1;
        x.height = Math.max(getHeight(x.left), getHeight(x.right)) + 1;
        return x;
    }

    public void bfs() {
//        HashMap<K, V> res = new HashMap<>();
        ArrayList<K> res = new ArrayList<>();
        LinkedList<Node> queue = new LinkedList<>();
        queue.addLast(root);
        while (queue.size() > 0){
            Node n = queue.removeFirst();
//            System.out.println(n.key);
            if (n != null){
                res.add(n.key);
                queue.addLast(n.left);
                queue.addLast(n.right);
            }
            else
                res.add(null);
        }
        System.out.println(res);
    }

    public void remove(K key){
        root = remove(root, key);
    }

    private Node remove(Node node, K key){
        if (node == null)
            return null;
        // 不能直接返回，使用这个retNode变量接住删除后的根节点，然后后续可以对这个节点进行平衡维护
        Node retNode;
        if (key.compareTo(node.key) > 0){
            node.right = remove(node.right, key);
//            return node;
            retNode = node;
        }
        else if (key.compareTo(node.key) < 0){
            node.left = remove(node.left, key);
//            return node;
            retNode = node;
        }
        else {
            if (node.left == null){
                Node rightNode = node.right;
                size -- ;
                node.right = null;
//                return rightNode;
                retNode = rightNode;

            }
            else if (node.right == null){
                Node leftNode = node.left;
                size -- ;
                node.left = null;
//                return leftNode;
                retNode = leftNode;
            }
            else {
                Node resNode = node.right;
                if (resNode.left == null){
                    node.right = resNode.right;
                }
                else {
                    while (resNode.left.left != null)
                        resNode = resNode.left;
                    Node t = resNode.left;
                    resNode.left = null;
                    resNode = t;
                }
                resNode.left = node.left;
                resNode.right = node.right;
                node.left = null;
                node.right = null;
//                return resNode;
                retNode = resNode;
            }
        }
        if(retNode == null)
            return null;
        // 更新height
        retNode.height = 1 + Math.max(getHeight(retNode.left), getHeight(retNode.right));
        //计算平衡因子
        int balance = getBalanceFactor(retNode);
        if (balance > 1 && getBalanceFactor(retNode.left) >= 0)
            return rightRotate(retNode);
        if (balance < -1 && getBalanceFactor(retNode.right) <= 0)
            return leftRotate(retNode);
        if (balance > 1 && getBalanceFactor(retNode.left) < 0){
            retNode.left = leftRotate(retNode.left);
            return rightRotate(retNode);
        }if (balance < -1 && getBalanceFactor(retNode.right) > 0){
            retNode.right = rightRotate(retNode.right);
            return leftRotate(retNode);
        }
        return retNode;
    }

}
