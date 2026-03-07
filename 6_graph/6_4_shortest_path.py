"""
最短路径算法

1. BFS (无权图): O(V+E)
2. Dijkstra (非负权图): O(V²) 或 O(E log V)
3. Floyd (任意图, 无负环): O(V³)

考研要点:
  - Dijkstra 手写过程 (每步更新 dist 数组)
  - Floyd 手写过程 (逐步更新矩阵)
  - Dijkstra 不能处理负权边!
  - Floyd 可以检测负权环
"""

import heapq
from collections import deque


# ==========================================
# 1. BFS 最短路径 (无权图)
# ==========================================

def bfs_shortest(adj, start, vertices):
    """BFS 求无权图最短路径"""
    dist = {v: float('inf') for v in vertices}
    prev = {v: None for v in vertices}
    dist[start] = 0
    queue = deque([start])

    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] == float('inf'):
                dist[v] = dist[u] + 1
                prev[v] = u
                queue.append(v)
    return dist, prev


# ==========================================
# 2. Dijkstra 算法
# ==========================================

def dijkstra(vertices, edges, start):
    """Dijkstra 最短路径算法

    思路:
    1. 初始: dist[start]=0, 其余为 ∞
    2. 每次选择 dist 最小的未确定顶点 u
    3. 用 u 更新所有邻居: dist[v] = min(dist[v], dist[u] + w(u,v))
    4. u 标记为已确定
    5. 重复 V 次

    注意: 不能处理负权边!
    """
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))

    dist = {v: float('inf') for v in vertices}
    prev = {v: None for v in vertices}
    dist[start] = 0
    visited = set()

    print(f"  Dijkstra 从 {start} 出发:")
    print(f"  {'步骤':>4s} {'选择':>4s}", end="")
    for v in vertices:
        print(f"  {v:>5s}", end="")
    print()
    print(f"  {'─' * (10 + 7 * len(vertices))}")

    # 初始状态
    print(f"  {'初始':>4s} {'':>4s}", end="")
    for v in vertices:
        d = dist[v]
        print(f"  {d if d != float('inf') else '∞':>5}", end="")
    print()

    for step in range(len(vertices)):
        # 找最小未访问顶点
        u = None
        for v in vertices:
            if v not in visited:
                if u is None or dist[v] < dist[u]:
                    u = v
        if u is None or dist[u] == float('inf'):
            break

        visited.add(u)

        # 松弛操作
        for v, w in adj[u]:
            if v not in visited and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u

        print(f"  {step + 1:>4d} {u:>4s}", end="")
        for v in vertices:
            d = dist[v]
            mark = "*" if v in visited else " "
            print(f" {mark}{d if d != float('inf') else '∞':>4}", end="")
        print()

    return dist, prev


def dijkstra_heap(vertices, edges, start):
    """Dijkstra (堆优化版) O(E log V)"""
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))

    dist = {v: float('inf') for v in vertices}
    prev = {v: None for v in vertices}
    dist[start] = 0
    heap = [(0, start)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))

    return dist, prev


# ==========================================
# 3. Floyd 算法
# ==========================================

def floyd(vertices, edges):
    """Floyd 最短路径算法 (多源)

    思路 (动态规划):
    dp[k][i][j] = 从 i 到 j, 中间只经过前 k 个顶点的最短路径
    dp[k][i][j] = min(dp[k-1][i][j], dp[k-1][i][k] + dp[k-1][k][j])

    空间优化: 原地更新矩阵
    """
    n = len(vertices)
    v_index = {v: i for i, v in enumerate(vertices)}
    INF = float('inf')

    # 初始化距离矩阵
    dist = [[INF] * n for _ in range(n)]
    path = [[None] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0

    for u, v, w in edges:
        i, j = v_index[u], v_index[v]
        dist[i][j] = w
        path[i][j] = i

    print(f"  Floyd 算法:")
    print(f"\n  初始距离矩阵:")
    _print_matrix(vertices, dist)

    # Floyd 核心: 三重循环
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    path[i][j] = path[k][j]

        print(f"\n  经过 {vertices[k]} 后:")
        _print_matrix(vertices, dist)

    return dist, path, v_index


def _print_matrix(vertices, dist):
    print(f"  {'':>4s}", end="")
    for v in vertices:
        print(f"{v:>5s}", end="")
    print()
    for i, v in enumerate(vertices):
        print(f"  {v:>4s}", end="")
        for j in range(len(vertices)):
            d = dist[i][j]
            print(f"{d if d != float('inf') else '∞':>5}", end="")
        print()


def get_path(prev, start, end):
    """还原路径"""
    if prev[end] is None and start != end:
        return []
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path


def demo():
    """最短路径演示"""
    print("=" * 60)
    print("最短路径算法")
    print("=" * 60)

    vertices = ['A', 'B', 'C', 'D', 'E']
    edges = [
        ('A', 'B', 10), ('A', 'D', 5),
        ('B', 'C', 1), ('B', 'D', 2),
        ('C', 'E', 4),
        ('D', 'B', 3), ('D', 'C', 9), ('D', 'E', 2),
        ('E', 'A', 7), ('E', 'C', 6),
    ]

    print(f"\n  有向带权图: {len(vertices)}个顶点, {len(edges)}条边")
    for u, v, w in edges:
        print(f"    {u} → {v}: {w}")

    # Dijkstra
    print(f"\n{'═' * 60}")
    dist, prev = dijkstra(vertices, edges, 'A')
    print(f"\n  Dijkstra 最短距离:")
    for v in vertices:
        path = get_path(prev, 'A', v)
        print(f"  A → {v}: dist={dist[v]}, path={'→'.join(path)}")

    # Floyd
    print(f"\n{'═' * 60}")
    f_dist, f_path, v_idx = floyd(vertices, edges)
    print(f"\n  Floyd 最终距离矩阵:")
    _print_matrix(vertices, f_dist)

    print()


if __name__ == "__main__":
    demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. Dijkstra:
     单源最短路径, 贪心策略
     时间: O(V²) 朴素,  O(E log V) 堆优化
     限制: 不能处理负权边!

  2. Floyd:
     多源最短路径, 动态规划
     时间: O(V³), 空间: O(V²)
     可以处理负权边 (但不能有负环)
     核心: dist[i][j] = min(dist[i][j], dist[i][k]+dist[k][j])

  3. BFS:
     无权图最短路径, O(V+E)

  4. 选择依据:
     无权图 → BFS
     单源非负权 → Dijkstra
     多源/负权 → Floyd
    """)
