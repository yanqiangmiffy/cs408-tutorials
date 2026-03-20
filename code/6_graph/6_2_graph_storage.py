"""
图的存储结构

1. 邻接矩阵 (Adjacency Matrix):
   - 用二维数组表示, A[i][j] 表示边 (i,j) 的权值
   - 适合稠密图, 空间 O(V²)
   - 查找边 O(1), 遍历邻居 O(V)

2. 邻接表 (Adjacency List):
   - 对每个顶点维护一个边链表
   - 适合稀疏图, 空间 O(V+E)
   - 遍历邻居 O(度), 查找边 O(度)

考研要点:
  - 邻接矩阵: 无向图对称, 有向图不一定对称
  - 邻接表: 无向图每条边存两次
  - 度的计算: 邻接矩阵按行/列求和
"""


# ==========================================
# 1. 邻接矩阵
# ==========================================

class GraphMatrix:
    """邻接矩阵表示的图"""

    INF = float('inf')

    def __init__(self, vertices, directed=False):
        self.vertices = vertices
        self.n = len(vertices)
        self.directed = directed
        self.v_index = {v: i for i, v in enumerate(vertices)}
        self.matrix = [[self.INF] * self.n for _ in range(self.n)]
        # 对角线为 0
        for i in range(self.n):
            self.matrix[i][i] = 0

    def add_edge(self, u, v, weight=1):
        i, j = self.v_index[u], self.v_index[v]
        self.matrix[i][j] = weight
        if not self.directed:
            self.matrix[j][i] = weight

    def has_edge(self, u, v):
        i, j = self.v_index[u], self.v_index[v]
        return self.matrix[i][j] != self.INF and self.matrix[i][j] != 0

    def get_neighbors(self, u):
        i = self.v_index[u]
        neighbors = []
        for j in range(self.n):
            if self.matrix[i][j] != self.INF and self.matrix[i][j] != 0:
                neighbors.append((self.vertices[j], self.matrix[i][j]))
        return neighbors

    def degree(self, u):
        """求顶点的度"""
        i = self.v_index[u]
        if self.directed:
            out_deg = sum(1 for j in range(self.n) if self.matrix[i][j] not in (0, self.INF))
            in_deg = sum(1 for j in range(self.n) if self.matrix[j][i] not in (0, self.INF))
            return in_deg, out_deg
        else:
            return sum(1 for j in range(self.n) if self.matrix[i][j] not in (0, self.INF))

    def display(self):
        print(f"  {'':>4s}", end="")
        for v in self.vertices:
            print(f"{v:>5s}", end="")
        print()
        for i, v in enumerate(self.vertices):
            print(f"  {v:>4s}", end="")
            for j in range(self.n):
                val = self.matrix[i][j]
                if val == self.INF:
                    print(f"{'∞':>5s}", end="")
                else:
                    print(f"{val:>5g}", end="")
            print()


# ==========================================
# 2. 邻接表
# ==========================================

class GraphAdjList:
    """邻接表表示的图"""

    def __init__(self, vertices, directed=False):
        self.vertices = vertices
        self.directed = directed
        self.adj = {v: [] for v in vertices}

    def add_edge(self, u, v, weight=1):
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def has_edge(self, u, v):
        return any(neighbor == v for neighbor, _ in self.adj[u])

    def get_neighbors(self, u):
        return self.adj[u]

    def degree(self, u):
        if self.directed:
            out_deg = len(self.adj[u])
            in_deg = sum(1 for v in self.vertices for n, _ in self.adj[v] if n == u)
            return in_deg, out_deg
        return len(self.adj[u])

    def display(self):
        for v in self.vertices:
            neighbors = [f"{n}({w})" for n, w in self.adj[v]]
            print(f"  {v} → {', '.join(neighbors) if neighbors else '(无)'}")


def demo():
    """图的存储演示"""
    print("=" * 60)
    print("图的存储结构")
    print("=" * 60)

    vertices = ['A', 'B', 'C', 'D', 'E']
    edges = [('A', 'B', 1), ('A', 'C', 1), ('B', 'C', 1),
             ('B', 'D', 1), ('C', 'E', 1), ('D', 'E', 1)]

    # 邻接矩阵
    print(f"\n  --- 无向图 · 邻接矩阵 ---")
    gm = GraphMatrix(vertices)
    for u, v, w in edges:
        gm.add_edge(u, v, w)
    gm.display()
    for v in vertices:
        print(f"  度({v}) = {gm.degree(v)}")

    # 邻接表
    print(f"\n  --- 无向图 · 邻接表 ---")
    gl = GraphAdjList(vertices)
    for u, v, w in edges:
        gl.add_edge(u, v, w)
    gl.display()

    # 有向图
    print(f"\n  --- 有向图 · 邻接矩阵 ---")
    dg = GraphMatrix(vertices, directed=True)
    for u, v, w in edges:
        dg.add_edge(u, v, w)
    dg.display()
    for v in vertices:
        in_d, out_d = dg.degree(v)
        print(f"  {v}: 入度={in_d}, 出度={out_d}")

    print()


if __name__ == "__main__":
    demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 邻接矩阵:
     空间: O(V²), 适合稠密图
     无向图: 对称矩阵, 可压缩存储
     度: 第 i 行(列)非零/非∞元素个数

  2. 邻接表:
     空间: O(V+E), 适合稀疏图
     无向图: 每条边存两次, 边数=链表节点总数/2

  3. 邻接矩阵 vs 邻接表:
     判断边是否存在: 矩阵 O(1), 表 O(度)
     遍历所有邻居: 矩阵 O(V), 表 O(度)
     空间: 矩阵 O(V²), 表 O(V+E)

  4. 十字链表 (有向图), 邻接多重表 (无向图):
     了解概念即可, 较少考代码
    """)
