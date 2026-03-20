# 手写模板库

## 使用说明

- 这里放的是考场上最值得默写的短模板。
- 代码优先追求“短、稳、边界清楚”，不是业务工程写法。

## 1. 单链表反转

```python
def reverse_list(head):
    prev = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev
```

## 2. 链表倒数第 k 个结点

```python
def kth_from_end(head, k):
    fast = slow = head
    for _ in range(k):
        if fast is None:
            return None
        fast = fast.next
    while fast:
        fast = fast.next
        slow = slow.next
    return slow
```

## 3. 找两个链表的第一个公共结点

```python
def intersection_node(headA, headB):
    p, q = headA, headB
    while p is not q:
        p = p.next if p else headB
        q = q.next if q else headA
    return p
```

## 4. 二叉树递归遍历

```python
def preorder(root):
    if root is None:
        return
    print(root.val)
    preorder(root.left)
    preorder(root.right)
```

## 5. 二叉树层序遍历

```python
from collections import deque


def level_order(root):
    if root is None:
        return []
    q = deque([root])
    ans = []
    while q:
        node = q.popleft()
        ans.append(node.val)
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    return ans
```

## 6. KMP 前缀函数

```python
def build_next(p):
    nxt = [0] * len(p)
    j = 0
    for i in range(1, len(p)):
        while j > 0 and p[i] != p[j]:
            j = nxt[j - 1]
        if p[i] == p[j]:
            j += 1
        nxt[i] = j
    return nxt
```

## 7. BFS

```python
from collections import deque


def bfs(graph, start):
    visited = {start}
    q = deque([start])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                q.append(v)
    return order
```

## 8. DFS

```python
def dfs(graph, u, visited, order):
    visited.add(u)
    order.append(u)
    for v in graph[u]:
        if v not in visited:
            dfs(graph, v, visited, order)
```

## 9. 拓扑排序

```python
from collections import deque


def topo_sort(graph):
    n = len(graph)
    indegree = [0] * n
    for u in range(n):
        for v in graph[u]:
            indegree[v] += 1

    q = deque(i for i in range(n) if indegree[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)
    return order if len(order) == n else []
```

## 10. Dijkstra

```python
import heapq


def dijkstra(graph, start):
    n = len(graph)
    dist = [float("inf")] * n
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[v] > d + w:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return dist
```

## 11. 并查集

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.parent[rx] = ry
```

## 12. 快速排序 partition

```python
def partition(nums, left, right):
    pivot = nums[left]
    i, j = left, right
    while i < j:
        while i < j and nums[j] >= pivot:
            j -= 1
        nums[i] = nums[j]
        while i < j and nums[i] <= pivot:
            i += 1
        nums[j] = nums[i]
    nums[i] = pivot
    return i
```

## 考前建议

- 链表、树、图、KMP、拓扑排序至少各手写 3 遍。
- 每写完一个模板，都主动检查边界：空输入、单元素、最后一个结点、越界。
