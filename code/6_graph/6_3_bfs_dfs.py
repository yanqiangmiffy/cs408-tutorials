"""
图的遍历: BFS 和 DFS

1. 广度优先搜索 (BFS):
   - 类似层次遍历, 用队列
   - 时间: 邻接表 O(V+E), 邻接矩阵 O(V²)
   - 可求最短路径 (无权图)
   - BFS 生成树

2. 深度优先搜索 (DFS):
   - 类似先序遍历, 用递归/栈
   - 时间: 邻接表 O(V+E), 邻接矩阵 O(V²)
   - DFS 生成树

考研要点:
  - BFS/DFS 的手写过程 (按邻接表/矩阵)
  - 生成树 vs 生成森林 (非连通图)
  - BFS 求无权图最短路径
"""

from collections import deque


class Graph:
    """邻接表表示的图"""
    def __init__(self, vertices, directed=False):
        self.vertices = vertices
        self.directed = directed
        self.adj = {v: [] for v in vertices}

    def add_edge(self, u, v, w=1):
        self.adj[u].append(v)
        if not self.directed:
            self.adj[v].append(u)


# ==========================================
# BFS
# ==========================================

def bfs(graph, start):
    """广度优先搜索

    用队列实现:
    1. 起点入队, 标记已访问
    2. 队头出队, 访问
    3. 将其未访问的邻居全部入队
    4. 重复
    """
    visited = set()
    queue = deque([start])
    visited.add(start)
    order = []

    while queue:
        v = queue.popleft()
        order.append(v)
        for neighbor in sorted(graph.adj[v]):  # 排序保证确定性
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


def bfs_verbose(graph, start):
    """带详细输出的 BFS"""
    visited = set()
    queue = deque([start])
    visited.add(start)
    order = []
    step = 0

    print(f"  BFS from {start}:")
    print(f"  {'步骤':>4s} {'出队':>4s} {'入队':>12s} {'队列':>15s}")
    print(f"  {'─' * 40}")

    while queue:
        step += 1
        v = queue.popleft()
        order.append(v)
        enqueued = []
        for neighbor in sorted(graph.adj[v]):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                enqueued.append(neighbor)
        print(f"  {step:>4d} {v:>4s} {str(enqueued):>12s} {str(list(queue)):>15s}")

    return order


def bfs_shortest_path(graph, start):
    """BFS 求无权图最短路径

    BFS 天然保证: 先访问到的节点距离更近
    """
    dist = {start: 0}
    prev = {start: None}
    queue = deque([start])

    while queue:
        v = queue.popleft()
        for neighbor in graph.adj[v]:
            if neighbor not in dist:
                dist[neighbor] = dist[v] + 1
                prev[neighbor] = v
                queue.append(neighbor)

    return dist, prev


def get_path(prev, start, end):
    """通过前驱数组还原路径"""
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path if path[0] == start else []


# ==========================================
# DFS
# ==========================================

def dfs(graph, start):
    """深度优先搜索 (递归)"""
    visited = set()
    order = []

    def _dfs(v):
        visited.add(v)
        order.append(v)
        for neighbor in sorted(graph.adj[v]):
            if neighbor not in visited:
                _dfs(neighbor)

    _dfs(start)
    return order


def dfs_iterative(graph, start):
    """深度优先搜索 (非递归, 用栈)"""
    visited = set()
    stack = [start]
    order = []

    while stack:
        v = stack.pop()
        if v in visited:
            continue
        visited.add(v)
        order.append(v)
        # 逆序入栈, 保证字典序小的先被访问
        for neighbor in sorted(graph.adj[v], reverse=True):
            if neighbor not in visited:
                stack.append(neighbor)

    return order


def dfs_verbose(graph, start):
    """带详细输出的 DFS"""
    visited = set()
    order = []

    print(f"  DFS from {start}:")

    def _dfs(v, depth=0):
        visited.add(v)
        order.append(v)
        indent = "  " * depth
        print(f"    {indent}访问 {v}")
        for neighbor in sorted(graph.adj[v]):
            if neighbor not in visited:
                print(f"    {indent}  → 递归进入 {neighbor}")
                _dfs(neighbor, depth + 1)
            else:
                print(f"    {indent}  → {neighbor} 已访问, 跳过")

    _dfs(start)
    return order


def traversal_all(graph):
    """遍历所有连通分量"""
    visited = set()
    components = []

    for v in graph.vertices:
        if v not in visited:
            component = []
            queue = deque([v])
            visited.add(v)
            while queue:
                node = queue.popleft()
                component.append(node)
                for neighbor in sorted(graph.adj[node]):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            components.append(component)

    return components


def demo():
    """图遍历演示"""
    print("=" * 60)
    print("图的BFS和DFS遍历")
    print("=" * 60)

    g = Graph(['A', 'B', 'C', 'D', 'E', 'F'])
    edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'),
             ('C', 'E'), ('D', 'F'), ('E', 'F')]
    for u, v in edges:
        g.add_edge(u, v)

    print(f"""
  图结构:
    A --- B --- D
    |     |     |
    C --- E --- F
    """)

    # BFS
    print(f"\n  === BFS ===")
    bfs_verbose(g, 'A')
    print(f"  BFS 序列: {bfs(g, 'A')}")

    # DFS
    print(f"\n  === DFS ===")
    dfs_verbose(g, 'A')
    print(f"  DFS 序列 (递归):   {dfs(g, 'A')}")
    print(f"  DFS 序列 (非递归): {dfs_iterative(g, 'A')}")

    # BFS 最短路径
    print(f"\n  === BFS 最短路径 ===")
    dist, prev = bfs_shortest_path(g, 'A')
    for v in sorted(dist.keys()):
        path = get_path(prev, 'A', v)
        print(f"  A → {v}: 距离={dist[v]}, 路径={'→'.join(path)}")

    print()


if __name__ == "__main__":
    demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. BFS:
     用队列, 层层推进
     时间: 邻接表 O(V+E), 矩阵 O(V²)
     可求无权图最短路径

  2. DFS:
     用递归/栈, 一条路走到黑再回溯
     时间: 邻接表 O(V+E), 矩阵 O(V²)

  3. 手写遍历序列:
     注意邻接表中邻居的顺序!
     不同顺序可能得到不同的遍历序列

  4. 非连通图:
     需要对每个未访问顶点调用 BFS/DFS
     得到的是生成森林 (多棵生成树)
    """)
