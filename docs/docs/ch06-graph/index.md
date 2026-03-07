# 第6章 图

> **考研要点速记**：图的存储结构有邻接矩阵(适合稠密图)和邻接表(适合稀疏图)；Dijkstra求单源最短路，Floyd求全源最短路；Kruskal配合并查集求最小生成树。

## 1. 图的存储 <a id="storage"></a>

### 邻接矩阵

邻接矩阵用二维数组存储，适合稠密图（边数接近n²）。

```python
class GraphMatrix:
    def __init__(self, n: int, directed=False):
        self.n = n              # 顶点数
        self.directed = directed
        self.matrix = [[float('inf')] * n for _ in range(n)]

        # 对角线设为0
        for i in range(n):
            self.matrix[i][i] = 0

    def add_edge(self, u: int, v: int, weight=1) -> None:
        """添加边"""
        self.matrix[u][v] = weight
        if not self.directed:
            self.matrix[v][u] = weight

    def get_neighbors(self, u: int) -> list:
        """获取顶点u的邻居"""
        neighbors = []
        for v in range(self.n):
            if self.matrix[u][v] != float('inf') and u != v:
                neighbors.append(v)
        return neighbors
```

### 邻接表

邻接表用链表/数组存储，适合稀疏图（边数远小于n²）。

```python
class GraphAdjList:
    def __init__(self, n: int, directed=False):
        self.n = n
        self.directed = directed
        self.adj_list = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, weight=1) -> None:
        """添加边"""
        self.adj_list[u].append((v, weight))
        if not self.directed:
            self.adj_list[v].append((u, weight))

    def get_neighbors(self, u: int) -> list:
        """获取顶点u的邻居"""
        return [v for v, _ in self.adj_list[u]]
```

## 2. BFS / DFS <a id="traversal"></a>

### 广度优先搜索（BFS）

BFS按层遍历图，使用队列实现，可求最短路径（无权图）。

```python
from collections import deque

def bfs(graph: GraphAdjList, start: int, visited=None) -> list:
    """广度优先搜索，返回遍历序列"""
    if visited is None:
        visited = set()

    result = []
    queue = deque([start])
    visited.add(start)

    while queue:
        u = queue.popleft()
        result.append(u)

        for v, _ in graph.adj_list[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)

    return result
```

### 深度优先搜索（DFS）

DFS一条路走到黑，用递归或栈实现。

```python
def dfs_recursive(graph: GraphAdjList, u: int, visited=None, result=None) -> list:
    """深度优先搜索（递归）"""
    if visited is None:
        visited = set()
    if result is None:
        result = []

    visited.add(u)
    result.append(u)

    for v, _ in graph.adj_list[u]:
        if v not in visited:
            dfs_recursive(graph, v, visited, result)

    return result

def dfs_iterative(graph: GraphAdjList, start: int) -> list:
    """深度优先搜索（非递归）"""
    visited = set()
    result = []
    stack = [start]

    while stack:
        u = stack.pop()
        if u not in visited:
            visited.add(u)
            result.append(u)
            # 逆序入栈，保证正确顺序
            for v, _ in reversed(graph.adj_list[u]):
                if v not in visited:
                    stack.append(v)

    return result
```

## 3. 最小生成树 <a id="mst"></a>

### Prim算法

Prim算法从任意顶点开始，每次选择与当前生成树相连的最小边，适合稠密图，时间复杂度O(V²)。

```python
import heapq

def prim(graph: GraphMatrix) -> tuple:
    """
    Prim算法求最小生成树
    返回：(总权重, 边列表)
    """
    n = graph.n
    visited = [False] * n
    min_dist = [float('inf')] * n
    parent = [-1] * n

    # 从顶点0开始
    min_dist[0] = 0
    total_weight = 0
    edges = []

    for _ in range(n):
        # 选择未被访问的最近顶点
        u = -1
        min_d = float('inf')
        for i in range(n):
            if not visited[i] and min_dist[i] < min_d:
                min_d = min_dist[i]
                u = i

        if u == -1:
            break

        visited[u] = True
        total_weight += min_dist[u]

        if parent[u] != -1:
            edges.append((parent[u], u, min_dist[u]))

        # 更新邻接顶点的距离
        for v in range(n):
            weight = graph.matrix[u][v]
            if not visited[v] and weight < min_dist[v]:
                min_dist[v] = weight
                parent[v] = u

    return total_weight, edges
```

### Kruskal算法

Kruskal算法按边权值从小到大排序，依次选择不形成环的边，适合稀疏图，需要并查集，时间复杂度O(ElogE)。

```python
def kruskal(graph: GraphMatrix) -> tuple:
    """
    Kruskal算法求最小生成树
    返回：(总权重, 边列表)
    """
    n = graph.n

    # 收集所有边
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if graph.matrix[i][j] != float('inf'):
                edges.append((graph.matrix[i][j], i, j))

    # 按权值排序
    edges.sort()

    uf = UnionFind(n)
    total_weight = 0
    mst_edges = []

    for weight, u, v in edges:
        if not uf.connected(u, v):
            uf.union(u, v)
            total_weight += weight
            mst_edges.append((u, v, weight))

    return total_weight, mst_edges
```

## 4. 最短路径 <a id="shortest-path"></a>

### Dijkstra算法

Dijkstra算法求单源最短路，不适用于含负权边的图，时间复杂度O(V²)，用堆优化可达O(ElogV)。

```python
def dijkstra(graph: GraphMatrix, start: int) -> tuple:
    """
    Dijkstra算法求单源最短路
    返回：(dist数组, path数组)
    """
    n = graph.n
    visited = [False] * n
    dist = [float('inf')] * n
    path = [-1] * n

    dist[start] = 0

    for _ in range(n):
        # 选择未访问的最近顶点
        u = -1
        min_d = float('inf')
        for i in range(n):
            if not visited[i] and dist[i] < min_d:
                min_d = dist[i]
                u = i

        if u == -1 or dist[u] == float('inf'):
            break

        visited[u] = True

        # 松弛操作
        for v in range(n):
            weight = graph.matrix[u][v]
            if not visited[v] and weight != float('inf'):
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    path[v] = u

    return dist, path
```

### Floyd算法

Floyd算法求全源最短路，可以处理含负权边的图（不含负权回路），时间复杂度O(V³)。

```python
def floyd(graph: GraphMatrix) -> tuple:
    """
    Floyd算法求全源最短路
    返回：(dist矩阵, path矩阵)
    """
    n = graph.n
    dist = [row[:] for row in graph.matrix]
    path = [[-1] * n for _ in range(n)]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    path[i][j] = k

    return dist, path
```

## 5. 拓扑排序 & 关键路径 <a id="topo"></a>

### 拓扑排序（Kahn算法）

对有向无环图(DAG)进行拓扑排序，用BFS思想实现，可检测环。

```python
from collections import deque

def topological_sort(graph: GraphAdjList) -> list:
    """Kahn算法拓扑排序，返回排序序列，有环返回空"""
    n = graph.n

    # 计算入度
    in_degree = [0] * n
    for u in range(n):
        for v, _ in graph.adj_list[u]:
            in_degree[v] += 1

    # 入度为0的顶点入队
    queue = deque([u for u in range(n) if in_degree[u] == 0])
    result = []

    while queue:
        u = queue.popleft()
        result.append(u)

        for v, _ in graph.adj_list[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    # 结果包含所有顶点则无环
    return result if len(result) == n else []
```

### 关键路径

关键路径是AOE网中从源点到汇点的最长路径，关键活动是关键路径上的活动。

```python
def critical_path(graph: GraphMatrix) -> tuple:
    """计算关键路径，返回(最早开始, 最晚开始, 关键活动)"""
    n = graph.n

    # 前向推进求最早开始时间ve
    ve = [0] * n
    # 先做拓扑排序确定计算顺序
    topo = topological_sort(GraphAdjList(n))
    if not topo:
        return None  # 有环

    for u in topo:
        for v in range(n):
            if graph.matrix[u][v] != float('inf'):
                ve[v] = max(ve[v], ve[u] + graph.matrix[u][v])

    # 后向回溯求最晚开始时间vl
    vl = [ve[n-1]] * n
    for u in reversed(topo):
        for v in range(n):
            if graph.matrix[u][v] != float('inf'):
                vl[u] = min(vl[u], vl[v] - graph.matrix[u][v])

    # 计算关键活动（最早开始=最晚开始）
    critical = []
    for u in range(n):
        for v in range(n):
            if graph.matrix[u][v] != float('inf'):
                e = ve[u]  # 最早开始
                l = vl[v] - graph.matrix[u][v]  # 最晚开始
                if e == l:
                    critical.append((u, v, e))

    return ve, vl, critical
```

## 考研重点 & 易错点

- ⚠️ 易错点：Dijkstra算法不能处理负权边，Floyd可以
- 📌 高频考点：Prim和Kruskal的区别与应用场景
- ⚠️ 易错点：拓扑排序只能用于DAG，有环图无法进行拓扑排序
- 📌 高频考点：关键活动的判断条件：最早开始时间=最晚开始时间
- 📌 高频考点：BFS求无权图最短路，Dijkstra求带权图最短路

## 复杂度总结表

| 算法 | 时间复杂度 | 空间复杂度 |
|------|-----------|-----------|
| 邻接矩阵存储 | O(V²) | O(V²) |
| 邻接表存储 | O(V+E) | O(V+E) |
| BFS/DFS | O(V+E) | O(V) |
| Prim算法 | O(V²) | O(V) |
| Prim(堆优化) | O(ElogV) | O(V) |
| Kruskal算法 | O(ElogE) | O(V) |
| Dijkstra算法 | O(V²) | O(V) |
| Dijkstra(堆优化) | O(ElogV) | O(V) |
| Floyd算法 | O(V³) | O(V²) |
| 拓扑排序 | O(V+E) | O(V) |
