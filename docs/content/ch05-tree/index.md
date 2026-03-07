# 第5章 树与二叉树

> 树是重要的非线性数据结构，二叉树是树的特例。掌握二叉树遍历、哈夫曼树和并查集是考研的核心内容。

---

## 1. 二叉树基本概念

### 二叉树定义

二叉树是每个结点最多有两个子结点的树结构：左子树和右子树。

### 二叉树性质（必考！）

| 性质 | 内容 |
|------|------|
| 1 | 非空二叉树上第k层最多有 2^(k-1) 个结点 |
| 2 | 深度为h的二叉树最多有 2^h - 1 个结点 |
| 3 | n₀ = n₂ + 1（叶子结点数 = 度为2的结点数 + 1） |
| 4 | 完全二叉树按层序编号：编号为i的结点，左孩子2i，右孩子2i+1 |
| 5 | 完全二叉树n个结点，深度 ⌊log₂n⌋ + 1 |

**性质3的证明思路**：
- 每个度2的结点产生2条边，度1的结点产生1条边，叶子结点产生0条边
- 总边数 = n₂ × 2 + n₁ × 1
- 总边数 = n - 1（树中边数 = 结点数 - 1）
- 因此：n = n₀ + n₁ + n₂ = n₀ + n₁ + n₂
- 代入得：n₀ = n₂ + 1

---

## 2. 二叉树遍历 <a id="traversal"></a>

### 先序遍历（根-左-右）

**顺序**：先访问根结点，再遍历左子树，最后遍历右子树

### 中序遍历（左-根-右）

**顺序**：先遍历左子树，再访问根结点，最后遍历右子树

### 后序遍历（左-右-根）

**顺序**：先遍历左子树，再遍历右子树，最后访问了根结点

### 层序遍历（BFS）

**顺序**：按层从上到下，每层从左到右访问

### 遍历示例（手写演示）

**二叉树结构**：

```
        A
       / \
      B   C
     / \   \
    D   E   F
```

**先序遍历（根-左-右）**：
```
1. 访问 A
2. 遍历 A 的左子树（以B为根）
   2.1 访问 B
   2.2 遍历 B 的左子树（以D为根）
       2.2.1 访问 D
   2.3 遍历 B 的右子树（以E为根）
       2.3.1 访问 E
3. 遍历 A 的右子树（以C为根）
   3.1 访问 C
   3.2 C 的左子树为空
   3.3 遍历 C 的右子树（以F为根）
       3.3.1 访问 F

结果: A B D E C F
```

**中序遍历（左-根-右）**：
```
结果: D B E A C F
```

**后序遍历（左-右-根）**：
```
结果: D E B F C A
```

**层序遍历**：
```
结果: A B C D E F
```

### Python实现

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


def level_order(root: TreeNode) -> list:
    """层序遍历（BFS）"""
    if not root:
        return []

    result = []
    from collections import deque
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

---

## 3. 线索二叉树 <a id="threaded"></a>

**核心思想**：二叉树有n个结点，2n个指针域，其中n+1个空指针。线索二叉树利用这些空指针存储前驱和后继信息。

### 标志位含义

- `ltag = 0`：left指向左孩子；`ltag = 1`：left指向前驱
- `rtag = 0`：right指向右孩子；`rtag = 1`：right指向后继

### 中序线索化

```python
class ThreadTreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None
        self.ltag = 0  # 0: 左孩子, 1: 前驱
        self.rtag = 0  # 0: 右孩子, 1: 后继


def in_threading(node: ThreadTreeNode, pre: list) -> None:
    """中序线索化"""
    if not node:
        return

    # 线索化左子树
    in_threading(node.left, pre)

    # 处理当前结点的左指针
    if not node.left:
        node.ltag = 1
        node.left = pre[0]  # 前驱

    # 处理前驱结点的右指针
    if pre[0] and not pre[0].right:
        pre[0].rtag = 1
        pre[0].right = node  # 后继

    # 更新前驱指针
    pre[0] = node

    # 线索化右子树
    in_threading(node.right, pre)
```

---

## 4. 哈夫曼树 <a id="huffman"></a>

**核心思想**：带权路径长度（WPL）最小的二叉树，用于数据压缩和最优编码。

### 构建步骤

1. 统计每个字符的频率
2. 每个字符创建叶子结点，按频率构成最小堆
3. 每次取出两个最小频率的结点，合并为新结点
4. 新结点频率为两子结点频率之和
5. 重复直到只剩一个结点（根结点）

### 哈夫曼树构建示例

**输入字符串**: `"ABACBCA"`

**步骤1**：统计频率
```
A: 3, B: 2, C: 2
```

**步骤2**：创建初始堆
```
堆: [A(3), B(2), C(2)]
```

**步骤3**：合并最小两个
```
1. 取出 B(2), C(2)
2. 合并为 BC(4)
3. 堆: [A(3), BC(4)]
```

**步骤4**：继续合并
```
1. 取出 A(3), BC(4)
2. 合并为 ABC(7)
3. 堆: [ABC(7)]
```

**哈夫曼树**：
```
      ABC(7)
      /    \
    A(3)  BC(4)
          /    \
       B(2)   C(2)
```

**哈夫曼编码**（左0右1）：
```
A: 0
B: 10
C: 11
```

**WPL计算**：
```
WPL = 3×1 + 2×2 + 2×2 = 3 + 4 + 4 = 11
```

### Python实现

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
    """生成哈夫曼编码（左0右1）"""
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

---

## 5. 并查集（Union-Find）<a id="union-find"></a>

**核心思想**：维护不相交集合，支持两个操作：find（查找根结点）和union（合并两个集合）。用于处理等价关系问题。

### 两种优化

1. **路径压缩**：find时将沿途所有结点直接指向根
2. **按秩合并**：union时将矮树挂到高树上

### 并查集操作示例

**初始**：5个元素，各自独立
```
parent = [0, 1, 2, 3, 4]  # 每个元素是自己的根
```

**union(0, 1)**：合并0和1
```
parent = [0, 0, 2, 3, 4]
        集合1: {0, 1}, 集合2: {2}, 集合3: {3}, 集合4: {4}
```

**union(2, 3)**：合并2和3
```
parent = [0, 0, 2, 2, 4]
        集合1: {0, 1}, 集合2: {2, 3}, 集合3: {4}
```

**find(1)**：查找1的根
```
1 → parent[1]=0 → parent[0]=0 (根)
返回 0
```

**connected(1, 3)**：判断1和3是否连通
```
find(1) = 0
find(3) = 2
0 != 2 → 不连通
```

**union(1, 3)**：合并集合{0,1}和集合{2,3}
```
parent = [0, 0, 0, 2, 4]
        集合1: {0, 1, 2, 3}, 集合2: {4}
```

### 路径压缩示例

**当前状态**：`parent = [0, 0, 1, 2, 4]`

```
find(3): 3 → 2 → 1 → 0 (根)
路径压缩后:
parent = [0, 0, 0, 0, 4]
         3直接指向根0
```

### Python实现

```python
class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))  # 父节点
        self.rank = [0] * size          # 树的高度（秩）

    def find(self, x: int) -> int:
        """
        查找x的根节点，带路径压缩

        时间复杂度: O(α(n)) ≈ O(1), α为反阿克曼函数
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 路径压缩
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        """
        合并x和y所在的集合，按秩合并

        时间复杂度: O(α(n)) ≈ O(1)
        """
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


def count_connected_components(n: int, edges: list) -> int:
    """
    应用：统计连通分量数量
    n: 顶点数
    edges: 边列表 [(u, v), ...]
    """
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)

    roots = set()
    for i in range(n):
        roots.add(uf.find(i))
    return len(roots)
```

---

## 6. 考研重点 & 易错点

### 高频考点

| 考点 | 关键要点 |
|------|---------|
| **二叉树性质** | n₀ = n₂ + 1 是必考点 |
| **遍历顺序** | 先、中、后序的区别和还原 |
| **哈夫曼树** | 构建过程、WPL计算、编码生成 |
| **并查集** | 路径压缩、按秩合并 |

### 易错点

| 易错点 | 正确做法 |
|--------|---------|
| n₀ = n₂ + 1 | 只适用于非空二叉树 |
| 线索二叉树标志位 | 0表示孩子指针，1表示线索 |
| 哈夫曼树 | 左0右1编码是约定，可互换 |
| 并查集未优化 | 时间复杂度O(n)，优化后接近O(1) |

### 应用场景

| 场景 | 数据结构 | 原因 |
|------|----------|------|
| 表达式树 | 二叉树 | 自然表示运算层次 |
| 文件系统 | 树 | 层次结构 |
| 数据压缩 | 哈夫曼树 | 最优前缀编码 |
| 连通性问题 | 并查集 | 高效合并查询 |
| 线性遍历二叉树 | 线索二叉树 | 无需递归或栈 |

---

## 7. 复杂度总结表

| 操作 | 时间复杂度 | 空间复杂度 |
|------|-----------|-----------|
| 二叉树递归遍历 | O(n) | O(h)栈空间 |
| 二叉树非递归遍历 | O(n) | O(n) |
| 层序遍历 | O(n) | O(n)队列 |
| 哈夫曼树构建 | O(nlogn) | O(n) |
| 并查集查找(未优化) | O(h) | O(1) |
| 并查集查找(路径压缩) | O(α(n))≈O(1) | O(1) |
| 并查集合并 | O(α(n))≈O(1) | O(1) |

---

## 📝 完整代码示例

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def preorder_traversal(root: TreeNode) -> list:
    """先序遍历"""
    result = []

    def dfs(node):
        if not node:
            return
        result.append(node.val)
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return result


def inorder_traversal(root: TreeNode) -> list:
    """中序遍历"""
    result = []

    def dfs(node):
        if not node:
            return
        dfs(node.left)
        result.append(node.val)
        dfs(node.right)

    dfs(root)
    return result


def level_order_traversal(root: TreeNode) -> list:
    """层序遍历"""
    if not root:
        return []

    result = []
    from collections import deque
    queue = deque([root])

    while queue:
        node = queue.popleft()
        result.append(node.val)

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return result


if __name__ == "__main__":
    # 构建示例二叉树
    #        A
    #       / \
    #      B   C
    #     / \   \
    #    D   E   F
    root = TreeNode('A',
                 TreeNode('B',
                          TreeNode('D'),
                          TreeNode('E')),
                 TreeNode('C',
                          None,
                          TreeNode('F')))

    print("=" * 40)
    print("二叉树遍历测试")
    print("=" * 40)
    print(f"先序遍历: {preorder_traversal(root)}")
    print(f"中序遍历: {inorder_traversal(root)}")
    print(f"层序遍历: {level_order_traversal(root)}")
```
