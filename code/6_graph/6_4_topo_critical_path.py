"""
拓扑排序 + 关键路径

1. 拓扑排序 (DAG):
   - 对有向无环图的顶点排序, 使得每条边 u→v 中 u 排在 v 前面
   - 用途: 判断 DAG, 任务调度
   - Kahn 算法: 每次选入度为0的顶点

2. 关键路径:
   - AOE 网 (用边表示活动, 顶点表示事件)
   - 关键路径 = 从源点到汇点的最长路径
   - 关键活动 = e(i) == l(i) 的活动

考研要点:
  - 手写拓扑排序过程
  - 求 ve, vl, e, l 四个数组
  - 关键路径可能有多条
"""

from collections import deque


# ==========================================
# 拓扑排序
# ==========================================

def topological_sort(vertices, edges):
    """拓扑排序 (Kahn 算法)

    思路:
    1. 计算所有顶点的入度
    2. 将入度为 0 的顶点入队
    3. 出队一个顶点, 将其所有邻居的入度减 1
    4. 入度变 0 的顶点入队
    5. 重复直到队空
    6. 如果输出的顶点数 < 总数 → 有环!
    """
    adj = {v: [] for v in vertices}
    in_degree = {v: 0 for v in vertices}

    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1

    queue = deque()
    for v in vertices:
        if in_degree[v] == 0:
            queue.append(v)

    result = []
    step = 0
    print(f"  拓扑排序 (Kahn 算法):")
    print(f"  初始入度: {dict(in_degree)}")
    print(f"  {'步骤':>4s} {'出队':>4s} {'更新入度':>20s} {'队列':>15s}")
    print(f"  {'─' * 50}")

    while queue:
        step += 1
        v = queue.popleft()
        result.append(v)
        updates = []
        for neighbor in adj[v]:
            in_degree[neighbor] -= 1
            updates.append(f"{neighbor}:{in_degree[neighbor]}")
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
        print(f"  {step:>4d} {v:>4s} {','.join(updates):>20s} {str(list(queue)):>15s}")

    if len(result) < len(vertices):
        print(f"\n  ⚠️ 图中有环! 只排出了 {len(result)}/{len(vertices)} 个顶点")
        return None

    return result


def dfs_topological_sort(vertices, edges):
    """拓扑排序 (DFS 版)

    思路: DFS 后序遍历的逆序 = 拓扑序
    """
    adj = {v: [] for v in vertices}
    for u, v in edges:
        adj[u].append(v)

    visited = set()
    stack = []

    def dfs(v):
        visited.add(v)
        for neighbor in adj[v]:
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(v)  # 后序加入

    for v in vertices:
        if v not in visited:
            dfs(v)

    return stack[::-1]  # 逆序


# ==========================================
# 关键路径
# ==========================================

def critical_path(vertices, edges_with_weight):
    """关键路径算法

    edges_with_weight: [(u, v, weight), ...]

    四个数组:
    ve[j]: 事件 j 的最早发生时间 (正向拓扑排序求)
    vl[j]: 事件 j 的最迟发生时间 (逆向拓扑排序求)
    e[i]:  活动 i 的最早开始时间 = ve[活动起点]
    l[i]:  活动 i 的最迟开始时间 = vl[活动终点] - 活动持续时间

    关键活动: e[i] == l[i]
    """
    adj = {v: [] for v in vertices}
    radj = {v: [] for v in vertices}
    in_degree = {v: 0 for v in vertices}

    for u, v, w in edges_with_weight:
        adj[u].append((v, w))
        radj[v].append((u, w))
        in_degree[v] += 1

    # 1. 拓扑排序
    topo_order = []
    queue = deque()
    for v in vertices:
        if in_degree[v] == 0:
            queue.append(v)

    in_deg_copy = dict(in_degree)
    while queue:
        v = queue.popleft()
        topo_order.append(v)
        for neighbor, w in adj[v]:
            in_deg_copy[neighbor] -= 1
            if in_deg_copy[neighbor] == 0:
                queue.append(neighbor)

    if len(topo_order) < len(vertices):
        print("  图中有环!")
        return

    # 2. 求 ve (最早发生时间) - 正向
    ve = {v: 0 for v in vertices}
    for u in topo_order:
        for v, w in adj[u]:
            ve[v] = max(ve[v], ve[u] + w)

    # 3. 求 vl (最迟发生时间) - 逆向
    max_ve = max(ve.values())
    vl = {v: max_ve for v in vertices}
    for u in reversed(topo_order):
        for v, w in adj[u]:
            vl[u] = min(vl[u], vl[v] - w)

    # 4. 求 e, l 和关键活动
    print(f"\n  拓扑序: {topo_order}")
    print(f"\n  事件最早/最迟时间:")
    print(f"  {'事件':>4s} {'ve':>5s} {'vl':>5s} {'vl-ve':>5s}")
    print(f"  {'─' * 22}")
    for v in topo_order:
        slack = vl[v] - ve[v]
        mark = " ← 关键" if slack == 0 else ""
        print(f"  {v:>4s} {ve[v]:>5d} {vl[v]:>5d} {slack:>5d}{mark}")

    print(f"\n  活动分析:")
    print(f"  {'活动':>8s} {'e':>5s} {'l':>5s} {'l-e':>5s} {'关键?':>6s}")
    print(f"  {'─' * 30}")
    critical_edges = []
    for u, v, w in edges_with_weight:
        e_val = ve[u]
        l_val = vl[v] - w
        slack = l_val - e_val
        is_critical = slack == 0
        mark = "✓" if is_critical else ""
        print(f"  {u}→{v}({w}){' ' * (4 - len(u) - len(v))} "
              f"{e_val:>5d} {l_val:>5d} {slack:>5d} {mark:>6s}")
        if is_critical:
            critical_edges.append((u, v, w))

    print(f"\n  关键路径: ", end="")
    if critical_edges:
        print(" → ".join(f"{u}→{v}" for u, v, w in critical_edges))
        print(f"  关键路径长度: {max_ve}")


def topo_demo():
    """拓扑排序演示"""
    print("=" * 60)
    print("拓扑排序")
    print("=" * 60)

    vertices = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']
    edges = [
        ('C1', 'C3'), ('C1', 'C4'),
        ('C2', 'C3'), ('C2', 'C5'),
        ('C3', 'C4'), ('C3', 'C5'), ('C3', 'C6'),
        ('C5', 'C6'),
    ]
    print(f"\n  课程先修关系: {edges}")
    result = topological_sort(vertices, edges)
    print(f"\n  拓扑序列: {result}")
    print()


def critical_path_demo():
    """关键路径演示"""
    print("=" * 60)
    print("关键路径")
    print("=" * 60)

    vertices = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6']
    edges = [
        ('V1', 'V2', 3), ('V1', 'V3', 2),
        ('V2', 'V4', 2), ('V2', 'V5', 3),
        ('V3', 'V4', 4), ('V3', 'V6', 3),
        ('V4', 'V6', 2),
        ('V5', 'V6', 1),
    ]
    print(f"\n  AOE 网:")
    for u, v, w in edges:
        print(f"    {u} →({w})→ {v}")

    critical_path(vertices, edges)
    print()


if __name__ == "__main__":
    topo_demo()
    critical_path_demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 拓扑排序:
     每次选入度为0的顶点
     不唯一 (可能多个入度为0)
     若排完的顶点数 < 总数 → 有环

  2. 关键路径:
     ve: 事件最早时间 (正向, 取max)
     vl: 事件最迟时间 (逆向, 取min)
     e: 活动最早 = ve[起点]
     l: 活动最迟 = vl[终点] - 持续时间
     关键活动: e == l (余量为0)

  3. 注意:
     - 关键路径可能不唯一
     - 缩短非关键活动不影响工期
     - 缩短关键活动可能改变关键路径
    """)
