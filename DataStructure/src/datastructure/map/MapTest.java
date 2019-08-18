package datastructure.map;

/**
 * Created By Jiangyuwei on 2019/7/23 10:53
 * Description:
 */
public class MapTest {

    public static void main(String[] args) {
        Map<String, Integer> map = new Map<>();
        map.add("asd", 1);
        map.add("qwe", 2);
        map.add("jyw", 3);
        map.add("jwy", 4);
        System.out.println(map.contains("asd"));
        System.out.println(map.contains("asqw"));
        System.out.println(map.get("qwe"));
        map.set("qwe", 99);
        System.out.println(map.get("qwe"));
    }

}
