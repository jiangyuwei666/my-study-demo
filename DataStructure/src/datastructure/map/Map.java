package datastructure.map;


/**
 * Created By Jiangyuwei on 2019/7/22 17:44
 * Description:
 */
public class Map<K extends Comparable<K>, V> {

    private class Node{
        public K key;
        public V value;
        public Node left;
        public Node right;

        public Node(K key, V value){
            this.key = key;
            this.value = value;
            this.left = null;
            this.right = null;
        }

    }

    private Node root;
    private int size;

    public Map(){
        root = null;
        size = 0;
    }

    public int getSize() {
        return size;
    }

    public boolean isEmpty(){
        return size == 0;
    }

    public void add(K key, V value){
        root = add(key, value, root);
    }

    private Node add(K key, V value, Node root){
        if (root == null){
            size ++;
            return new Node(key, value);
        }
        if (root.key.compareTo(key) > 0)
            root.left = add(key, value, root.left);
        else if(root.key.compareTo(key) < 0)
            root.right = add(key, value, root.right);
        return root;
    }

    public V get(K key){
        return getNode(root, key).value;
    }

    private Node getNode(Node node, K key){
        if (node == null){
            return null;
        }
        if (node.key.compareTo(key) > 0){
            return getNode(node.left, key);
        }
        else if (node.key.compareTo(key) < 0){
            return getNode(node.right, key);
        }
        else
            return node;
    }

    public boolean contains(K key){
        Node node = getNode(root, key);
        return node != null;
    }

    public void set(K key, V value){
        Node node = getNode(root, key);
        node.value = value;
    }

    public Node minium(){
        return minium(root);
    }

    private Node minium(Node node){
        if (node.left == null)
            return node;
        else
            return node.left;
    }

    public void remove(K key){
        root = remove(root, key);
    }

    private Node remove(Node root, K key){
        if (root == null)
            return null;
        if (root.key.compareTo(key) > 0) {
            root.left = remove(root.left, key);
            return root;
        }
        else if (root.key.compareTo(key) < 0){
            root.right = remove(root.right, key);
            return root;
        }
        else {
            if (root.left == null){
                Node node = root.right;
                root.right = null;
                size --;
                return node;
            }
            else if (root.right == null){
                Node node = root.left;
                root.left = null;
                size --;
                return node;
            }
            else {
                Node node = minium(root.right);
                node.right = root.right;
                node.left = root.left;
                root.right = root.left = null;
                size --;
                return node;
            }
        }
    }
}
