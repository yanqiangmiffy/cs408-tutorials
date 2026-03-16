# 408考研 · 查找算法总结

> 本文档包含查找算法的完整总结，涵盖顺序查找、折半查找、分块查找、BST、B树、B+树、AVL树和散列表的算法思想、ASL分析、手写查找过程和 Python 实现。适合 408 考研数据结构复习使用。

---

## 📊 算法对比总览

| 算法 | 时间复杂度 | 适用条件 | ASL(成功) |
|------|-----------|---------|-----------|
| 顺序查找 | O(n) | 任意线性表 | (n+1)/2 |
| 折半查找 | O(log n) | 有序**顺序表** | ≈log₂(n+1)-1 |
| 分块查找 | O(√n) | 块间有序 | ≈log₂(s+1)+(t+1)/2 |
| BST | 平均 O(log n) | 动态查找 | 取决于树形 |
| AVL | O(log n) | 动态查找 | ≈log₂n |
| B树 | O(logₘn) | 关键字集合 | O(logₘn) |
| B+树 | O(logₘn) | 关键字集合 | O(logₘn) |
| 散列表 | 近似 O(1) | 关键字集合 | 取决于装填因子 |

---

## 1. 顺序查找 (Sequential Search)

**核心思想**：从头到尾逐个比较，找到就返回。最简单但效率最低。

**关键步骤**：
1. 从第一个元素开始逐个比较
2. 找到返回下标，否则返回 -1
3. 带哨兵版本：将 key 放在 arr[0]，从后往前找，免去越界检查

**手写查找过程**（在 `[5, 3, 8, 1, 9, 2]` 中查找 8）：

```
arr = [5, 3, 8, 1, 9, 2]

比较次数:
  arr[0]=5 ≠ 8  第1次
  arr[1]=3 ≠ 8  第2次
  arr[2]=8 = 8  第3次 → 找到! 下标=2

ASL(成功) = (1+2+3+4+5+6)/6 = 21/6 = 3.5 = (n+1)/2
ASL(失败) = n+1 = 7 (带哨兵) 或 n = 6
```

**ASL公式**：
- 查找成功：ASL = (n+1)/2
- 查找失败：ASL = n+1 (带哨兵) 或 n (不带哨兵)

**Python 实现**：

```python
def sequential_search(arr, key):
    """顺序查找 O(n)"""
    for i in range(len(arr)):
        if arr[i] == key:
            return i
    return -1


def sequential_search_sentinel(arr, key):
    """带哨兵的顺序查找"""
    arr_copy = [key] + arr  # arr_copy[0] = 哨兵
    i = len(arr_copy) - 1
    while arr_copy[i] != key:
        i -= 1
    return i - 1 if i > 0 else -1  # 返回在原数组中的下标
```

---

## 2. 折半查找 (Binary Search)

**核心思想**：在**有序顺序表**中，每次将查找范围缩小一半。比较 mid 元素与 key，相等返回，大则左半，小则右半。

**关键步骤**：
1. `low=0, high=n-1`
2. `mid = (low + high) // 2`
3. `arr[mid] == key` → 找到
4. `arr[mid] > key` → `high = mid - 1`（左半区）
5. `arr[mid] < key` → `low = mid + 1`（右半区）
6. `low > high` → 查找失败

**手写查找过程**（在 `[7, 10, 13, 16, 19, 29, 32, 33, 37, 41, 43]` 中查找 33）：

```
arr = [7, 10, 13, 16, 19, 29, 32, 33, 37, 41, 43]
      下标: 0   1   2   3   4   5   6   7   8   9  10

查找 33:
步骤  low  high  mid  arr[mid]  比较
1     0    10    5    29        29<33 → 右半, low=6
2     6    10    8    37        37>33 → 左半, high=7
3     6    7     6    32        32<33 → 右半, low=7
4     6    7     6    33        33==33 ✓ 中!

共比较 4 次
```

**手写查找过程**（查找 20 — 失败）：

```
查找 20:
步骤  low  high  mid  arr[mid]  比较
1     0    10    5    29        29>20 → 左半, high=4
2     0    4     2    13        13<20 → 右半, low=3
3     3    4     3    16        16<20 → 右半, low=4
4     4    4     4    19        19<20 → 右半, low=5
      low=5 > high=4 → 查找失败 ✗
```

**折半查找判定树**（n=11）：

```
                 19(4)
               /      \
           10(1)        33(7)
          /    \       /    \
        7(0)  13(2)  29(5) 41(9)
           \     \      \    / \
          10(1)  16(3)  32(6) 37(8) 43(10)

ASL(成功) = (1×1 + 2×2 + 3×4 + 4×4) / 11 = 33/11 = 3.0
ASL(失败) = (3×4 + 4×8) / 12 = 44/12 ≈ 3.67
```

> ⚠️ 折半查找**仅适用于有序顺序表**（不能是链表！因为链表无法 O(1) 访问 mid）

**Python 实现**：

```python
def binary_search(arr, key):
    """折半查找 O(log n) — 仅适用有序顺序表"""
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == key:
            return mid
        elif arr[mid] > key:
            high = mid - 1
        else:
            low = mid + 1
    return -1
```

---

## 3. 分块查找 (Block Search)

**核心思想**：将线性表分成若干块，**块间有序**（前块最大 ≤ 后块最小），块内无序。先在索引表折半确定块号，再在块内顺序查找。

**优势**：不需要全部元素有序，只需块间有序。

**手写查找过程**（在分块表中查找 38）：

```
索引表: [22, 44, 74]
块0: [22, 12, 13, 8, 9]    最大=22
块1: [33, 42, 44, 38, 24]  最大=44
块2: [48, 60, 58, 74, 57]  最大=74

查找 38:
第1步 索引表折半: 38 > 22, 38 ≤ 44 → 第1块
第2步 块1内顺序: 33≠38, 42≠38, 44≠38, 38=38 → 找到! ✓

ASL ≈ log₂(s+1) + (t+1)/2
s = 块数, t = 每块元素数
当 s = √n 时 ASL 最小 ≈ √n + 1
```

**Python 实现**：

```python
def block_search(blocks, block_index, key):
    """分块查找: 索引表折半 + 块内顺序"""
    # 索引表折半查找
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

    # 块内顺序查找
    for i, val in enumerate(blocks[block_id]):
        if val == key:
            # 计算全局下标
            global_idx = sum(len(blocks[j]) for j in range(block_id)) + i
            return global_idx

    return -1
```

---

## 4. 二叉排序树 (BST)

**核心思想**：左子树所有节点 < 根 < 右子树所有节点。**中序遍历 = 有序序列**。查找、插入、删除平均 O(log n)，最坏 O(n)。

**手写 BST 插入过程**（依次插入 `50, 30, 70, 20, 40, 60, 80`）：

```
插入50:      50
插入30:      50        插入70:    50
            /                    /
           30                   30   70
插入70:      50        插入20:    50
            /          \                /   \
           30   70             30   70
          /                   /  \
         20                  20   70

插入20:      50        插入40:    50
            /          \                /   \
           30   70             30   70
          /                   /   / \
         20   40                  20   40  60
         20         /  /  /  \
         40        60  80
插入40:      50        插入60:    50
            /          \                /   \
           30   70             30   70 40  60
          /                   /  /  /  \
         20   40  60             40 60  80

插入60:      50        插入80:    50
            /                    /
           30   70             30   70 80

插入80:      50
            /    \
           30   70

最终:         50
            /    \
           30     70
          / \    /  \
        20  40 60 80

中序遍历: 20, 30, 40, 50, 60, 70, 80 (有序✓)
```

**手写 BST 删除过程**（删除 30）：

```
删除30 (有两个孩子):
  → 用中序前驱 20 (或后继 40) 替换 30

用前驱替换:       用后继替换:
      50                50
     /  \              /  \
    20   70           40   70
      \  /  \         /   / \
      40  60 80     20  60 80
```

**BST 删除三种情况总结**：

| 情况 | 处理方式 |
|------|---------|
| **叶子结点** | 直接删除，父指针置为 None |
| **只有一个孩子** | 用孩子替代父节点的指针 |
| **有两个孩子** | 用中序前驱/后继的值替换，再递归删除原前驱/后继 |

**Python 实现**：

```python
class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, key: int) -> None:
        """BST插入"""
        self.root = self._insert(self.root, key)

    def _insert(self, node: BSTNode, key: int) -> BSTNode:
        if not node:
            return BSTNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        return node

    def search(self, key: int) -> bool:
        """BST查找"""
        curr = self.root
        while curr:
            if key == curr.key:
                return True
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return False

    def delete(self, key: int) -> bool:
        """BST删除（三种情况）"""
        self.root = self._delete(self.root, key)
        return True

    def _delete(self, node: BSTNode, key: int) -> BSTNode:
        if not node:
            return None

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:  # 找到了
            if not node.left and not node.right:
                return None
            elif not node.left or not node.right:
                return node.left if node.left else node.right
            else:
                # 找右子树的最小值（后继）
                successor = node.right
                while successor.left:
                    successor = successor.left
                # 用后继结点替换被删结点
                node.key = successor.key
                # 删除后继结点
                node.right = self._delete(node.right, successor.key)
                return node
```

    def inorder(self) -> list:
        """中序遍历"""
        result = []
        curr = self.root
        parent = None
        while curr:
            pass
        return result
```

---

## 5. 平衡二叉树 (AVL)

**核心思想**：BST 的改进。**任意节点**左右子树高度差（平衡因子）≤ 1。不平衡时通过旋转调整。

**平衡因子**：BF = 左子树高度 - 右子树高度

| BF值 | 说明 |
|------|------|
| BF = 0 | 完美平衡 |
| BF = 1 | 左子树高1 |
| BF = -1 | 右子树高1 |
| BF ≥ 2 或 BF ≤ -2 | 不平衡，需要调整 |

**四种旋转**：

```
LL(右单旋): 在左子树的左子树插入
     A(+2)         B
    /              / \
   B              C   A
  /
 C

RR(左单旋): 在右子树的右子树插入
  A(-2)            B
  \              / \
   B            A   C
    \
     C

LR(先左后右): 在左子树的右子树插入
   A(+2)       A          C
  /           /          / \
 B           C          B   A
  \         /
   C       B

RL(先右后左): 在右子树的左子树插入
 A(-2)      A            C
  \          \          / \
 B          C        A   B
 /            \
   C              B
```

**手写 AVL 失衡调整**（依次插入 `50, 30, 20`）：

```
插入50:   50
插入30:   50(+1)     插入20:   50(+2) ← 失衡!
                                /
                               30
                                                   /
                                                  20

LL 失衡 → 右单旋:
       30
      /  \
     20   50
```

**AVL 高度 h 的最少节点**：
```
h=1:  n_min = 1, n_max = 2
h=2: n_min = 3, n_max = 4
h=3: n_min = 7, n_max = 8
h=4: n_min = 15, n_max = 16

公式: n(h) = n(h-1) + n(h-2) + 1
类似斐波那契数列
```

**Python 实现**：

```python
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

    def get_height(self, node):
        return node.height if node else 0

    def update_height(self):
        self.height = 1 + max(
            self.get_height(self.left),
            self.get_height(self.right)
        )

    def get_balance(self):
        return self.get_height(self.left) - self.get_height(self.right)


class AVLTree:
    def __init__(self):
        self.root = None

    def rotate_right(self, y: AVLNode) -> AVLNode:
        """右旋(LL型)"""
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.update_height()
        x.update_height()

        return x

    def rotate_left(self, x: AVLNode) -> AVLNode:
        """左旋(RR型)"""
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.update_height()
        y.update_height()

        return y

    def insert(self, key: int) -> None:
        """AVL插入并自动平衡"""
        self.root = self._insert(self.root, key)

    def _insert(self, node: AVLNode, key: int) -> AVLNode:
        if not node:
            return AVLNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node

        node.update_height()
        balance = node.get_balance()

        # LL型: 右旋
        if balance > 1 and key < node.left.key:
            return self.rotate_right(node)

        # RR型: 左旋
        if balance < -1 and key > node.right.key:
            return self.rotate_left(node)

        # LR型: 先左旋左子树，再右旋
        if balance > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # RL型: 先右旋右子树，再左旋
        if balance < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node
```

---

## 6. B树

**核心思想**：多路平衡查找树。所有节点（包括内部节点）的孩子数不超过 m（阶数）。所有叶子节点在同一层（平衡特性）。

**性质**：
- 树的高度为 h，关键字数 N 满足：m^h ≤ N < m^(h+1)
- h 层最多有 m^h 个节点，h+1 层至少有 2 个节点
- 树的查找效率为 O(logₘn)，其中 m 为 B树的阶数

**手写 B 树查找示例**（m=3阶 B树）：

```
B树结构（m=3）：
          [P, 50, 75]
        /      |      \
   [20, 30, 40]  [60, 70, 80]  [85, 90, 95]

查找 40:
第1层: 在根结点中查找
  20 < 40 < 50 → 找到第2个孩子指针
第2层: 在第2个子结点中查找
  40 == 40 ✓ 找到!

查找 85:
第1层: 在根结点中查找
  50 < 75 < 85 → 找到第3个孩子指针
第2层: 在第3个子结点中查找
  60 < 85 → 找到第2个孩子指针
第3层: 在第2个子结点中查找
  85 == 85 ✓ 找到!
```

**B树插入示例**（插入 82）：

```
插入 82:
第1层: 根=[P,50,75], 82<75 → 插入第1个子结点
       插入80: [P,50,75, 82, 80] [85, 90, 95]

第2层: 75=[82,80], 75>82 → 需要分裂!
       提升中值75到根结点
       树=[75], [P,50,75] [85,90, 95]
```

**B树节点分裂规则**：
- 插入后某个子结点的关键字数超过 m-1，需要分裂
- 将中间值提升到父结点
- 将剩余关键字分裂成 m/2 个子节点

**Python 实现**：

```python
class BTreeNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []     # 关键字
        self.children = []  # 子节点


class BTree:
    def __init__(self, order=3):
        self.order = order  # m路树
        self.root = None

    def search(self, key: int) -> bool:
        """B树查找"""
        return self._search(self.root, key)

    def _search(self, node: BTreeNode, key: int) -> bool:
        if not node:
            return False

        # 在当前节点中查找
        for i in range(len(node.keys)):
            if key == node.keys[i]:
                return True
            elif key < node.keys[i]:
                # 递归搜索第i个子节点
                return self._search(node.children[i], key)

        # key比所有 key 都大
        if not node.is_leaf:
            return self._search(node.children[-1], key)

        return False

    def insert(self, key: int) -> None:
        """B树插入"""
        self.root = self._insert(self.root, key)
```

---

## 7. B+树

**核心思想**：B树的变体。**所有节点（包括内部节点）的孩子数不超过 m**（不是 m+1）。

**与 B树的区别**：

| 特性 | B树 | B+树 |
|------|------|-------|
| 结点孩子数 | ≤ m | ≤ m |
| 内部结点关键字数 | k(m-1) ≤ k ≤ m | m-1（固定 m） |
| 叶子结点孩子数 | 0 | 0 |
| 树形 | 凑凑 | 完全平衡 |

**B+树查找手写示例**（m=3阶 B+树）：

```
B+树结构（m=3）:
          [50, 75, 100]
        /      |      \
   [20, 30] 40]  [60, 70] 80]

查找 70:
第1层: 在根结点中查找
  50 < 70 < 75 → 找到第2个孩子指针
第2层: 在第2个子结点中查找
  60 < 70 → 找到第2个孩子指针
第3层: 在第2个子结点中查找
  70 == 70 ✓ 找到!

查找 25:
第1层: 在根结点中查找
  25 < 50 → 找到第1个孩子指针
第2层: 在第1个子结点中查找
  25 < 30 → 超出范围，未找到 ✗
```

**B+树插入示例**（在上述树中插入 65）：

```
插入65:
第1层: 根=[50, 75, 100], 65<50 → 插入到第1个子结点
       插入40: [50, 65, 75] 40] [60, 70]
```

**B+树节点分裂规则**：
- 插入后某个子结点的关键字数等于 m
- 将中间值提升到父结点
- 将剩余关键字分裂成 m/2 个子节点

**Python 实现**：

```python
class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []     # 关键字（最多 m-1 个）
        self.children = []  # 最多 m 个孩子


class BPlusTree:
    def __init__(self, order=3):
        self.order = order
        self.root = None

    def search(self, key: int) -> bool:
        """B+树查找"""
        return self._search(self.root, key)

    def _search(self, node: BPlusTreeNode, key: int) -> bool:
        if not node:
            return False

        # 在当前结点中查找
        for i in range(len(node.keys)):
            if key == node.keys[i]:
                return True
            elif key < node.keys[i]:
                if node.is_leaf:
                    return False
                # 递归搜索第i个子结点
                return self._search(node.children[i], key)

        # key比所有 key 都大
        return False

    def insert(self, key: int) -> None:
        """B+树插入"""
        if self.root is None:
            self.root = BPlusTreeNode(True)
            self.root.keys.append(key)
            return

        self.root, overflow = self._insert(self.root, key)
        if overflow:
            self._handle_overflow()
```

    def _insert(self, node: BPlusTreeNode, key: int) -> tuple:
        """递归插入，返回(节点, 是否溢出)"""
        # 查找插入位置并插入
        # 实现略，涉及查找和分裂操作
        pass

    def _handle_overflow(self):
        """处理溢出，需要提升和分裂"""
        pass
```

---

## 8. 红黑树

**核心思想**：AVL树的一种实现，通过**红黑性质**保持平衡。

**红黑性质**（必须同时满足）：
1. 节点要么是红色，要么是黑色
2. 根结点是黑色
3. 红色节点的两个子结点都是黑色
4. 从任一结点出发，到其后代结点的所有路径上，不能有两个连续的红色结点
5. 任意红色结点，其左右子树的高度差必须相同，且每个子树的根结点是黑色

**红黑树性质图示**：

```
性质3: 黑色节点的孩子都是黑色

      B(黑)
     /     \
   R(红)  R(红)

性质4: 不能有连续两个红色

      B(黑)
     /     \
   R(红)  B(红)  ← 违反！
```

**红黑树查找复杂度**：O(log n)

**Python 实现**：（略，红黑树插入和删除逻辑复杂，408通常只考概念）

```python
class RBNode:
    def __init__(self, key, color='RED'):
        self.key = key
        self.left = None
        self.right = None
        self.color = color  # 'RED' or 'BLACK'


class RBTree:
    def __init__(self):
        self.root = None
        self.NIL = RBNode(0, 'BLACK')  # 哨兵结点

    def insert(self, key: int) -> None:
        """红黑树插入"""
        pass

    def search(self, key: int) -> bool:
        """红黑树查找"""
        pass
```

---

## 9. 散列表 (Hash Table)

**核心思想**：通过散列函数将关键字映射到存储位置，实现 O(1) 平均查找。

**装填因子**：
```
α = n / m
```
- n：已存储元素个数
- m：散列表容量
- α越小，冲突越少，查找效率越高

### 常用散列函数

- **除留余数法**: H(key) = key % p（p 取≤表长的最大素数）
- **直接定址法**: H(key) = a*key + b（不会冲突）

### 冲突处理方法

| 方法 | 思路 | 特点 |
|------|------|------|
| 拉链法 | 同义词链在一起 | 简单，删除方便 |
| 线性探测 | d₀, d₀+1, d₀+2... | 会产生堆积现象 |
| 平方探测 | d₀+1², d₀-1², d₀+2²... | 缓解堆积 |

**手写散列表构造**（拉链法，H(key) = key % 7）：

```
插入: 14, 23, 1, 9, 36, 22, 15

H(14)=0, H(23)=2, H(1)=1, H(9)=2, H(36)=1, H(22)=1, H(15)=1

散列表 (拉链法):
0: → [14]
1: → [1] → [36] → [22] → [15]
2: → [23]
3: → ∅
4: → ∅
5: → ∅
6: → ∅

ASL(成功) = (1×2 + 2×2 + 3×1 + 4×1) / 7
           = (1+1+1+2+2+3+4) / 7 = 14/7 = 2.0
```

**手写散列表构造**（线性探测，H(key) = key % 11，表长=11）：

```
插入: 19, 1, 23, 14, 55, 68

H(19)=8  → 位置8
H(1)=1   → 位置1
H(23)=1  → 冲突! 探测2,3... → 位置2
H(14)=3  → 位置3
H(55)=0  → 位置0
H(68)=2  → 冲突! 探测3(占),4 → 位置4

下标: 0    1    2    3    4    5  ... 8  ...
值:  [55] [1]  [23] [14] [68] []     [19]

ASL(成功) = (1+1+1+3+1) / 6 = 8/6 ≈ 1.33
```

**Python 实现**（拉链法）：

```python
class ChainingHashTable:
    """拉链法散列表"""
    def __init__(self, capacity=13):
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]

    def _hash(self, key: int) -> int:
        """除留余数法"""
        return key % self.capacity

    def insert(self, key: int) -> bool:
        """插入(拉链法)"""
        idx = self._hash(key)

        # 检查是否已存在
        for item in self.table[idx]:
            if item == key:
                return False

        # 插入表头
        self.table[idx].append(key)
        return True

    def search(self, key: int) -> int:
        """查找，返回位置，未找到返回-1"""
        idx = self._hash(key)
        for i, k in enumerate(self.table[idx]):
            if k == key:
                return idx, i + 1  # 位置， 比较次数
        return -1, len(self.table[idx]) + 1

    def load_factor(self) -> float:
        """装填因子"""
        n = 0
        for chain in self.table:
            n += len(chain)
        return n / self.capacity
```


class LinearProbingHashTable:
    """线性探测法散列表"""
    def __init__(self, capacity=11):
        self.capacity = capacity
        self.table = [None] * capacity
        self.DELETED = "DELETED"

    def _hash(self, key: int) -> int:
        """除留余数法"""
        return key % self.capacity

    def insert(self, key: int) -> bool:
        """插入(线性探测)"""
        idx = self._hash(key)
        start = idx

        while self.table[idx] is not None and self.table[idx] != self.DELETED:
            if self.table[idx] == key:
                return False  # 已存在
            idx = (idx + 1) % self.capacity
            if idx == start:
                return False  # 表满

        self.table[idx] = key
        return True

    def search(self, key: int) -> int:
        """查找"""
        idx = self._hash(key)
        start = idx

        while self.table[idx] is not None and self.table[idx] != self.DELETED:
            if self.table[idx] == key:
                return idx
            idx = (idx + 1) % self.capacity
            if idx == start:
                break

        return -1

    def load_factor(self) -> float:
        """装填因子"""
        n = 0
        for val in self.table:
            if val is not None and val != self.DELETED:
                n += 1
        return n / self.capacity
```

---

## 🧠 考研重点速记

### 顺序查找
- **ASL(成功)** = (n+1)/2，**ASL(失败)** = n+1
- 适用于任意线性表，无序也可

### 折半查找
- **ASL(成功)** ≈ log₂(n+1) - 1
- **仅适用于有序顺序表**（不能是链表!)
- **判定树是平衡 BST**

### 分块查找
- **块间有序** + 块内无序
- ASL ≈ log₂(s+1) + (t+1)/2

### BST
- **左 < 根 < 右**，中序 = 有序
- 删除：叶子直接删，单子女用子女替，双子女用前驱/后继替

### AVL
- 平衡因子 |BF| ≤ 1
- **四种旋转**: LL(右旋)、RR(左旋)、LR(先左后右)、RL(先右后左)
- **高度 h 的最少节点**: n(h) = n(h-1) + n(h-2) + 1

### B树
- **性质**: m^h ≤ N < m^(h+1)
- **查找复杂度**: O(logₘn)

### B+树
- **与B树区别**: 孩储的关键字数固定为 m-1
- **查找复杂度**: O(logₘn)

### 红黑树
- **5条红黑性质**：
  1. 节点红或黑
  2. 根黑色
 3. 红色孩子都是黑色
  4. 不能有两个连续红色
  5. 红色节点的两个子树高度相同，且根结点黑色

### 散列表
- **除留余数法**: H(key) = key % p（p取素数）
- **拉链法** vs **开放定址法**
- **ASL 计算**: 成功/失败分别计算，考研必考!
- **装填因子 α = 记录数/表长**，α 越大冲突越多

---

## 📁 文件结构

```
7_search/
├── README.md                  # 本文档
├── 7_2_search_algorithms.py   # 顺序/折半/分块查找
├── 7_3_bst_avl.py             # BST与AVL树
├── 7_4_btree.py               # B树与B+树
├── 7_5_hash_table.py          # 散列表
```

每个 Python 文件包含：
- 📝 算法说明文档字符串
- ⚡ 标准实现函数
- 🔍 带详细输出的 verbose 版本
- ✍️ 手写过程模拟
- ✅ 测试用例

运行示例：
```bash
python 7_search/7_2_search_algorithms.py
python 7_search/7_3_bst_avl.py
python 7_search/7_4_btree.py
python 7_search/7_5_hash_table.py
```
