# 第5章 树与二叉树

> **考研要点速记**：二叉树性质n₀=n₂+1是考研必考；哈夫曼树用于构造最优前缀编码；并查集用路径压缩和按秩合并优化，适用于处理等价关系问题。

## 1. 二叉树遍历 <a id="traversal"></a>

### 先序遍历（根-左-右）

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def preorder_recursive(root: TreeNode) -> list:
    """先序遍历（递归）"""
    result = []

    def dfs(node):
        if not node:
            return
        result.append(node.val)  # 访问根
        dfs(node.left)            # 遍历左子树
        dfs(node.right)           # 遍历右子树

    dfs(root)
    return result

def preorder_iterative(root: TreeNode) -> list:
    """先序遍历（非递归，用栈）"""
    if not root:
        return []

    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)

        # 右子树先入栈（后处理）
        if node.right:
            stack.append(node.right)
        # 左子树后入栈（先处理）
        if node.left:
            stack.append(node.left)

    return result
```

### 中序遍历（左-根-右）

```python
def inorder_recursive(root: TreeNode) -> list:
    """中序遍历（递归）"""
    result = []

    def dfs(node):
        if not node:
            return
        dfs(node.left)
        result.append(node.val)
        dfs(node.right)

    dfs(root)
    return result

def inorder_iterative(root: TreeNode) -> list:
    """中序遍历（非递归，用栈）"""
    result = []
    stack = []
    curr = root

    while curr or stack:
        # 一路向左，将结点入栈
        while curr:
            stack.append(curr)
            curr = curr.left

        # 弹出并访问
        curr = stack.pop()
        result.append(curr.val)

        # 转向右子树
        curr = curr.right

    return result
```

### 层序遍历（BFS）

```python
from collections import deque

def level_order(root: TreeNode) -> list:
    """层序遍历"""
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        result.append(node.val)

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return result
```

## 2. 线索二叉树 <a id="threaded"></a>

线索二叉树利用空指针域存储前驱和后继信息，便于线性遍历。

```python
class ThreadTreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None
        self.ltag = 0  # 0: left是左孩子，1: left是前驱
        self.rtag = 0  # 0: right是右孩子，1: right是后继

def in_threading(node: ThreadTreeNode, pre: list) -> None:
    """中序线索化"""
    if not node:
        return

    # 线索化左子树
    in_threading(node.left, pre)

    # 处理当前结点
    if not node.left:
        node.ltag = 1
        node.left = pre[0]  # 前驱
    if pre[0] and not pre[0].right:
        pre[0].rtag = 1
        pre[0].right = node  # 后继

    pre[0] = node  # 更新前驱

    # 线索化右子树
    in_threading(node.right, pre)
```

## 3. 哈夫曼树 <a id="huffman"></a>

哈夫曼树是带权路径长度最短的二叉树，常用于数据压缩。

```python
import heapq

class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text: str) -> HuffmanNode:
    """构建哈夫曼树"""
    # 统计字符频率
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1

    # 创建叶子节点并加入最小堆
    heap = [HuffmanNode(char, f) for char, f in freq.items()]
    heapq.heapify(heap)

    # 合并节点构建树
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heap[0] if heap else None

def generate_codes(node: HuffmanNode, prefix: str, code_map: dict) -> None:
    """生成哈夫曼编码"""
    if node:
        if node.char is not None:  # 叶子节点
            code_map[node.char] = prefix
        else:
            generate_codes(node.left, prefix + '0', code_map)
            generate_codes(node.right, prefix + '1', code_map)

def huffman_encode(text: str) -> tuple:
    """哈夫曼编码"""
    root = build_huffman_tree(text)
    code_map = {}
    generate_codes(root, '', code_map)

    encoded = ''.join(code_map[char] for char in text)
    return encoded, code_map, root
```

## 4. 并查集 <a id="union-find"></a>

并查集用于处理不相交集合的合并和查询操作，带路径压缩和按秩合并。

```python
class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))  # 父节点
        self.rank = [0] * size          # 树的高度（秩）

    def find(self, x: int) -> int:
        """查找x的根节点，带路径压缩"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 路径压缩
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        """合并x和y所在的集合，按秩合并"""
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x != root_y:
            # 按秩合并：将矮树挂到高树上
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1

    def connected(self, x: int, y: int) -> bool:
        """判断x和y是否在同一集合"""
        return self.find(x) == self.find(y)


# 应用：计算连通分量数量
def count_connected_components(n: int, edges: list) -> int:
    """统计连通分量数量"""
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)

    roots = set()
    for i in range(n):
        roots.add(uf.find(i))
    return len(roots)
```

## 考研重点 & 易错点

- ⚠️ 易错点：二叉树性质n₀=n₂+1只适用于非空二叉树，空树n₀=0
- 📌 高频考点：由先序/后序+中序序列还原二叉树
- ⚠️ 易错点：线索二叉树的ltag和rtag含义，0表示孩子指针，1表示线索
- 📌 高频考点：哈夫曼树的构建和WPL计算
- 📌 高频考点：并查集的路径压缩和按秩合并，时间复杂度接近O(1)

## 复杂度总结表

| 操作 | 时间复杂度 | 空间复杂度 |
|------|-----------|-----------|
| 二叉树递归遍历 | O(n) | O(h)栈空间 |
| 二叉树非递归遍历 | O(n) | O(n) |
| 层序遍历 | O(n) | O(n)队列 |
| 哈夫曼树构建 | O(nlogn) | O(n) |
| 并查集查找(未优化) | O(h) | O(1) |
| 并查集查找(路径压缩) | O(α(n))≈O(1) | O(1) |
| 并查集合并 | O(α(n))≈O(1) | O(1) |
