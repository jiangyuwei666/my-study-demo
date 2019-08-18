package datastructure.heap;

import datastructure.array.Array;

import java.util.ArrayList;

/**
 * Created By Jiangyuwei on 2019/7/23 13:10
 * Description:
 */
public class HeapTest {
    public static void main(String[] args) {
        MaxHeap<Integer> maxHeap = new MaxHeap();
        int[] a = {3, 4, 1, 6, 4, 23, 4, 67, 42, 345, 2};
        for (int i : a)
            maxHeap.add(i);
        ArrayList<Integer> res = new ArrayList<>();
        while (maxHeap.size() > 0) {
            res.add(maxHeap.extractMax());
        }
        System.out.println(res);
        res.clear();
        for (int i : a)
            res.add(i);
        System.out.println(res);
        Integer[] b = {3, 4, 1, 6, 4, 23, 4, 67, 42, 345, 2};
        MaxHeap<Integer> maxHeap1 = new MaxHeap<>(b);
        res.clear();
        while (maxHeap1.size() > 0) {
            res.add(maxHeap1.extractMax());
        }
        System.out.println(res);
        MaxHeap.heapify(a);
        res.clear();
        for (int i : a)
            res.add(i);
        System.out.println(res);
    }
}


