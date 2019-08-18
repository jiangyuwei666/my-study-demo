package datastructure.set;

/**
 * Created By Jiangyuwei on 2019/7/20 20:49
 * Description:
 */
public interface Set<E> {

    void add(E e);
    void remove(E e);
    boolean contains(E e);
    int getSize();

}
