# 第6章 图

> 图是重要的非线性数据结构，描述多对多的关系。掌握图的存储、遍历、最小生成树和最短路径算法是考研的核心内容。

---

## 1. 图的存储结构 <a id="storage"></a>

### 邻接矩阵

**核心思想**：用n×n的二维数组存储，matrix[i][j]表示顶点i到顶点j的边或权值。适合稠密图（边数接近n²）。

**示例**：无向图

```
顶点: 0 --- 1 --- 2
       \   /   /
         3

邻接矩阵:
    0   1   2   3
0   [0,  1,  0,  1]
1   [1,  0,  1,  1]
2   [0,  1,  0,  1]
3   [1,  1,  1,  0]

说明: matrix[0][1] = 1 表示0和1相连
```

```python
class GraphMatrix:
    def __init__(self, n: int, directed=False):
        self.n = n
        self.directed = directed
        self.matrix = [[float('inf')] * n for _ in range(n)]

        # 对角线设为0（自己到自己距离为0）
        for i in range(n):
            self.matrix[i][i] = 0

    def add_edge(self, u: int, v: int, weight=1) -> None:
        """添加边"""
        self.matrix[u][v] = weight
        if not self.directed:
            self.matrix[v][u] = weight  # 无向图对称

    def get_neighbors(self, u: int) -> list:
        """获取顶点u的邻居"""
        neighbors = []
        for v in range(self.n):
            if self.matrix[u][v] != float('inf') and u != v:
                neighbors.append(v)
        return neighbors
```

### 邻接表

**核心思想**：用数组的链表存储，adj_list[u]存储顶点u的所有邻接边。适合稀疏图（边数远小于n²）。

**示例**：与上图相同

```
邻接表:
0: [(1, 1), (3, 1)]  # 0连1(权1)和3(权1)
1: [(0, 1), (2, 1), (3, 1)]
2: [(1, 1), (3, 1)]
3: [(0, 1), (1, 1), (2, 1)]
```

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

---

## 2. 图的遍历 <a id="traversal"></a>

### 广度优先搜索（BFS）

**核心思想**：按层遍历图，从起点开始，先访问所有邻居，再访问邻居的邻居。使用队列实现。

### BFS 和 DFS 该怎么直觉地区分

- **BFS** 像往水里丢石头后的波纹，一圈一圈向外扩散，所以它天然适合求“边数意义下的最短路”。
- **DFS** 像走迷宫时先认准一条路一直走到底，走不通再回头，所以它更像“试探路径”和“递归搜索”。
- 一个看“层”，一个看“路”，把这点想清楚，很多题目选算法就快了。

**手写示例**：

```
图结构:
    1 --- 2 --- 5
    |           |
    3 --- 4 --- 6

从顶点1开始BFS:

初始: queue=[1], visited={1}
出队1, 访问1, 入队2,3
      queue=[2,3], visited={1,2,3}

出队2, 访问2, 入队5
      queue=[3,5], visited={1,2,3,5}

出队3, 访问3, 入队4
      queue=[5,4], visited={1,2,3,5,4}

出队5, 访问5, 入队6
      queue=[4,6], visited={1,2,3,5,4,6}

出队4, 访问4, 无新邻居
      queue=[6], visited={1,2,3,5,4,6}

出队6, 访问6, 无新邻居
      queue=[], visited={1,2,3,5,4,6}

结果: 1, 2, 3, 5, 4, 6
```

```python
from collections import deque

def bfs(graph: GraphAdjList, start: int, visited=None) -> list:
    """
    广度优先搜索
    返回遍历序列
    """
    if visited is None:
        visited = set()

    result = []
    queue = deque([start])
    visited.add(start)

    while queue:
        u = queue.popleft()
        result.append(u)

        # 访问所有未访问的邻居
        for v, _ in graph.adj_list[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)

    return result
```

### 深度优先搜索（DFS）

**核心思想**：一条路走到黑，遇到未访问的顶点就继续深入，直到回溯到有其他路可走。用递归或栈实现。

**手写示例**：

```
图结构:
    1 --- 2 --- 5
    |           |
    3 --- 4 --- 6

从顶点1开始DFS:

递归过程:
  dfs(1)
    访问1
    dfs(2)  # 第一个邻居
      访问2
      dfs(5)  # 第一个邻居
        访问5
        dfs(6)  # 唯一未访问邻居
          访问6
          无未访问邻居，返回
        无未访问邻居，返回
      无未访问邻居，返回
    dfs(3)  # 第二个邻居
      访问3
      dfs(4)  # 第一个邻居
        访问4
        无未访问邻居，返回
      无未访问邻居，返回
    无未访问邻居，返回

结果: 1, 2, 5, 6, 3, 4
```

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
```

---

## 3. 最小生成树（MST）<a id="mst"></a>

**问题**：在连通带权图中找一棵权值和最小的生成树（包含所有顶点，无环）。

### Prim算法

**核心思想**：从任意顶点开始，每次选择与当前生成树相连的最小边。适合稠密图。

**手写示例**：

```
带权图:
      2      3    (5)
   A ----- B ----- C
   |       |       |
 (6)     (4)     (6)
   |       |       |
   D ----- E ----- F
      2      3

初始: MST={A}, min_dist=[0,∞,∞,∞,∞,∞]

第1轮: 选A, 更新B=2, D=6
       min_dist=[0,2,∞,6,∞,∞]

第2轮: 选B(2), 更新C=3, E=4
       min_dist=[0,2,3,6,4,∞]
       加边(A,B), MST={A,B}

第3轮: 选C(3), 更新F=6
       min_dist=[0,2,3,6,4,6]
       加边(B,C), MST={A,B,C}

第4轮: 选E(4), 更新D=2(更小)
       min_dist=[0,2,3,2,4,6]
       加边(B,E), MST={A,B,C,E}

第5轮: 选D(2), 无新更新
       加边(D,E), MST={A,B,C,E,D}

第6轮: 选F(6), 无新更新
       加边(C,F), MST={A,B,C,E,D,F}

总权值: 2+3+4+2+6 = 17
```

```python
def prim(graph: GraphMatrix) -> tuple:
    """
    Prim算法求最小生成树
    返回：(总权重, 边列表)

    时间复杂度: O(V²)
    空间复杂度: O(V)
    """
    n = graph.n
    visited = [False] * n
    min_dist = [float('inf')] * n  # 到MST的最小距离
    parent = [-1] * n             # 最小距离边的起点

    min_dist[0] = 0  # 从顶点0开始
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

        # 松弛操作：更新邻接顶点的距离
        for v in range(n):
            weight = graph.matrix[u][v]
            if not visited[v] and weight < min_dist[v]:
                min_dist[v] = weight
                parent[v] = u

    return total_weight, edges
```

### Kruskal算法

**核心思想**：按边权值从小到大排序，依次选择不形成环的边。配合并查集判断环。适合稀疏图。

**手写详细示例**：

```
带权图:
      2      3    (5)
   A ----- B ----- C
   |       |       |
   (6)     (4)     (6)
   |       |       |
   D ----- E ----- F
      2      3

边按权值排序:
  权值=2: (A,B), (D,E)
  权值=3: (B,C), (E,F)
  权值=4: (B,E)
  权值=5: (A,C)
  权值=6: (A,D), (C,F)

初始状态: 每个顶点独立
  A, B, C, D, E, F 各自为一个集合

第1步: 选(A,B)=2
  find(A)=A, find(B)=B, 不同集合
  不成环, 加入MST
  合并后: {A,B}, {C}, {D}, {E}, {F}
  MST边: [(A,B)]

第2步: 选(D,E)=2
  find(D)=D, find(E)=E, 不同集合
  不成环, 加入MST
  合并后: {A,B}, {C}, {D,E}, {F}
  MST边: [(A,B), (D,E)]

第3步: 选(B,C)=3
  find(B)=A, find(C)=C, 不同集合
  不成环, 加入MST
  合并后: {A,B,C}, {D,E}, {F}
  MST边: [(A,B), (D,E), (B,C)]

第4步: 选(E,F)=3
  find(E)=D, find(F)=F, 不同集合
  不成环, 加入MST
  合并后: {A,B,C}, {D,E,F}
  MST边: [(A,B), (D,E), (B,C), (E,F)]

第5步: 选(B,E)=4
  find(B)=A, find(E)=D, 不同集合
  不成环, 加入MST
  合并后: {A,B,C,D,E,F}  所有顶点连通!
  MST边: [(A,B), (D,E), (B,C), (E,F), (B,E)]

第6步: 已选5边 = 6顶点-1, MST完成!

最终结果:
  MST边: (A,B), (D,E), (B,C), (E,F), (B,E)
  总权值: 2+2+3+3+4 = 14
  MST图:
       B ---- C
      / \     \
     A   E     F
          \    /
           D
```

```python
def kruskal(graph: GraphMatrix) -> tuple:
    """
    Kruskal算法求最小生成树
    返回：(总权重, 边列表)

    时间复杂度: O(ElogE)
    空间复杂度: O(V+E)
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

    uf = UnionFind(n)  # 需并查集
    total_weight = 0
    mst_edges = []

    for weight, u, v in edges:
        if not uf.connected(u, v):  # 不成环
            uf.union(u, v)
            total_weight += weight
            mst_edges.append((u, v, weight))

            # MST边数 = V-1 时完成
            if len(mst_edges) == n - 1:
                break

    return total_weight, mst_edges
```

---

## 4. 最短路径 <a id="shortest-path"></a>

### Dijkstra算法

**核心思想**：求单源最短路。每次选择距离起点最近的未访问顶点，松弛其邻接边。不能处理负权边。

**手写示例**：

```
带权图:
      2      3
   A ----- B ----- C
   |       |       |
 (5)     (1)     (1)
   |       |       |
   D ----- E ----- F
      1      2

从A出发求最短路:

初始: dist=[0,∞,∞,∞,∞,∞], visited=[]

第1轮: 选A(0), 松弛B=2, D=5
       dist=[0,2,∞,5,∞,∞], visited=[A]

第2轮: 选B(2), 松弛C=5, E=3
       dist=[0,2,5,5,3,∞], visited=[A,B]

第3轮: 选E(3), 松弛D=4, F=5
       dist=[0,2,5,4,3,5], visited=[A,B,E]

第4轮: 选D(4), 无新松弛
       dist=[0,2,5,4,3,5], visited=[A,B,E,D]

第5轮: 选C(5), 松弛F=6(不更小)
       dist=[0,2,5,4,3,5], visited=[A,B,E,D,C]

第6轮: 选F(5), 无新松弛
       dist=[0,2,5,4,3,5], visited=[A,B,E,D,C,F]

结果: A→各点最短距离
A→A:0, A→B:2, A→C:5, A→D:4, A→E:3, A→F:5
```

```python
def dijkstra(graph: GraphMatrix, start: int) -> tuple:
    """
    Dijkstra算法求单源最短路
    返回：(dist数组, path数组)

    时间复杂度: O(V²), 堆优化O(ElogV)
    空间复杂度: O(V)
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

**核心思想**：求全源最短路。尝试每个顶点k作为中间点，检查i→k→j是否比i→j更短。可以处理负权边（不含负权回路）。

**递推公式**：
```
dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

### 为什么 Floyd 的递推式长这样

把 `k` 看成“新开放使用的中转站”。

- 在第 `k` 轮之前，`dist[i][j]` 表示“不经过编号大于 `k-1` 的中间点时”的最短路。
- 到了第 `k` 轮，只需要问一个问题：
  - 直接从 `i` 到 `j` 更短？
  - 还是绕一下 `i -> k -> j` 更短？
- 所以更新式自然就是：
  - 原来的 `dist[i][j]`
  - 和 `dist[i][k] + dist[k][j]`
  - 取更小者

这也是 Floyd 好记的关键：本质上就是“要不要借助当前这个中转点”。

```python
def floyd(graph: GraphMatrix) -> tuple:
    """
    Floyd算法求全源最短路
    返回：(dist矩阵, path矩阵)

    时间复杂度: O(V³)
    空间复杂度: O(V²)
    """
    n = graph.n
    dist = [row[:] for row in graph.matrix]
    path = [[-1] * n for _ in range(n)]

    for k in range(n):      # 中间点
        for i in range(n):  # 起点
            for j in range(n):  # 终点
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    path[i][j] = k

    return dist, path
```

---

## 5. 判环、拓扑排序 & 关键路径 <a id="topo"></a>

### 图中如何判断有环

先分清题目里的图类型：

| 图类型 | 常用方法 | 判断依据 | 适合场景 |
|--------|----------|----------|----------|
| **有向图** | 拓扑排序 | 若最终输出顶点数 `< V`，说明有环 | 课程依赖、任务调度 |
| **有向图** | DFS | 若访问到“正在递归栈中”的顶点，说明出现回边 | 手写推导、解释回边 |
| **无向图** | Union-Find Set | 加边时若两端已在同一集合，则成环 | 边集处理、Kruskal同类题 |

**一句话记忆**：

- 有向图判环，优先想到 **拓扑排序 / DFS回边**。
- 无向图判环，优先想到 **并查集**。

### 方法一：用拓扑排序判断有向图是否有环

**核心思想**：如果图是 DAG，就一定能不断删去入度为 0 的顶点；如果删到一半删不动了，还剩下一批顶点，说明这些顶点互相依赖，形成了环。

**手算示例**：

```
有向图:
0 → 1
    ↓
    2 → 3
    ↑
    └── 1

边集写法:
0→1, 1→2, 2→1, 2→3

入度统计:
0:0
1:2   (来自0和2)
2:1   (来自1)
3:1   (来自2)

初始: queue=[0]，因为只有0的入度为0

第1步: 出队0，输出[0]
      删除边0→1，1的入度从2变成1
      此时 queue=[]

队列已经空了，但顶点1、2、3还没删完
说明剩余部分无法继续产生入度为0的点
原因就是 1 ↔ 2 形成了环

结论:
输出顶点数 = 1 < 4
所以图中有环
```

```python
from collections import deque

def has_cycle_directed_topo(graph: GraphAdjList) -> bool:
    """
    用拓扑排序判断有向图是否有环
    True表示有环，False表示无环
    """
    n = graph.n
    in_degree = [0] * n

    for u in range(n):
        for v, _ in graph.adj_list[u]:
            in_degree[v] += 1

    queue = deque([u for u in range(n) if in_degree[u] == 0])
    count = 0

    while queue:
        u = queue.popleft()
        count += 1

        for v, _ in graph.adj_list[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    return count != n
```

### 方法二：用 DFS 判断有向图是否有环

**核心思想**：DFS 过程中把顶点分成 3 种状态：

- `0`：未访问
- `1`：正在访问（已经进递归栈，还没回退）
- `2`：访问完成

如果从当前顶点还能走到一个状态为 `1` 的顶点，说明回到了当前递归路径上的老点，也就是出现了 **回边**，因此有环。

**手算示例**：

```
仍看刚才的有向图:
0→1, 1→2, 2→1, 2→3

初始状态:
state = [0, 0, 0, 0]

从0开始DFS:

dfs(0):
  state[0] = 1   # 0正在访问
  走到1

dfs(1):
  state[1] = 1   # 1正在访问
  走到2

dfs(2):
  state[2] = 1   # 2正在访问
  查看邻居1
  发现 state[1] = 1

这说明:
当前递归路径是 0 → 1 → 2
而2又能回到“还没退栈”的1
所以出现回边 2 → 1

结论: 图中有环
```

```python
def has_cycle_directed_dfs(graph: GraphAdjList) -> bool:
    """
    用DFS判断有向图是否有环
    state: 0=未访问, 1=正在访问, 2=访问完成
    """
    n = graph.n
    state = [0] * n

    def dfs(u: int) -> bool:
        state[u] = 1

        for v, _ in graph.adj_list[u]:
            if state[v] == 1:
                return True  # 找到回边，说明有环
            if state[v] == 0 and dfs(v):
                return True

        state[u] = 2
        return False

    for u in range(n):
        if state[u] == 0 and dfs(u):
            return True

    return False
```

> 补充：无向图也能用 DFS 判环，但要额外排除“回到父节点”这种正常回退。  
> 考研里更常见的组合是：**有向图用 DFS 回边判环，无向图用并查集判环**。

### 方法三：用 Union-Find Set 判断无向图是否有环

**核心思想**：把每个连通分量看成一个集合。每加入一条边 `(u, v)`：

- 如果 `u` 和 `v` 本来就在同一集合，那么这条边一加就会形成环
- 如果不在同一集合，就把两个集合合并

**手算示例**：

```
无向图边按顺序加入:
(0,1), (1,2), (2,3), (0,3)

初始:
{0}, {1}, {2}, {3}

加入(0,1):
find(0) != find(1)
合并后:
{0,1}, {2}, {3}

加入(1,2):
find(1) = find(0)
find(2) = 2
不在同一集合，继续合并
合并后:
{0,1,2}, {3}

加入(2,3):
find(2) = find(0)
find(3) = 3
不在同一集合，继续合并
合并后:
{0,1,2,3}

加入(0,3):
find(0) = find(3)
说明0和3早就连通
现在再加一条(0,3)，就会形成环

结论: 无向图有环
```

```python
class UnionFind:
    """并查集（路径压缩 + 按秩合并）"""

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


def has_cycle_undirected_union_find(n: int, edges: list[tuple[int, int]]) -> bool:
    """
    用并查集判断无向图是否有环
    这里直接传边集更方便，避免无向图邻接表中的重复边
    """
    uf = UnionFind(n)

    for u, v in edges:
        if uf.connected(u, v):
            return True
        uf.union(u, v)

    return False
```

### 拓扑排序（Kahn算法）

**核心思想**：对 DAG（有向无环图）排序，使得每条边 `(u→v)` 满足 `u` 在 `v` 之前。  
它不仅能输出依赖顺序，也能顺便判环：**如果无法输出全部顶点，说明图中有环**。

**手写示例**：

```
DAG:
   A → B → D
   ↓   ↓
   C → E → F

计算入度: A=0, B=2, C=1, D=1, E=2, F=1

初始: queue=[A](入度0)
出队A, result=[A]
      A的邻居B,C入度-1 → B=1, C=0
      C入队, queue=[C]

出队C, result=[A,C]
      C的邻居B,E入度-1 → B=0, E=1
      B入队, queue=[B]

出队B, result=[A,C,B]
      B的邻居D,E入度-1 → D=0, E=0
      D,E入队, queue=[D,E]

出队D, result=[A,C,B,D]
      D无邻居, queue=[E]

出队E, result=[A,C,B,D,E]
      E的邻居F入度-1 → F=0
      F入队, queue=[F]

出队F, result=[A,C,B,D,E,F]
      F无邻居, queue=[]

结果: A, C, B, D, E, F
```

```python
from collections import deque

def topological_sort(graph: GraphAdjList) -> list:
    """
    Kahn算法拓扑排序
    返回排序序列，有环返回空

    时间复杂度: O(V+E)
    空间复杂度: O(V)
    """
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

---

## 6. 考研重点 & 易错点

### 高频考点

| 考点 | 关键要点 |
|------|---------|
| **邻接矩阵 vs 邻接表** | 稠密图用矩阵，稀疏图用邻接表 |
| **BFS vs DFS** | BFS层序遍历，DFS深度优先 |
| **图中判环** | 先看有向图还是无向图，再选拓扑/DFS/并查集 |
| **Prim vs Kruskal** | Prim适合稠密图，Kruskal适合稀疏图 |
| **Dijkstra vs Floyd** | Dijkstra单源，Floyd全源 |
| **拓扑排序** | 只能用于DAG，可检测环 |

### 易错点

| 易错点 | 正确做法 |
|--------|---------|
| 判环方法混用 | 有向图优先用拓扑排序或DFS回边；无向图优先用并查集 |
| Dijkstra负权边 | 不能处理，改用Bellman-Ford |
| Prim算法初始 | min_dist[start]=0，其他为∞ |
| Kruskal成环判断 | 用并查集，connected(u,v) |
| Floyd三重循环 | 顺序k,i,j不能错 |
| 拓扑排序有环 | 返回空或检测环 |

### 应用场景

| 场景 | 算法 | 原因 |
|------|------|------|
| 判断课程依赖是否冲突 | 拓扑排序 / DFS判环 | 检测有向环 |
| 判断无向边集是否成环 | 并查集 | 合并集合时快速判断 |
| 无权图最短路 | BFS | 天然层序就是距离 |
| 最短路径(无负权) | Dijkstra | 单源高效 |
| 全源最短路 | Floyd | 代码简洁 |
| 连通所有点(最小权) | Prim/Kruskal | 最小生成树 |
| 依赖关系解决 | 拓扑排序 | 前驱后继关系 |
| 项目工期估算 | 关键路径 | 最长路径决定 |

---

## 7. 复杂度总结表

| 算法 | 时间复杂度 | 空间复杂度 | 适用场景 |
|------|-----------|-----------|---------|
| 邻接矩阵存储 | O(V²) | O(V²) | 稠密图 |
| 邻接表存储 | O(V+E) | O(V+E) | 稀疏图 |
| BFS/DFS | O(V+E) | O(V) | 图遍历 |
| DFS判环（有向图） | O(V+E) | O(V) | 找回边 |
| 拓扑判环（有向图） | O(V+E) | O(V) | 统计是否能删完点 |
| 并查集判环（无向图） | O(Eα(V)) | O(V) | 边集判环 |
| Prim算法 | O(V²) | O(V) | 稠密图MST |
| Prim(堆优化) | O(ElogV) | O(V) | 通用MST |
| Kruskal算法 | O(ElogE) | O(V) | 稀疏图MST |
| Dijkstra算法 | O(V²) | O(V) | 单源最短路 |
| Dijkstra(堆优化) | O(ElogV) | O(V) | 优化版 |
| Floyd算法 | O(V³) | O(V²) | 全源最短路 |
| 拓扑排序 | O(V+E) | O(V) | DAG排序 |

---

## 📝 完整代码示例

```python
from collections import deque


class GraphAdjList:
    def __init__(self, n: int, directed=False):
        self.n = n
        self.directed = directed
        self.adj_list = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, weight=1) -> None:
        self.adj_list[u].append((v, weight))
        if not self.directed:
            self.adj_list[v].append((u, weight))


def bfs(graph: GraphAdjList, start: int) -> list:
    """广度优先搜索"""
    visited = set([start])
    result = []
    queue = deque([start])

    while queue:
        u = queue.popleft()
        result.append(u)
        for v, _ in graph.adj_list[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)

    return result


def dfs(graph: GraphAdjList, start: int) -> list:
    """深度优先搜索（递归）"""
    visited = set()
    result = []

    def _dfs(u):
        visited.add(u)
        result.append(u)
        for v, _ in graph.adj_list[u]:
            if v not in visited:
                _dfs(v)

    _dfs(start)
    return result


if __name__ == "__main__":
    # 构建测试图
    # 1 --- 2 --- 5
    # |           |
    # 3 --- 4 --- 6
    graph = GraphAdjList(7)  # 顶点1-6
    edges = [(1,2), (2,5), (1,3), (3,4), (4,6), (5,6)]
    for u, v in edges:
        graph.add_edge(u, v)

    print("=" * 40)
    print("图遍历测试")
    print("=" * 40)
    print(f"BFS从顶点1: {bfs(graph, 1)}")
    print(f"DFS从顶点1: {dfs(graph, 1)}")
```

## 常考题型与相关算法题

### 常考点

- 邻接矩阵与邻接表的适用场景和复杂度比较。
- BFS / DFS 的访问顺序、`visited` 数组的使用。
- 图中判环时，先判断是 **有向图** 还是 **无向图**，再选择拓扑排序、DFS 或并查集。
- Prim 与 Kruskal 的适用图类型和复杂度。
- Dijkstra 不能处理负权边，Floyd 可以处理负权边但不能有负环。
- 拓扑排序只适用于 DAG，关键路径建立在 AOE 网基础上。

### 相关算法题

| 题目 | 训练点 |
|------|--------|
| LeetCode 200. 岛屿数量 | DFS / BFS |
| LeetCode 547. 省份数量 | 图遍历 / 并查集 |
| LeetCode 207. 课程表 | 拓扑排序判环 |
| LeetCode 210. 课程表 II | 拓扑序输出 |
| LeetCode 684. 冗余连接 | 并查集判无向环 |
| LeetCode 685. 冗余连接 II | 有向图判环 + 入度分析 |
| LeetCode 743. 网络延迟时间 | 单源最短路 |
| LeetCode 1584. 连接所有点的最小费用 | 最小生成树 |
