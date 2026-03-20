# 408考研 · 树与二叉树总结

> 本文档包含树与二叉树的完整总结，涵盖二叉树遍历、线索二叉树、哈夫曼树和并查集的算法思想、手写遍历过程和 Python 实现。适合 408 考研数据结构复习使用。

---

## 📊 知识点总览

| 编号 | 内容 | 文件 |
|------|------|------|
| 5.3 | 二叉树的遍历(先/中/后/层序) + 由序列构造 | `5_3_binary_tree_traversal.py` |
| 5.3.2 | 线索二叉树 | `5_3_threaded_binary_tree.py` |
| 5.5.1 | 哈夫曼树与哈夫曼编码 | `5_5_huffman_tree.py` |
| 5.5.2 | 并查集 | `5_5_union_find.py` |

---

## 1. 二叉树的遍历

**核心思想**：按照不同的访问根节点的顺序，分为先序(根左右)、中序(左根右)、后序(左右根)和层序(逐层)四种遍历方式。

### 遍历顺序助记

| 遍历方式 | 顺序 | 助记 |
|----------|------|------|
| 先序 (Pre) | 根 → 左 → 右 | NLR |
| 中序 (In) | 左 → 根 → 右 | LNR |
| 后序 (Post) | 左 → 右 → 根 | LRN |
| 层序 (Level) | 逐层从左到右 | 用队列 |

**手写遍历过程**（示例二叉树）：

```
          A
         / \
        B   C
       / \   \
      D   E   F

先序 (根左右): A → B → D → E → C → F
中序 (左根右): D → B → E → A → C → F
后序 (左右根): D → E → B → F → C → A
层序 (逐层):   A → B → C → D → E → F
```

**先序遍历手写详细过程**：

```
访问 A (根)
  ├─ 访问 B (A的左)
  │   ├─ 访问 D (B的左)
  │   │   ├─ D无左 → 回
  │   │   └─ D无右 → 回
  │   └─ 访问 E (B的右)
  │       ├─ E无左 → 回
  │       └─ E无右 → 回
  └─ 访问 C (A的右)
      ├─ C无左 → 回
      └─ 访问 F (C的右)

结果: A B D E C F
```

**层序遍历手写过程**（使用队列）：

```
步骤    出队    入队        队列状态
初始                        [A]
1       A       B, C        [B, C]
2       B       D, E        [C, D, E]
3       C       F           [D, E, F]
4       D       无          [E, F]
5       E       无          [F]
6       F       无          []

结果: A B C D E F
```

**Python 实现**：

```python
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

# === 递归遍历 ===
def preorder(root):
    """先序: 根左右"""
    if root is None:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)

def inorder(root):
    """中序: 左根右"""
    if root is None:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

def postorder(root):
    """后序: 左右根"""
    if root is None:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]

# === 非递归中序 (用栈) ===
def inorder_iterative(root):
    """中序非递归: 一路向左到底，弹出，转向右"""
    result, stack = [], []
    cur = root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left     # 一路左到底
        cur = stack.pop()
        result.append(cur.val) # 访问
        cur = cur.right         # 转向右子树
    return result

# === 层序遍历 (用队列) ===
from collections import deque
def level_order(root):
    if not root:
        return []
    result, queue = [], deque([root])
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

## 2. 由遍历序列构造二叉树

**核心思想**：**必须有中序**！中序 + (先序/后序/层序) → 唯一确定一棵二叉树。

**手写构造过程**（先序: `ABDECF`，中序: `DBEACF`）：

```
步骤1: 先序首元素 A 是根
       中序中 A 左边 = 左子树{D,B,E}  右边 = 右子树{C,F}

步骤2: 左子树先序 BDE → 根=B
       中序 DBE → B左={D}  B右={E}

步骤3: 右子树先序 CF → 根=C
       中序 CF → C左=∅  C右={F}

结果:      A
          / \
         B   C
        / \   \
       D   E   F
```

**Python 实现**：

```python
def build_from_preorder_inorder(preorder_seq, inorder_seq):
    """由先序+中序构造二叉树"""
    if not preorder_seq:
        return None
    root_val = preorder_seq[0]
    root = TreeNode(root_val)
    idx = inorder_seq.index(root_val)
    root.left = build_from_preorder_inorder(
        preorder_seq[1:1+idx], inorder_seq[:idx])
    root.right = build_from_preorder_inorder(
        preorder_seq[1+idx:], inorder_seq[idx+1:])
    return root
```

---

## 3. 线索二叉树

**核心思想**：利用二叉树中 **n+1 个空指针域**存储前驱/后继信息。左空指向前驱，右空指向后继。通过 `ltag` 和 `rtag` 区分是孩子还是线索。

**手写中序线索化**：

```
原始二叉树:          中序序列: D B E A C F
      A
     / \
    B   C               中序线索二叉树:
   / \   \
  D   E   F         D的right→B (后继)    ltag=1 rtag=1
                    B: 有左右孩子          ltag=0 rtag=0
                    E的left→B, right→A    ltag=1 rtag=1
                    A: 有左右孩子          ltag=0 rtag=0
                    C的left→A (前驱)      ltag=1 rtag=0
                    F的left→C (前驱)      ltag=1 rtag=1

tag=0: 指向孩子    tag=1: 指向线索(前驱/后继)
```

---

## 4. 哈夫曼树与哈夫曼编码

**核心思想**：给定 n 个权值，构造一棵带权路径长度 (WPL) 最小的二叉树。每次取两个最小的合并，合并值作为新节点的权值。

**手写构造过程**（权值: `{A:5, B:2, C:4, D:1, E:7}`）：

```
初始权值: 5, 2, 4, 1, 7

第1步: 取最小两个 1, 2 → 合并为 3
       剩余: 5, 4, 3, 7

第2步: 取最小两个 3, 4 → 合并为 7
       剩余: 5, 7, 7

第3步: 取最小两个 5, 7 → 合并为 12
       剩余: 7, 12

第4步: 取最小两个 7, 12 → 合并为 19
       剩余: 19 (根)

哈夫曼树:
            19
           /  \
          12    E(7)
         / \
        7   A(5)
       / \
      3   C(4)
     / \
    D(1) B(2)

WPL = 7×1 + 5×2 + 4×2 + 2×3 + 1×3
    = 7 + 10 + 8 + 6 + 3 = 34

哈夫曼编码 (左0右1):
  E: 1       (1位)
  A: 01      (2位)
  C: 001     (3位→实际为01)
  B: 0001    (4位)
  D: 0000    (4位)
```

> **性质**: n 个叶子节点 → 2n-1 个节点，不存在度为1的节点

**Python 实现**：

```python
import heapq

def build_huffman(weights):
    """构建哈夫曼树, weights = [(weight, char), ...]"""
    heap = [(w, c) for w, c in weights]
    heapq.heapify(heap)
    while len(heap) > 1:
        w1, c1 = heapq.heappop(heap)
        w2, c2 = heapq.heappop(heap)
        heapq.heappush(heap, (w1 + w2, c1 + c2))
    return heap[0]
```

---

## 5. 并查集 (Union-Find)

**核心思想**：用**树的双亲表示法**（数组）实现集合的合并 (Union) 和查找 (Find)。按秩合并 + 路径压缩优化后，单次操作近似 O(1)。

**手写操作过程**（初始: {0}, {1}, {2}, {3}, {4}）：

```
初始: parent = [-1, -1, -1, -1, -1]  (每个元素自成一棵树)

Union(0, 1):  parent = [-1, 0, -1, -1, -1]   1→0
Union(2, 3):  parent = [-1, 0, -1, 2, -1]    3→2
Union(0, 2):  parent = [-1, 0, 0, 2, -1]     2→0 (合并两棵树)
Union(4, 3):  parent = [-1, 0, 0, 2, 0]      Find(3)=0, 4→0

树结构:
      0
    / | \
   1  2  4
      |
      3

Find(3): 3→2→0  (路径压缩后: 3→0)
```

**Python 实现**：

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        """路径压缩"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """按秩合并"""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
```

---

## 🧠 考研重点速记

### 遍历
- **先序**: 根左右 (NLR)；**中序**: 左根右 (LNR)；**后序**: 左右根 (LRN)
- **非递归后序**: 改造先序为根右左 → 反转得到左右根
- **层序**: 用队列实现

### 序列构造
- **必须有中序**！先序/后序/层序 + 中序 → 唯一确定
- 先序第一个元素是根，后序最后一个元素是根

### 线索二叉树
- 利用 **n+1 个空指针域**存前驱后继
- `ltag=0` 左孩子，`ltag=1` 前驱；`rtag=0` 右孩子，`rtag=1` 后继

### 哈夫曼树
- **WPL 最小**，n 个叶子 → 2n-1 个节点
- 没有度为 1 的节点
- 哈夫曼编码是**前缀编码**（任一编码不是另一编码的前缀）

### 并查集
- **Find + Union**，按秩合并 + 路径压缩
- 优化后单次操作近似 **O(1)**

### 二叉树性质（最常考）
- **n₀ = n₂ + 1** ← 叶子数 = 度2节点数 + 1
- 完全二叉树高度 h = ⌊log₂n⌋ + 1
- 第 i 层最多 2^(i-1) 个节点

---

## 📁 文件结构

```
5_tree/
├── README.md                         # 本文档
├── 5_3_binary_tree_traversal.py      # 二叉树遍历
├── 5_3_threaded_binary_tree.py       # 线索二叉树
├── 5_5_huffman_tree.py               # 哈夫曼树
└── 5_5_union_find.py                 # 并查集
```

每个 Python 文件包含：
- 📝 算法说明文档字符串
- ⚡ 标准实现函数
- 🔍 带详细输出的 verbose 版本
- ✍️ 手写过程模拟
- ✅ 测试用例

运行示例：
```bash
python 5_tree/5_3_binary_tree_traversal.py
python 5_tree/5_3_threaded_binary_tree.py
python 5_tree/5_5_huffman_tree.py
python 5_tree/5_5_union_find.py
```
