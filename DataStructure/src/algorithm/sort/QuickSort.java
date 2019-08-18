package algorithm.sort;

/**
 * Created By Jiangyuwei on 2019/8/6 12:39
 * Description:
 */
public class QuickSort extends BaseSort {

    QuickSort(int n) {
        super(n);
    }

    QuickSort(int n, int m) {
        super(n, m);
    }

    @Override
    public void sort() {
        sort3(this.arr, 0, this.arr.length - 1);
    }

    private void sort(int[] arr, int l, int r){
        if (l >= r)
            return;
        int p = partition(arr, l, r);
        sort(arr, l, p-1);
        sort(arr, p + 1, r);
    }

    //返回一个索引p，在p左边都是比p位置小的元素，在p右边都是比p大的元素
    private int partition(int[] arr, int l, int r){
        int j = l;
        for (int i = l + 1; i <= r; i ++){
            if (arr[i] < arr[l]){
                int temp = arr[i];
                arr[i] = arr[j + 1];
                arr[j + 1] = temp;
                j ++;
            }
        }
        int temp = arr[j];
        arr[j] = arr[l];
        arr[l] = temp;
        return j;
    }

    private void sort2(int[] arr, int l, int r){
        if (l >= r)
            return;
        int p = partition2(arr, l, r);
        sort2(arr, l, p - 1);
        sort2(arr, p + 1, r);
    }

    private int partition2(int[] arr, int l, int r){
        int i = l + 1;
        int j = r;
        while(true){
            while (i <= r && arr[i] < arr[l])
                i ++;
            while (j >= l + 1 && arr[j] > arr[l])
                j --;
            if (i > j)
                break;
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
            i ++;
            j --;
        }
        int temp = arr[j];
        arr[j] = arr[l];
        arr[l] = temp;
        return j;
    }

    private void sort3(int[] arr, int l, int r){
        if (l >= r)
            return;
        int lt = l; // 表示从[l...lt] < arr[l]
        int i = l + 1; // 表示当前遍历的元素，并且[lt...i] == arr[l]
        int gt = r + 1;
        while(i < gt){
            if (arr[i] > arr[l]){
                int temp = arr[i];
                arr[i] = arr[gt - 1];
                arr[gt - 1] = temp;
                gt --;
            }
            else if (arr[i] < arr[l]){
                int temp = arr[i];
                arr[i] = arr[lt + 1];
                arr[lt + 1] = temp;
                i ++;
                lt ++;
            }
            else {
                i ++;
            }
        }
        int temp = arr[l];
        arr[l] = arr[lt];
        arr[lt] = temp;
        sort3(arr, l, lt - 1);
        sort3(arr, gt, r);
    }
}
