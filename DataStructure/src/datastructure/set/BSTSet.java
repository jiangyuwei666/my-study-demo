package datastructure.set;

import datastructure.bst.BST;

/**
 * Created By Jiangyuwei on 2019/7/20 20:50
 * Description:
 */
public class BSTSet<E extends Comparable<E>> implements Set<E> {

    private BST<E> bst;

    public BSTSet() {
        bst = new BST<>();
    }

    @Override
    public void add(E e) {
        bst.addNode(e);
    }

    @Override
    public void remove(E e) {

    }

    @Override
    public boolean contains(E e) {
        return bst.contains(e);
    }

    @Override
    public int getSize() {
        return bst.size;
    }

}
