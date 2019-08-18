package datastructure.heap;

import datastructure.array.Array;

/**
 * Created By Jiangyuwei on 2019/7/23 11:23
 * Description:
 */
public class MaxHeap<E extends Comparable<E>> {

    private Array<E> data;

    public MaxHeap(){
        data = new Array<>();
    }

    public MaxHeap(int capacity){
        data = new Array<>(capacity);
    }

    public MaxHeap(E[] arr){
        data = new Array<>(arr);
        for (int i = parent(arr.length - 1); i >= 0; i --)
            siftDown(i);
    }

    public int size(){
        return data.getSize();
    }

    public boolean isEmpty(){
        return data.isEmpty();
    }

    private int parent(int index){
        if (index == 0)
            throw new IllegalArgumentException("");
        return (index - 1) / 2;
    }

    private int leftChild(int index){
        return index * 2 + 1;
    }

    private int rightChild(int index){
        return index * 2 + 2;
    }

    public void add(E e){
        data.addLast(e);
        siftUp(data.getSize() - 1);
    }
    //
    private void siftUp(int index){
        while (index > 0 && data.get(parent(index)).compareTo(data.get(index)) < 0){
            data.swap(index, parent(index));
            index = parent(index);
        }
    }

    public E extractMax(){
        data.swap(0, data.getSize() - 1);
        E max = data.removeLast();
        siftDown(0);
        return max;
    }

    private void siftDown(int index){
        while (leftChild(index) < data.getSize()){
            int j = leftChild(index);
            if (j + 1 < data.getSize() && data.get(j).compareTo(data.get(j + 1)) < 0)
                j ++;
            if (data.get(j).compareTo(data.get(index)) > 0){
                data.swap(j, index);
                index = j;
            }
            else
                break;
        }
    }

    public static void heapify(int[] arr){
        int last = (arr.length - 1 - 1) / 2;
        for (int i = last; i >= 0; i --){
            int k = i;
            while (k * 2 + 1 < arr.length){
                int j = 2 * k + 1;
                if (j + 1 < arr.length && arr[j + 1] > arr[j])
                    j ++;
                if (arr[k] < arr[j]){
                    int temp = arr[k];
                    arr[k] = arr[j];
                    arr[j] = temp;
                    k = j;
                }
                else
                    break;
            }
        }
    }


}
