package algorithm.sort;

/**
 * Created By Jiangyuwei on 2019/8/6 12:44
 * Description:
 */
public class MergeSort extends BaseSort {

    MergeSort(int n) {
        super(n);
    }

    MergeSort(int n, int m) {
        super(n, m);
    }

    @Override
    public void sort() {
        sort(this.arr, 0, this.arr.length - 1);
    }

    private void sort(int[] arr, int l, int r) {
        if (l >= r)
            return;
        int mid = (l + r) / 2;
        sort(this.arr, l, mid);
        sort(this.arr, mid + 1, r);
        merge(arr, l, mid, r);
    }

    private void merge(int[] arr, int l, int mid, int r) {
        int[] aux = new int[r - l + 1];
        System.arraycopy(arr, l, aux, 0, r - l + 1);
        int i = l, j = mid + 1;
        for (int k = l; k <= r; k ++){
            if (i > mid){
                arr[k] = aux[j - l];
                j ++;
            }
            else if (j > r){
                arr[k] = aux[i - l];
                i ++;
            }
            else if(aux[i - l] > aux[j - l]){
                arr[k] = aux[j - l];
                j ++;
            }
            else {
                arr[k] = aux[i - l];
                i ++;
            }
        }
    }

}
