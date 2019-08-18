package algorithm.sort;

/**
 * Created By Jiangyuwei on 2019/8/6 17:28
 * Description:
 */
public class HeapSort extends BaseSort {

    HeapSort(int n) {
        super(n);
    }

    HeapSort(int n, int m) {
        super(n, m);
    }

    @Override
    public void sort() {
        sort(this.arr, this.arr.length - 1);
    }

    private void sort(int[] arr, int n){
        for (int k = (n - 1) / 2; k >= 0; k --){
            shifDown(arr, n, k);
        }
        for (int k = n; k >= 0; k --){
            int temp = arr[k];
            arr[k] = arr[0];
            arr[0] = temp;
            shifDown(arr, k, 0);
        }
    }

    private void shifDown(int[] arr, int n, int index){
        while (index * 2 + 1 < n){
            int j = index * 2 + 1;
            if (j + 1 < n && arr[j] < arr[j + 1])
                j ++;
            if (arr[j] < arr[index])
                break;
            int temp = arr[j];
            arr[j] = arr[index];
            arr[index] = temp;
            index = j;
        }
    }

}
