package algorithm.sort;

import datastructure.array.Array;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;

/**
 * Created By Jiangyuwei on 2019/8/6 12:49
 * Description:
 */
public class BaseSort {

    public int[] arr;

    BaseSort(int n){
        arr = new int[n];
        for (int i = 0; i < n; i ++){
            Random random = new Random();
            arr[i] = random.nextInt(100);
        }
    }
    BaseSort(int n, int m){
        arr = new int[n];
        for (int i = 0; i < n; i ++){
            Random random = new Random();
            arr[i] = random.nextInt(m);
        }
    }

    public void sort(){}

    public void sortedList(){
        ArrayList<Integer> res = new ArrayList<>();
        for (int i:arr){
            res.add(i);
        }
        System.out.println("before sort:" + res);
        sort();
        res.clear();
        for (int i:arr){
            res.add(i);
        }
        System.out.println(" after sort:" + res);
    }

}
