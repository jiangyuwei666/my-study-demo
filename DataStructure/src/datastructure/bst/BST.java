package datastructure.bst;

import java.util.*;

import static java.util.Comparator.reverseOrder;

public class BST<E extends Comparable<E>> {

    public TreeNode<E> root;
    public int size;

    public BST() {
        this.root = null;
    }

    public int size() {
        return size;
    }

    public TreeNode<E> getRoot() {
        return root;
    }

    public void addNode(E e){
        if (root == null){
            root = new TreeNode<E>(e);
            size ++;
        }
        else
            add(root, e);
    }

    private void add(TreeNode<E> node, E e){
        if (e.compareTo(node.e) > 0){
            if (node.right != null)
                add(node.right, e);
            else{
                node.right = new TreeNode<>(e);
                size ++;
            }

        }
        else if (e.compareTo(node.e) < 0){
            if (node.left != null)
                add(node.left, e);
            else{
                node.left = new TreeNode<>(e);
                size ++;
            }
        }
    }

    public boolean contains(E e){
        return contains(root, e);
    }

    private boolean contains(TreeNode<E> root, E e){
        if (root == null)
            return false;
        if (root.e.compareTo(e) < 0)
            return contains(root.right, e);
        else if (root.e.compareTo(e) > 0)
            return contains(root.left, e);
        else
            return true;
    }
    //先序遍历
    public void preOrder(){
        ArrayList<E> res = new ArrayList<>();
        preOrder(root, res);
        System.out.println(res);
    }

    public void preOrder1(){
        ArrayList<E> res = new ArrayList<>();
        Stack<TreeNode<E>> s = new Stack<>();
        TreeNode<E> node = root;
        while (node != null || s.size() > 0){
            if (node != null){
                s.push(node);
                res.add(node.e);
                node = node.left;
            }
            else {
                node = s.pop();
                node = node.right;
            }
        }
        System.out.println(res);
    }

    private void preOrder(TreeNode<E> root, ArrayList<E> res){
        if (root == null)
            return;
        res.add(root.e);
        preOrder(root.left, res);
        preOrder(root.right, res);
    }

    public void inOrder(){
        ArrayList<E> res = new ArrayList<>();
        inOrder(root, res);
        System.out.println(res);
    }

    public void inOrder1(){
        ArrayList<E> res = new ArrayList<>();
        Stack<TreeNode<E>> s = new Stack<>();
        TreeNode<E> cur = root;
        while (cur != null || s.size() > 0){
            if (cur != null){
                s.push(cur);
                cur = cur.left;
            }
            else {
                cur= s.pop();
                res.add(cur.e);
                cur = cur.right;
            }
        }
        System.out.println(res);
    }

    private void inOrder(TreeNode<E> root, ArrayList<E> res){
        if (root == null)
            return;
        inOrder(root.left, res);
        res.add(root.e);
        inOrder(root.right, res);
    }

    //层序遍历
    public void bfs(){
        ArrayList<E> res = new ArrayList<>();
        LinkedList<TreeNode<E>> list = new LinkedList<>();
        list.addLast(root);
        while (list.size() != 0){
            TreeNode<E> node = list.removeFirst();
            if (node != null){
                res.add(node.e);
                list.addLast(node.left);
                list.addLast(node.right);
            }
        }
        List<E> a = new LinkedList<>();
        System.out.println(res);
    }

    public E mininum(){
        if (size == 0)
            throw new IllegalArgumentException("BST is empty");
        return mininum(root).e;
    }

    private TreeNode<E> mininum(TreeNode<E> root){
        if (root.left == null)
            return root;
        return mininum(root.left);
    }

    public E removeMin(){
        E ret = mininum();
        root = removeMin(root);
        return ret;
    }

    private TreeNode<E> removeMin(TreeNode<E> root){
        if (root.left == null){
            TreeNode<E> rightNode = root.right;
            root.right = null;
            size --;
            return rightNode;
        }
        root.left = removeMin(root.left);
        return root;
    }

    public void remove(E e){
        // 将删除元素后的树赋值给当前根节点
        root = remove(root, e);
    }

    private TreeNode<E> remove(TreeNode<E> node, E e){
        //注意这里的返回值不是至删除的节点，而是删除这个节点后改变的那棵子树的根节点
        if (node == null)
            return null;
        // 当前节点比待删除元素大，去左子树找
        if (node.e.compareTo(e) > 0){
            node.left = remove(node.left, e);
            return node;
        }
        // 当前节点比待删除元素小，去右子树找
        else if (node.e.compareTo(e) < 0){
            node.right = remove(node.right, e);
            return node;
        }
        else {
            // 判断左子树是否为空，如果为空，删除后，直接将右子树接在上一个节点的左子树位置
            // 即返回当前节点的右子树节点即可
            if (node.left == null){
                TreeNode<E> rightNode = node.right;
                size --;
                node.right = null;
                return rightNode;
            }
            // 判断右子树是否为空，如果为空，删除后，直接将左子树接在上一个节点的右子树位置
            // 即返回当前节点的右子树即可
            if (node.right == null){
                TreeNode<E> leftNode = node.left;
                size -- ;
                node.left = null;
                return leftNode;
            }
            // 都不为空操作
            // 先将当前节点右子树中找到最小节点，取出来，作为当前节点
            // 将当前节点的左子树连接在该节点上，右子树(删除该节点后的子树)连接在该节点的右子树上
            // 最后返回，返回右会有一个节点的孩子节点(删除的那个节点)来接住这个节点
            TreeNode<E> newNode = mininum(node.right);
            removeMin(node.right);
            newNode.left = node.left;
            newNode.right = node.right;
            return newNode;
        }
    }

}
