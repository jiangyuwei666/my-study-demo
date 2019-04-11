class DenseGraph:
    """
    稠密图 - 邻接矩阵
    """
    n = None  # 点熟
    m = None  # 边数
    directed = None  # 有向图或者是无向图

    def __init__(self, n, directed):
        self.n = n
        self.m = 0
        self.directed = directed
        self.g = [[False] * self.n] * self.n

    def v(self):
        return self.n

    def e(self):
        return self.m

    def add_edge(self, p1, p2):
        assert p1 >= 0
        assert p1 < self.n
        assert p2 >= 0
        assert p2 < self.n

        if self.has_edge(p1, p2):
            return

        self.g[p1][p2] = True
        if not self.directed:
            # 如果不是有向图，是无向图（也就是双向图）
            self.g[p1][p2] = True

        # 边数+1
        self.m += 1

    def has_edge(self, p1, p2):
        """
        判断两个点是否有边
        """
        assert p1 >= 0
        assert p1 < self.n
        assert p2 >= 0
        assert p2 < self.n
        return self.g[p1][p2]