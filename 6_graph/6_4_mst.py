"""
最小生成树 (Minimum Spanning Tree)

1. Prim 算法:
   - 从某顶点开始, 每次选择连接已选和未选顶点的最小边
   - 适合稠密图, 时间 O(V²)

2. Kruskal 算法:
   - 将边按权值排序, 每次选最小边且不构成环 (用并查集)
   - 适合稀疏图, 时间 O(E log E)

考研要点:
  - 手写 Prim/Kruskal 的执行过程
  - 两种算法的适用场景
  - MST 的性质: V-1 条边, 权值和最小
"""

import heapq


class UnionFind:
    """并查集 (Kruskal 算法用)"""
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True


def prim(vertices, edges):
    """Prim 算法求最小生成树

    思路 (贪心):
    1. 从任意顶点开始, 加入已选集合
    2. 每次从「已选 ↔ 未选」的边中选最小的
    3. 将新顶点加入已选, 重复直到所有顶点都选入
    """
    n = len(vertices)
    v_index = {v: i for i, v in enumerate(vertices)}

    # 邻接表
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    # 从第一个顶点开始
    start = vertices[0]
    in_mst = {start}
    mst_edges = []
    total_weight = 0

    # 最小堆: (权值, 起点, 终点)
    heap = []
    for neighbor, weight in adj[start]:
        heapq.heappush(heap, (weight, start, neighbor))

    print(f"  Prim 算法执行过程:")
    print(f"  起始顶点: {start}")
    step = 0

    while heap and len(in_mst) < n:
        weight, u, v = heapq.heappop(heap)
        if v in in_mst:
            continue
        step += 1
        in_mst.add(v)
        mst_edges.append((u, v, weight))
        total_weight += weight
        print(f"  步骤{step}: 选边 ({u},{v}) 权={weight}, 已选顶点={in_mst}")

        for neighbor, w in adj[v]:
            if neighbor not in in_mst:
                heapq.heappush(heap, (w, v, neighbor))

    return mst_edges, total_weight


def kruskal(vertices, edges):
    """Kruskal 算法求最小生成树

    思路 (贪心):
    1. 将所有边按权值排序
    2. 依次取最小边, 若不构成环 (并查集判断) 则加入 MST
    3. 选够 V-1 条边即完成
    """
    n = len(vertices)
    v_index = {v: i for i, v in enumerate(vertices)}

    # 按权值排序
    sorted_edges = sorted(edges, key=lambda x: x[2])
    uf = UnionFind(n)

    mst_edges = []
    total_weight = 0

    print(f"\n  Kruskal 算法执行过程:")
    print(f"  按权值排序: {[(u, v, w) for u, v, w in sorted_edges]}")
    step = 0

    for u, v, w in sorted_edges:
        ui, vi = v_index[u], v_index[v]
        if uf.union(ui, vi):
            step += 1
            mst_edges.append((u, v, w))
            total_weight += w
            print(f"  步骤{step}: 选边 ({u},{v}) 权={w} ✓")
            if len(mst_edges) == n - 1:
                break
        else:
            print(f"  跳过: 边 ({u},{v}) 权={w} 会形成环 ✗")

    return mst_edges, total_weight


def demo():
    """最小生成树演示"""
    print("=" * 60)
    print("最小生成树")
    print("=" * 60)

    vertices = ['A', 'B', 'C', 'D', 'E', 'F']
    edges = [
        ('A', 'B', 6), ('A', 'C', 1), ('A', 'D', 5),
        ('B', 'C', 5), ('B', 'E', 3),
        ('C', 'D', 5), ('C', 'E', 6), ('C', 'F', 4),
        ('D', 'F', 2),
        ('E', 'F', 6),
    ]

    print(f"\n  图: {len(vertices)}个顶点, {len(edges)}条边")
    for u, v, w in edges:
        print(f"    ({u},{v}) = {w}")

    # Prim
    print()
    prim_edges, prim_weight = prim(vertices, edges)
    print(f"\n  Prim MST: {prim_edges}")
    print(f"  总权值: {prim_weight}")

    # Kruskal
    print()
    kruskal_edges, kruskal_weight = kruskal(vertices, edges)
    print(f"\n  Kruskal MST: {kruskal_edges}")
    print(f"  总权值: {kruskal_weight}")
    print()


if __name__ == "__main__":
    demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. Prim 算法:
     从顶点出发, 逐步扩展
     每次选「已选↔未选」最小边
     时间: O(V²) 或 O(E log V) (用堆)
     适合: 稠密图 (边多)

  2. Kruskal 算法:
     从边出发, 排序后逐步选
     用并查集判断是否形成环
     时间: O(E log E)
     适合: 稀疏图 (边少)

  3. MST 性质:
     - 恰好 V-1 条边
     - 权值和最小
     - MST 不唯一 (权值相同的边)
     - 但 MST 的权值和唯一
    """)
