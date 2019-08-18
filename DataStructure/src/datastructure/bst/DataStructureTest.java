package datastructure.bst;

import datastructure.bst.BST;
import datastructure.bst.TreeNode;

public class DataStructureTest {

    public static void main(String[] args) {
        BST<Integer> tree = new BST<>();
        tree.addNode(5);
        tree.addNode(3);
        tree.addNode(7);
        tree.addNode(1);
        tree.addNode(2);
        tree.addNode(4);
        tree.bfs();
        System.out.println(tree.contains(3));
        System.out.println(tree.contains(9));
        tree.preOrder();
        tree.preOrder1();
        tree.inOrder();
        tree.inOrder1();
//        System.out.println(tree.removeMin());
//        tree.bfs();
        tree.remove(1);
        tree.bfs();
    }

}
