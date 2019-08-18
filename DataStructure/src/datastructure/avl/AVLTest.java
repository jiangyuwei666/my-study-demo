package datastructure.avl;

/**
 * Created By Jiangyuwei on 2019/8/1 19:32
 * Description:
 */
public class AVLTest {

    public static void main(String[] args) {
        AVLTree<Integer, String> tree = new AVLTree<>();
        tree.add(1,"asd");
        tree.add(2,"qwed");
        tree.add(3,"aasdsd");
        tree.add(4,"aasdd");
        tree.add(5,"asasds");
        tree.add(6,"asasds");
        tree.add(7,"asasds");
        tree.add(8,"asasds");
        tree.add(9,"asasds");
        tree.add(0,"asasds");
        tree.bfs();
        tree.remove(4);
        tree.bfs();
    }

}
