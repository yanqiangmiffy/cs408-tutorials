# 第7章 查找

> 查找的核心是“如何更快定位目标元素”。408 里最重要的是顺序查找、折半查找、BST / AVL 和散列表；B树、B+树更偏磁盘索引结构与综合题。

---

## 1. 顺序查找 <a id="sequential"></a>

**核心思想**：从头到尾逐个比较，找到目标就返回，否则遍历完整个表。

**适用场景**：
- 表无序
- 元素数量不大
- 只查几次，不值得额外建索引

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

**核心思想**：要求表必须有序。每次取中点比较，把查找区间缩小一半。

**重点**：
- 只能用于**有序顺序表**
- 不能直接用于链表，因为链表无法 `O(1)` 访问中间元素

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

**核心思想**：块间有序，块内无序。先在索引表中定位块，再在块内顺序查找。

**适合记忆的结构**：
- 第一步：查索引
- 第二步：查块内

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

### 4.1 查找

从根开始：
- 比根小，往左
- 比根大，往右
- 相等则找到

### 4.2 删除三种情况

1. 删除叶子结点：直接删
2. 删除只有一个孩子的结点：孩子顶上来
3. 删除有两个孩子的结点：用中序后继或前驱替换，再删除后继/前驱

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

            succ = node.right
            while succ.left:
                succ = succ.left
            node.key = succ.key
            node.right = self._delete(node.right, succ.key)
        return node
```

---

## 5. 平衡二叉树 AVL <a id="avl"></a>

**核心思想**：AVL 是“严格平衡”的 BST。任意结点左右子树高度差不超过 1。

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

**核心思想**：B树是多路平衡查找树，适合减少磁盘 I/O。内部结点可以有多个关键字和多个孩子。

**考研记忆点**：
- 所有叶子在同一层
- 一个结点可存多个关键字
- 结点分裂后中间关键字上移

下面这个仓库里的代码文件提供了可运行的教学实现：
- [code/7_search/7_4_btree.py](G:\Projects\cs408-tutorials\code\7_search\7_4_btree.py)

```python
tree = BTree(order=3)
for key in [50, 30, 70, 20, 40, 60, 80]:
    tree.insert(key)
print(tree.search(60))  # True
```

---

## 7. B+树 <a id="bplustree"></a>

**核心思想**：
- 内部结点只做索引
- 所有真实数据都放在叶子结点
- 叶子结点之间有链表，适合范围查询

**和 B 树的区别**：
- B树：内部结点也可能存放实际记录
- B+树：内部结点只存索引键，叶子结点串成链表

本项目当前采用的是**教学型实现**：对外行为正确，支持插入、查找、删除、范围查询；为了让演示稳定可验证，插入和删除后会重建索引层，而不是追求工业级增量分裂实现。

```python
tree = BPlusTree(order=3)
for key in [50, 30, 70, 20, 40, 60, 80]:
    tree.insert(key)

print(tree.search(40))          # True
print(tree.range_search(35, 70))  # [40, 50, 60, 70]
```

---

## 8. 散列表 <a id="hash"></a>

**核心思想**：通过哈希函数直接计算存储位置，平均查找效率可以达到 `O(1)`。

### 常见哈希函数

- 直接定址法
- 除留余数法：`H(key) = key % p`

### 常见冲突处理

- 线性探测
- 二次探测
- 拉链法

### 装填因子

`α = n / m`

- `n`：表中已有元素数
- `m`：散列表长度

装填因子越大，冲突通常越多，查找效率越差。

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
