"""
0/1背包问题
"""

# 背包的容量 capacity
capacity = 4

# 商品的重量和价值
goods = ["音响", "吉他", "笔记本"]
weights = [4, 1, 3]
values = [3000, 1500, 2000]

# 商品的种类数 types
types = len(goods)


def dynamicPlan():
    cell = [[0 for j in range(capacity + 1)] for i in range(types + 1)]
    for i in range(1, types + 1):
        for j in range(1, capacity + 1):
            cell[i][j] = cell[i - 1][j]
            if j >= weights[i - 1] and values[i - 1] + cell[i - 1][j - weights[i - 1]] > cell[i][
                j]:  # 放得下当前商品，max{当前商品的价值+剩余容量的价值 , 上一个单元格的值}
                cell[i][j] = values[i - 1] + cell[i - 1][j - weights[i - 1]]
    #	显示网格
    for i in range(types + 1):
        print(cell[i])
    return cell


def pathTrace(cell):
    processed = [False for i in range(types)]
    cap = capacity
    for i in range(types, 0, -1):
        if cell[i][cap] != cell[i - 1][cap]:  # 从右上角向左下角遍历
            processed[i - 1] = True
            cap -= weights[i - 1]
    print(processed)
    print("You choose goods:", end='')
    for i in range(1, types + 1):
        if processed[i - 1]:
            print("%s, " % goods[i - 1], end='')
    print()


if __name__ == "__main__":
    pathTrace(dynamicPlan())