"""
并查集 (Union-Find / Disjoint Set)

核心思想: 用森林表示多个不相交的集合
  - 每棵树代表一个集合
  - 树根是集合的代表元素
  - 用数组实现: parent[i] = i 的父节点, 根的 parent 为 -1 或自身

两个基本操作:
  Find(x):  找 x 所属集合的根节点
  Union(x, y): 合并 x 和 y 所在的集合

优化:
  1. 按秩合并 (Union by rank): 矮树挂到高树下
  2. 路径压缩 (Path compression): Find 时将经过的节点直接挂到根

时间复杂度:
  - 基础版: O(n) 最坏
  - 按秩合并: O(log n)
  - 路径压缩: 近似 O(α(n)) ≈ O(1)  (α 是阿克曼函数的反函数)
"""


class UnionFind:
    """并查集基础版"""

    def __init__(self, n):
        self.parent = list(range(n))  # 每个元素的父节点
        self.n = n

    def find(self, x):
        """Find: 找根节点"""
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def union(self, x, y):
        """Union: 合并两个集合"""
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.parent[rx] = ry  # 把 rx 挂到 ry 下
            return True
        return False  # 已在同一集合

    def connected(self, x, y):
        """判断 x 和 y 是否在同一集合"""
        return self.find(x) == self.find(y)

    def display(self):
        print(f"  parent: {self.parent}")
        sets = {}
        for i in range(self.n):
            root = self.find(i)
            if root not in sets:
                sets[root] = []
            sets[root].append(i)
        for root, members in sets.items():
            print(f"    集合(根={root}): {members}")


class UnionFindOptimized:
    """并查集优化版 (按秩合并 + 路径压缩)"""

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n  # 秩 (树高的上界)
        self.n = n

    def find(self, x):
        """Find + 路径压缩

        将路径上所有节点直接挂到根
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 递归压缩
        return self.parent[x]

    def union(self, x, y):
        """Union + 按秩合并

        矮树挂到高树下, 保持树的平衡
        """
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        # 按秩合并
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1  # 等高时，合并后高度+1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)

    def count_sets(self):
        """计算集合个数"""
        roots = set()
        for i in range(self.n):
            roots.add(self.find(i))
        return len(roots)


def basic_demo():
    """基础并查集演示"""
    print("=" * 60)
    print("并查集基本操作")
    print("=" * 60)

    uf = UnionFind(7)
    print(f"\n  初始: 7 个独立元素 (0~6)")
    uf.display()

    operations = [
        (0, 1), (2, 3), (4, 5),  # 第一轮合并
        (1, 2), (3, 5),          # 第二轮合并
    ]

    for x, y in operations:
        print(f"\n  Union({x}, {y}):")
        uf.union(x, y)
        uf.display()

    print(f"\n  查询:")
    for x, y in [(0, 5), (0, 6), (3, 4)]:
        print(f"  Connected({x}, {y}) = {uf.connected(x, y)}")
    print()


def optimized_demo():
    """优化版并查集演示"""
    print("=" * 60)
    print("优化版并查集 (按秩合并 + 路径压缩)")
    print("=" * 60)

    uf = UnionFindOptimized(8)

    # 构造一条链: 0-1-2-3-4-5-6-7
    print(f"\n  依次合并: 0-1, 2-3, 4-5, 6-7, 0-2, 4-6, 0-4")
    for x, y in [(0, 1), (2, 3), (4, 5), (6, 7), (0, 2), (4, 6), (0, 4)]:
        uf.union(x, y)

    print(f"  parent: {uf.parent}")
    print(f"  rank:   {uf.rank}")
    print(f"  集合数: {uf.count_sets()}")

    # 路径压缩
    print(f"\n  Find(7) 触发路径压缩:")
    print(f"  压缩前 parent: {uf.parent}")
    uf.find(7)
    print(f"  压缩后 parent: {uf.parent}")
    print(f"  → 7 直接挂到根节点下!")
    print()


def application_demo():
    """应用: 判断图的连通分量"""
    print("=" * 60)
    print("应用: 判断图的连通分量")
    print("=" * 60)

    n = 6
    edges = [(0, 1), (1, 2), (3, 4)]

    uf = UnionFindOptimized(n)
    for u, v in edges:
        uf.union(u, v)

    print(f"\n  {n} 个顶点, 边: {edges}")
    print(f"  连通分量数: {uf.count_sets()}")

    # 显示各连通分量
    sets = {}
    for i in range(n):
        root = uf.find(i)
        if root not in sets:
            sets[root] = []
        sets[root].append(i)
    for root, members in sets.items():
        print(f"  分量: {members}")
    print()


if __name__ == "__main__":
    basic_demo()
    optimized_demo()
    application_demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 并查集 = 不相交集合的合并与查询
     Find(x): 找根
     Union(x,y): 合并

  2. 优化策略:
     按秩合并: 矮树挂高树, 保证树高 O(log n)
     路径压缩: Find 时将节点直接挂到根

  3. 时间复杂度:
     基础: O(n)
     按秩合并: O(log n)
     按秩合并 + 路径压缩: O(α(n)) ≈ O(1)

  4. 应用场景:
     - 连通分量判断
     - Kruskal 最小生成树
     - 等价类划分
    """)
