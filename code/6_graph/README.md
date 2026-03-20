# 408考研 · 图总结

> 本文档包含图的完整总结，涵盖图的存储结构、BFS/DFS 遍历、最小生成树、最短路径、拓扑排序和关键路径的算法思想、手写执行过程和 Python 实现。适合 408 考研数据结构复习使用。

---

## 📊 算法对比总览

| 算法 | 时间复杂度 | 适用场景 |
|------|-----------|---------|
| BFS | 邻接表 O(V+E) / 矩阵 O(V²) | 无权图最短路径、层次遍历 |
| DFS | 邻接表 O(V+E) / 矩阵 O(V²) | 连通性检测、拓扑排序 |
| Prim | O(V²) / O(E log V) | 稠密图最小生成树 |
| Kruskal | O(E log E) | 稀疏图最小生成树 |
| Dijkstra | O(V²) / O(E log V) | 单源最短路径（无负权） |
| Floyd | O(V³) | 多源最短路径 |
| 拓扑排序 | O(V+E) | DAG，判断有向图是否有环 |

---

## 1. 图的存储结构

### 邻接矩阵 vs 邻接表

| 特性 | 邻接矩阵 | 邻接表 |
|------|----------|--------|
| 空间 | O(V²) | O(V+E) |
| 适合 | 稠密图 | 稀疏图 |
| 判断边 | O(1) | O(度) |
| 求度 | O(V) | O(度) |
| 唯一性 | 唯一 | 不唯一（边的顺序可变） |

**手写邻接矩阵**（无向图）：

```
图结构:
  A --- B
  |     |
  C --- D

邻接矩阵:           邻接表:
    A  B  C  D       A → [B, C]
A [ 0  1  1  0 ]    B → [A, D]
B [ 1  0  0  1 ]    C → [A, D]
C [ 1  0  0  1 ]    D → [B, C]
D [ 0  1  1  0 ]

无向图特点: 邻接矩阵是对称阵
顶点 A 的度 = 第 A 行的非零元素个数 = 2
```

---

## 2. BFS (广度优先搜索)

**核心思想**：类似层次遍历，用**队列**实现。从起点出发，先访问所有邻居，再访问邻居的邻居。可求无权图最短路径。

**关键步骤**：
1. 起点入队，标记已访问
2. 队头出队，访问该节点
3. 将其**未访问**的邻居全部入队
4. 重复直到队空

**手写 BFS 过程**（从 A 开始）：

```
图:  A --- B --- D
     |     |     |
     C --- E --- F

步骤  出队  入队      队列状态
1     A     B,C       [B, C]
2     B     D,E       [C, D, E]
3     C     (E已访问) [D, E]
4     D     F         [E, F]
5     E     (F已访问) [F]
6     F     无        []

BFS 序列: A → B → C → D → E → F
```

**BFS 求最短路径**：

```
从 A 到各顶点的最短距离:
  A→A: 0     A→B: 1     A→C: 1
  A→D: 2     A→E: 2     A→F: 3
```

**Python 实现**：

```python
from collections import deque

def bfs(graph, start):
    """BFS 广度优先搜索"""
    visited = set([start])
    queue = deque([start])
    order = []
    while queue:
        v = queue.popleft()
        order.append(v)
        for neighbor in sorted(graph[v]):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order
```

---

## 3. DFS (深度优先搜索)

**核心思想**：类似先序遍历，用**递归/栈**实现。沿一条路走到底，无路可走时回溯。

**手写 DFS 过程**（从 A 开始）：

```
图:  A --- B --- D
     |     |     |
     C --- E --- F

访问 A
  → 递归进入 B
    → 递归进入 D
      → 递归进入 F
        → 递归进入 E
          → E的邻居 B,C,F 中 C 未访问
          → 递归进入 C
            → C的邻居都已访问, 回溯
          ← 回溯到 E
        ← 回溯到 F
      ← 回溯到 D
    ← 回溯到 B
  ← 回溯到 A

DFS 序列: A → B → D → F → E → C
```

**Python 实现**：

```python
def dfs(graph, start):
    """DFS 深度优先搜索 (递归)"""
    visited = set()
    order = []

    def _dfs(v):
        visited.add(v)
        order.append(v)
        for neighbor in sorted(graph[v]):
            if neighbor not in visited:
                _dfs(neighbor)

    _dfs(start)
    return order
```

---

## 4. 最小生成树 (MST)

### 4.1 Prim 算法

**核心思想**：从一个顶点出发，每次选择**连接已选集合和未选集合的最小权边**，加入新顶点。适合稠密图。

**手写 Prim 过程**：

```
图 (带权):
  A --2-- B --3-- D
  |       |       |
  3       4       5
  |       |       |
  C --1-- E --6-- F

从 A 开始:
步骤  已选集合      选择的边          加入顶点
1     {A}          A-B(2)最小        B
2     {A,B}        A-C(3)最小        C
3     {A,B,C}      C-E(1)最小        E
4     {A,B,C,E}    B-D(3)最小        D
5     {A,B,C,E,D}  D-F(5)最小        F

MST 边: A-B(2), A-C(3), C-E(1), B-D(3), D-F(5)
总权值 = 2 + 3 + 1 + 3 + 5 = 14
```

### 4.2 Kruskal 算法

**核心思想**：将所有边按权值排序，依次选择**最小的且不构成环**的边。用并查集判环。适合稀疏图。

**手写 Kruskal 过程**：

```
所有边排序: C-E(1), A-B(2), A-C(3), B-D(3), B-E(4), D-F(5), E-F(6)

步骤  选择边      是否成环   操作
1     C-E(1)     否 ✓       选入
2     A-B(2)     否 ✓       选入
3     A-C(3)     否 ✓       选入
4     B-D(3)     否 ✓       选入
5     B-E(4)     会成环 ✗   跳过 (A-B-E-C-A)
6     D-F(5)     否 ✓       选入
                             已选5条边 = V-1, 完成!

MST 边: C-E(1), A-B(2), A-C(3), B-D(3), D-F(5)
总权值 = 14 (与 Prim 结果相同)
```

**Python 实现**（Kruskal）：

```python
def kruskal(vertices, edges):
    """Kruskal 最小生成树"""
    edges.sort(key=lambda e: e[2])  # 按权值排序
    parent = {v: v for v in vertices}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    mst = []
    for u, v, w in edges:
        if find(u) != find(v):
            mst.append((u, v, w))
            parent[find(u)] = find(v)
    return mst
```

---

## 5. 最短路径

### 5.1 Dijkstra 算法

**核心思想**：贪心策略。维护 dist[] 数组，每次选择**未确定的最近顶点**，用它来松弛邻居的距离。不能处理负权边。

**手写 Dijkstra 过程**（从 A 出发）：

```
图:  A --1-- B --2-- D
     |       |       |
     4       3       1
     |       |       |
     C --5-- E --2-- F

初始 dist: A=0, B=∞, C=∞, D=∞, E=∞, F=∞

轮次  选中   更新后的 dist[]
1     A(0)   B=1, C=4
2     B(1)   D=3, E=4 (min(∞,1+3))
3     D(3)   F=4 (min(∞,3+1))
4     C(4)   E=4 (不变, C+5=9>4)
5     E(4)   F=4 (不变)
6     F(4)   完成

最短路径:
  A→A=0   A→B=1   A→C=4
  A→D=3   A→E=4   A→F=4
```

### 5.2 Floyd 算法

**核心思想**：动态规划。三重循环尝试每个中转点 k，更新 `dist[i][j] = min(dist[i][j], dist[i][k]+dist[k][j])`。

**手写 Floyd 过程**（3个顶点）：

```
初始距离矩阵:      以0为中转:        以1为中转:        以2为中转(最终):
    0   1   2         0   1   2         0   1   2         0   1   2
0 [ 0   3   ∞ ]   0 [ 0   3   ∞ ]   0 [ 0   3   6 ]   0 [ 0   3   6 ]
1 [ ∞   0   1 ]   1 [ ∞   0   1 ]   1 [ ∞   0   1 ]   1 [ 8   0   1 ]
2 [ 7   ∞   0 ]   2 [ 7  10   0 ]   2 [ 7  10   0 ]   2 [ 7  10   0 ]

dist[2][1] = min(∞, 7+3) = 10 (经过顶点0中转)
dist[0][2] = min(∞, 3+1) = 4→6→6 (经过顶点1中转: 0→1→2)
```

**Python 实现**（Dijkstra）：

```python
def dijkstra(graph, start, n):
    """Dijkstra 单源最短路径"""
    dist = [float('inf')] * n
    dist[start] = 0
    visited = [False] * n

    for _ in range(n):
        # 选未确定的最近顶点
        u = -1
        for v in range(n):
            if not visited[v] and (u == -1 or dist[v] < dist[u]):
                u = v
        visited[u] = True
        # 松弛邻居
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist
```

---

## 6. 拓扑排序与关键路径

### 6.1 拓扑排序

**核心思想**：每次选择**入度为0**的顶点输出，删除该顶点和所有出边。若输出顶点数 < 总顶点数，则图有环。

**手写拓扑排序过程**：

```
有向图:
  A → B → D
  A → C → D
  B → C

入度: A=0, B=1, C=2, D=2

步骤  选入度=0  删除出边            入度变化
1     A        删 A→B, A→C        B=0, C=1
2     B        删 B→C, B→D        C=0, D=1
3     C        删 C→D             D=0
4     D        无出边             完成

拓扑序列: A → B → C → D ✓ (输出4个=V, 无环)
```

### 6.2 关键路径

**核心思想**：AOE 网中，找**最长路径**（关键路径），决定工程最短完成时间。计算 ve/vl/e/l 四个数组，e(i)==l(i) 的活动为关键活动。

**手写关键路径**：

```
AOE 网:
  V0 --a1(3)-→ V1 --a3(2)-→ V3 --a5(3)-→ V5
  V0 --a2(2)-→ V2 --a4(4)-→ V3
               V2 --a6(3)-→ V4 --a7(2)-→ V5

ve(事件最早): V0=0, V1=3, V2=2, V3=6, V4=5, V5=9
vl(事件最迟): V5=9, V4=7, V3=6, V2=2, V1=4, V0=0

活动    e(最早)  l(最迟)  l-e   关键?
a1(3)   0        1        1     否
a2(2)   0        0        0     ✓ 关键
a3(2)   3        4        1     否
a4(4)   2        2        0     ✓ 关键
a5(3)   6        6        0     ✓ 关键
a6(3)   2        4        2     否
a7(2)   5        7        2     否

关键路径: V0→V2→V3→V5 (a2→a4→a5)
工程最短完成时间 = 2+4+3 = 9
```

---

## 🧠 考研重点速记

### 存储结构
- **邻接矩阵** O(V²) 适合稠密图，邻接表 O(V+E) 适合稀疏图
- 无向图邻接矩阵**对称**，第 i 行非零个数 = 顶点 i 的度
- 有向图：第 i 行 = 出度，第 j 列 = 入度

### 遍历
- **BFS**: 用队列，层层推进，可求无权图最短路径
- **DFS**: 用递归/栈，一条路走到黑再回溯
- 遍历序列与邻接表中邻居顺序有关

### 最小生成树
- **Prim**: 从顶点扩展（稠密图）；**Kruskal**: 从最小边选（稀疏图）
- n 个顶点的 MST 有 **n-1** 条边

### 最短路径
- **Dijkstra**: 贪心，不能负权，O(V²)
- **Floyd**: DP 三重循环，O(V³)，可处理负权（无负环）

### 拓扑排序
- 每次选入度为 0 的顶点
- 输出数 < V → 有环

### 关键路径
- ve/vl/e/l 四个数组，**e(i)==l(i)** 的是关键活动

---

## 📁 文件结构

```
6_graph/
├── README.md                    # 本文档
├── 6_2_graph_storage.py         # 图的存储结构
├── 6_3_bfs_dfs.py               # BFS和DFS遍历
├── 6_4_mst.py                   # 最小生成树
├── 6_4_shortest_path.py         # 最短路径
└── 6_4_topo_critical_path.py    # 拓扑排序与关键路径
```

每个 Python 文件包含：
- 📝 算法说明文档字符串
- ⚡ 标准实现函数
- 🔍 带详细输出的 verbose 版本
- ✍️ 手写过程模拟
- ✅ 测试用例

运行示例：
```bash
python 6_graph/6_2_graph_storage.py
python 6_graph/6_3_bfs_dfs.py
python 6_graph/6_4_mst.py
python 6_graph/6_4_shortest_path.py
python 6_graph/6_4_topo_critical_path.py
```
