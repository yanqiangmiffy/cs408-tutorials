# 第7章 查找

> 查找的目标是“在尽量少的比较次数下定位目标元素”。408 里最核心的内容是顺序查找、折半查找、BST、AVL 和散列表；B树、B+树则更偏向综合题和外存索引结构。

---

## 1. 顺序查找 <a id="sequential"></a>

**核心思想**：从头到尾逐个比较，找到目标就返回，否则遍历完整个表。

**适用场景**：
- 表无序
- 元素数量不大
- 查找次数少，不值得专门建立索引

**ASL（平均查找长度）**：
- 成功：`(n + 1) / 2`
- 失败：`n`

```python
def sequential_search(arr: list[int], key: int) -> int:
    for i, value in enumerate(arr):
        if value == key:
            return i
    return -1
```

---

## 2. 折半查找 <a id="binary"></a>

**核心思想**：要求表必须有序。每次取中间元素比较，将查找区间缩小一半。

**重点**：
- 只能用于**有序顺序表**
- 不能直接用于链表，因为链表无法 `O(1)` 访问中间位置

```python
def binary_search(arr: list[int], key: int) -> int:
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == key:
            return mid
        if arr[mid] < key:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

**复杂度**：
- 时间复杂度：`O(log n)`
- 空间复杂度：`O(1)`

---

## 3. 分块查找 <a id="block"></a>

**核心思想**：块间有序，块内无序。先通过索引表找到目标块，再在块内顺序查找。

**步骤**：
1. 先在索引表中定位块
2. 再在块内顺序比较

```python
def block_search(blocks: list[list[int]], block_index: list[int], key: int) -> int:
    low, high = 0, len(block_index) - 1
    block_id = -1

    while low <= high:
        mid = (low + high) // 2
        if key <= block_index[mid]:
            block_id = mid
            high = mid - 1
        else:
            low = mid + 1

    if block_id == -1:
        return -1

    offset = sum(len(block) for block in blocks[:block_id])
    for i, value in enumerate(blocks[block_id]):
        if value == key:
            return offset + i
    return -1
```

---

## 4. 二叉排序树 BST <a id="bst"></a>

**性质**：左子树所有关键字 `< 根 <` 右子树所有关键字。

### 4.1 查找思路

从根开始：
- 比根小，往左
- 比根大，往右
- 相等则找到

### 4.2 删除三种情况

1. 删除叶子结点：直接删
2. 删除只有一个孩子的结点：孩子顶上来
3. 删除有两个孩子的结点：用中序后继替换，再删除后继

```python
class BSTNode:
    def __init__(self, key: int):
        self.key = key
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, key: int) -> None:
        self.root = self._insert(self.root, key)

    def _insert(self, node, key: int):
        if node is None:
            return BSTNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        return node

    def search(self, key: int) -> bool:
        node = self.root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def delete(self, key: int) -> None:
        self.root = self._delete(self.root, key)

    def _delete(self, node, key: int):
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            successor = node.right
            while successor.left:
                successor = successor.left
            node.key = successor.key
            node.right = self._delete(node.right, successor.key)

        return node
```

---

## 5. 平衡二叉树 AVL <a id="avl"></a>

**核心思想**：AVL 是严格平衡的 BST。任意结点左右子树高度差不超过 1。

### 四种失衡与调整

- `LL`：右旋
- `RR`：左旋
- `LR`：先左旋左子树，再右旋
- `RL`：先右旋右子树，再左旋

```python
class AVLNode:
    def __init__(self, key: int):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


def height(node) -> int:
    return node.height if node else 0


def update_height(node) -> None:
    node.height = max(height(node.left), height(node.right)) + 1


def balance_factor(node) -> int:
    return height(node.left) - height(node.right)


def rotate_right(y):
    x = y.left
    t2 = x.right
    x.right = y
    y.left = t2
    update_height(y)
    update_height(x)
    return x


def rotate_left(x):
    y = x.right
    t2 = y.left
    y.left = x
    x.right = t2
    update_height(x)
    update_height(y)
    return y
```

**复杂度**：
- 查找：`O(log n)`
- 插入：`O(log n)`
- 删除：`O(log n)`

---

## 6. B树 <a id="btree"></a>

**核心思想**：B树是多路平衡查找树。一个结点里可以存多个关键字，孩子数也不止两个，所以树高比 BST 更低，更适合磁盘块存储。

### 6.1 为什么 B树适合外存查找

BST 一个结点往往只存一个关键字，结点多了以后树会长高。  
B树把多个关键字放进同一个结点里，一次磁盘 I/O 读入一个块后，就能在块内完成多次比较，整体查找层数更少。

例如 3 阶 B树：

```text
        [30 | 60]
       /    |    \
   [10 20] [40] [70 80]
```

查找 `40` 的过程：
- 在根结点中比较，发现 `30 < 40 < 60`
- 进入中间孩子
- 在结点 `[40]` 中找到目标

### 6.2 B树插入要点

- 叶子没满：直接插入
- 叶子满了：分裂成左右两个结点
- 中间关键字上移到父结点
- 如果父结点也满，则继续向上分裂
- 根结点分裂时，整棵树高度加 1

### 6.3 教学版 B树实现

下面这段代码是适合博客正文阅读的版本，支持查找、插入和简化删除。  
删除为了便于讲清原理，采用“中序结果重建”的写法，牺牲效率来换可读性。

```python
from typing import Optional


class BTreeNode:
    def __init__(self, is_leaf: bool = False):
        self.is_leaf = is_leaf
        self.keys: list[int] = []
        self.children: list["BTreeNode"] = []


class BTree:
    def __init__(self, order: int = 3):
        self.order = order
        self.max_keys = order - 1
        self.root: Optional[BTreeNode] = None

    def search(self, key: int) -> bool:
        return self._search(self.root, key)

    def _search(self, node: Optional[BTreeNode], key: int) -> bool:
        if node is None:
            return False

        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return True

        if node.is_leaf:
            return False

        return self._search(node.children[i], key)

    def insert(self, key: int) -> None:
        if self.root is None:
            self.root = BTreeNode(True)
            self.root.keys.append(key)
            return

        up_key, new_child = self._insert(self.root, key)
        if up_key is not None:
            new_root = BTreeNode(False)
            new_root.keys = [up_key]
            new_root.children = [self.root, new_child]
            self.root = new_root

    def _insert(self, node: BTreeNode, key: int):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return None, None

        if node.is_leaf:
            node.keys.insert(i, key)
        else:
            up_key, new_child = self._insert(node.children[i], key)
            if up_key is None:
                return None, None
            node.keys.insert(i, up_key)
            node.children.insert(i + 1, new_child)

        if len(node.keys) > self.max_keys:
            return self._split(node)

        return None, None

    def _split(self, node: BTreeNode):
        mid = len(node.keys) // 2
        up_key = node.keys[mid]

        right = BTreeNode(node.is_leaf)
        right.keys = node.keys[mid + 1:]
        node.keys = node.keys[:mid]

        if not node.is_leaf:
            right.children = node.children[mid + 1:]
            node.children = node.children[:mid + 1]

        return up_key, right

    def inorder(self) -> list[int]:
        result: list[int] = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[BTreeNode], result: list[int]) -> None:
        if node is None:
            return
        if node.is_leaf:
            result.extend(node.keys)
            return

        for i, key in enumerate(node.keys):
            self._inorder(node.children[i], result)
            result.append(key)
        self._inorder(node.children[-1], result)

    def delete(self, key: int) -> bool:
        values = self.inorder()
        if key not in values:
            return False
        values.remove(key)
        self.root = None
        for value in values:
            self.insert(value)
        return True


tree = BTree(order=3)
for value in [50, 30, 70, 20, 40, 60, 80]:
    tree.insert(value)

print(tree.search(40))   # True
print(tree.search(25))   # False
print(tree.inorder())    # [20, 30, 40, 50, 60, 70, 80]
```

---

## 7. B+树 <a id="bplustree"></a>

**核心思想**：
- 内部结点只存索引键
- 所有真实数据都存放在叶子结点
- 叶子结点之间用链表连接起来，方便范围查询

### 7.1 B+树为什么适合范围查询

假设叶子层长这样：

```text
[10 20] -> [25 30] -> [35 40] -> [45 50] -> [60 70]
```

如果要查询区间 `[35, 70]`：
- 先找到包含 `35` 的叶子
- 然后顺着叶子链表往后扫
- 遇到大于 `70` 的值就停止

所以 B+树在数据库、文件系统这类“查一个范围”的场景里很常见。

### 7.2 B+树和 B树的区别

| 对比项 | B树 | B+树 |
|------|------|------|
| 内部结点 | 可能存实际记录 | 只存索引 |
| 叶子结点 | 不一定连成链表 | 通常连成链表 |
| 范围查询 | 一般 | 更适合 |
| 数据分布 | 分散在整棵树 | 集中在叶子层 |

### 7.3 教学版 B+树实现

下面这版代码强调“博客里可读、行为稳定”。  
为了避免把篇幅耗在复杂分裂边界上，这里采用“插入和删除后重建索引层”的教学写法，但从查找模型上看，它依然保留了 B+树最重要的两个特点：**内部结点只做索引**、**叶子结点顺序链表支持范围查询**。

```python
from typing import Optional


class BPlusTreeNode:
    def __init__(self, is_leaf: bool = False):
        self.is_leaf = is_leaf
        self.keys: list[int] = []
        self.children: list["BPlusTreeNode"] = []
        self.next: Optional["BPlusTreeNode"] = None


class BPlusTree:
    def __init__(self, order: int = 3):
        self.order = order
        self.max_keys = order - 1
        self.root: Optional[BPlusTreeNode] = None
        self.leaf_head: Optional[BPlusTreeNode] = None
        self.values: list[int] = []

    def insert(self, key: int) -> None:
        if key in self.values:
            return
        self.values.append(key)
        self.values.sort()
        self._rebuild()

    def delete(self, key: int) -> bool:
        if key not in self.values:
            return False
        self.values.remove(key)
        self._rebuild()
        return True

    def search(self, key: int) -> bool:
        leaf = self._find_leaf(key)
        return leaf is not None and key in leaf.keys

    def range_search(self, left: int, right: int) -> list[int]:
        result: list[int] = []
        leaf = self._find_leaf(left)
        while leaf:
            for key in leaf.keys:
                if left <= key <= right:
                    result.append(key)
                elif key > right:
                    return result
            leaf = leaf.next
        return result

    def _find_leaf(self, key: int) -> Optional[BPlusTreeNode]:
        node = self.root
        if node is None:
            return None

        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]
        return node

    def _rebuild(self) -> None:
        if not self.values:
            self.root = None
            self.leaf_head = None
            return

        leaves: list[BPlusTreeNode] = []
        for i in range(0, len(self.values), self.max_keys):
            leaf = BPlusTreeNode(True)
            leaf.keys = self.values[i:i + self.max_keys]
            if leaves:
                leaves[-1].next = leaf
            leaves.append(leaf)

        self.leaf_head = leaves[0]
        self.root = self._build_index(leaves)

    def _build_index(self, nodes: list[BPlusTreeNode]) -> BPlusTreeNode:
        level = nodes
        while len(level) > 1:
            next_level: list[BPlusTreeNode] = []
            for i in range(0, len(level), self.order):
                children = level[i:i + self.order]
                parent = BPlusTreeNode(False)
                parent.children = children
                parent.keys = [self._first_key(child) for child in children[1:]]
                next_level.append(parent)
            level = next_level
        return level[0]

    def _first_key(self, node: BPlusTreeNode) -> int:
        while not node.is_leaf:
            node = node.children[0]
        return node.keys[0]


tree = BPlusTree(order=3)
for value in [50, 30, 70, 20, 40, 60, 80, 25, 35, 45]:
    tree.insert(value)

print(tree.search(40))            # True
print(tree.search(65))            # False
print(tree.range_search(35, 70))  # [35, 40, 45, 50, 60, 70]
```

### 7.4 应试要点

- B树重点记“分裂”和“中间关键字上移”
- B+树重点记“叶子链表”和“范围查询”
- 两者都是**多路平衡查找树**
- 它们高度都比较低，适合磁盘块组织

---

## 8. 散列表 <a id="hash"></a>

**核心思想**：通过哈希函数直接计算存储位置，平均查找效率可达 `O(1)`。

### 常见哈希函数

- 直接定址法
- 除留余数法：`H(key) = key % p`

### 常见冲突处理

- 线性探测
- 二次探测
- 拉链法

### 装填因子

`α = n / m`

- `n`：表中已有元素个数
- `m`：散列表长度

装填因子越大，冲突通常越多，查找效率越低。

```python
class LinearProbingHashTable:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.table = [None] * capacity

    def insert(self, key: int) -> bool:
        idx = key % self.capacity
        start = idx
        while self.table[idx] is not None:
            if self.table[idx] == key:
                return False
            idx = (idx + 1) % self.capacity
            if idx == start:
                return False
        self.table[idx] = key
        return True

    def search(self, key: int) -> int:
        idx = key % self.capacity
        start = idx
        while self.table[idx] is not None:
            if self.table[idx] == key:
                return idx
            idx = (idx + 1) % self.capacity
            if idx == start:
                break
        return -1
```

---

## 9. 复杂度总结 <a id="summary"></a>

| 方法 | 平均时间复杂度 | 最坏时间复杂度 | 空间复杂度 |
|------|----------------|----------------|-----------|
| 顺序查找 | `O(n)` | `O(n)` | `O(1)` |
| 折半查找 | `O(log n)` | `O(log n)` | `O(1)` |
| 分块查找 | `O(√n)` | `O(n)` | `O(1)` |
| BST | `O(log n)` | `O(n)` | `O(n)` |
| AVL | `O(log n)` | `O(log n)` | `O(n)` |
| B树 | `O(log_m n)` | `O(log_m n)` | `O(n)` |
| B+树 | `O(log_m n)` | `O(log_m n)` | `O(n)` |
| 散列表 | `O(1)` | `O(n)` | `O(m)` |

## 10. 考研易错点

- 折半查找只能用于**有序顺序表**
- BST 删除有两个孩子的结点时，常用**中序后继**替换
- AVL 的 `LR` 和 `RL` 需要两次旋转
- 散列表的 `O(1)` 是**平均复杂度**，不是最坏复杂度
- B+树做范围查询时，优势来自**叶子链表**

## 11. 常考题型与相关算法题

### 常考点

- 折半查找判定树、ASL 的计算。
- BST 的插入、删除三种情况和中序有序性。
- AVL 的 `LL / RR / LR / RL` 四类失衡与旋转。
- 散列表装填因子、冲突处理和平均查找长度。
- B树与 B+树在范围查询、磁盘友好性上的差异。

### 相关算法题

| 题目 | 训练点 |
|------|--------|
| [37 数字在排序数组中出现的次数](/coding-interview-offer/37) | 折半查找边界 |
| LeetCode 704. 二分查找 | 二分模板 |
| LeetCode 700. 二叉搜索树中的搜索 | BST 查询 |
| LeetCode 98. 验证二叉搜索树 | BST 性质 |
| LeetCode 450. 删除二叉搜索树中的节点 | BST 删除 |
| LeetCode 706. 设计哈希映射 | 散列表实现 |
