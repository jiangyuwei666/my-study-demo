package datastructure.hash;

import java.util.TreeMap;

/**
 * Created By Jiangyuwei on 2019/7/31 19:56
 * Description:
 */
public class HashTable<K, V> {

    private TreeMap<K, V> [] hashTable;
    private int M;
    private int size;

    public HashTable(int M){
        this.M = M;
        this.size  = 0;
        this.hashTable = new TreeMap[M];
        for (int i = 0; i < M; i ++){
            this.hashTable[i] = new TreeMap<>();
        }
    }

    public HashTable(){
        this(97);
    }

    private int hash(K key){
        // 得到一个证书并对其取正
        return (key.hashCode() & 0x7fffffff) % M;
    }

    public void add(K key, V value){
        TreeMap<K, V> map = hashTable[hash(key)]; // 获取当前数组的这个位置的映射
        // 判断是否在里面
        if (!map.containsKey(key)){
            map.put(key, value);
            size ++;
        }

    }

}
