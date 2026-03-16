# 第7章 查找

> 查找是计算机中的基本操作，根据给定值在数据结构中定位对应元素。掌握折半查找、BST、B树、B+树、AVL树和散列表是考研的核心内容。

---

## 1. 顺序查找 <a id="basic"></a>

**核心思想**：从第一个元素开始，逐个比较，直到找到目标或遍历完所有元素。

**手写示例**：在 `[5, 3, 8, 1, 9, 2]` 中查找 `4`

```
索引:   0   1   2   3   4   5
数组: [ 5,  3,  8,  1,  9,  2]

i=0: 5 ≠ 4, 继续
i=1: 3 ≠ 4, 继续
i=2: 8 ≠ 4, 继续
i=3: 1 ≠ 4, 继续
i=4: 9 ≠ 4, 继续
i=5: 2 ≠ 4, 继续

返回: -1 (未找到)
```

**ASL（平均查找长度）**：
- 查找成功：ASL = (n+1)/2 = (6+1)/2 = 3.5
- 查找失败：ASL = n = 6

**带哨兵的顺序查找**：将 key 放在 arr[0]，从后往前找，免去越界检查

```python
def sequential_search(arr: list, key: int) -> int:
    """
    顺序查找
    返回key的索引，未找到返回-1

    时间复杂度: O(n)
    空间复杂度: O(1)
    """
    for i, val in enumerate(arr):
        if val == key:
            return i
    return -1


def sequential_search_sentinel(arr: list, key: int) -> int:
    """
    带哨兵的顺序查找 - 省去边界检查

    时间复杂度: O(n)
    空间复杂度: O(1)
    """
    arr_copy = [key] + arr  # arr_copy[0] = 哨兵
    i = len(arr_copy) - 1
    while arr_copy[i] != key:
        i -= 1
    return i - 1 if i > 0 else -1  # 返回在原数组中的下标
```

---

## 2. 折半查找 <a id="binary"></a>

**核心思想**：在有序数组中，每次比较中间元素，缩小一半查找范围。要求有序顺序表。

**手写示例**：在 `[1, 2, 3, 5, 8, 9]` 中查找 `8`

```
数组: [1, 2, 3, 5, 8, 9]
索引:  0   1   2   3   4   5

第1轮: low=0, high=5
       mid=(0+5)//2=2, arr[2]=3
       3 < 8, low=mid+1=3

第2轮: low=3, high=5
       mid=(3+5)//2=4, arr[4]=8
       8 == 8 ✓ 找到！

返回: 4
```

**手写示例**：在 `[1, 2, 3, 5, 8, 9]` 中查找 `4`

```
第1轮: low=0, high=5, mid=2, arr[2]=3
       3 < 4, low=3

第2轮: low=3, high=5, mid=4, arr[4]=8
       8 > 4, high=3

第3轮: low=3, high=3, mid=3, arr[3]=5
       5 > 4, high=2

第4轮: low=3 > high=2, 退出循环

返回: -1 (未找到)
```

**判定折半查找树**（n=6）：

```
         5
       / \
      3     8
     / \   /
    1   5   9

ASL(成功) ≈ log₂(6+1) - 1 = 2.58
ASL(失败) ≈ 3
```

> ⚠️ 折半查找**仅适用于有序顺序表**（不能是链表！因为链表无法 O(1) 访问 mid）

```python
def binary_search(arr: list, key: int) -> int:
    """
    折半查找
    返回key的索引，未找到返回-1

    时间复杂度: O(logn)
    空间复杂度: O(1)
    """
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

## 3. 分块查找 <a id="block"></a>

**核心思想**：将线性表分成若干块，**块间有序**（前块最大 ≤ 后块最小），块内无序。先在索引表折半确定块号，再在块内顺序查找。

**优势**：不需要全部元素有序，只需块间有序。

**手写示例**：查找 38

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

```python
def block_search(blocks: list, block_index: list, key: int) -> int:
    """
    分块查找
    blocks: 分块后的数据 [[block1], [block2], ...]
    block_index: 索引表 [每块最大值, ...]

    返回全局索引，未找到返回-1
    """
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

## 4. 二叉搜索树（BST）<a id="bst"></a>

**核心思想**：左子树所有结点值 < 根结点值 < 右子树所有结点值。

**手写 BST 插入过程**（依次插入 `50, 30, 70, 20, 40, 60, 80`）：

```
插入50:      50
插入30:      50
            /
           30
插入70:      50        插入70:    50
            /                    /  \
           30                   30   70
插入20:      50        插入40:    50
            /          插入20:  /   \
           30        插入20: 30   70
          /        /   / \
         20      40      20   40   70

最终:         50
            /    \
           30     70
          / \    /  \
        20  40  60  80

中序遍历: 20, 30, 40, 50, 60, 70, 80 (有序✓)
```

### BST查找手写过程

**手写示例**：在上述 BST 中查找 60

```
查找过程:
  curr=50, key=60
  60 > 50, curr=curr.right=70

  curr=70, key=60
  60 < 70, curr=curr.left=60

  curr=60, key=60
  60 == 60 ✓ 找到!

返回: 结点60
```

### BST删除三种情况

**情况1：删除叶子结点**
```
删除前:
    5
   / \
  3   7
   \
    4

删除4(叶子):

删除后:
    5
   / \
  3   7
```

**情况2：删除只有一个孩子的结点**
```
删除前:
    5
   / \
  3   7
   \
    6

删除7(只有一个孩子6):

删除后:
    5
   /
  3
  \
    6
```

**情况3：删除有两个孩子的结点**
```
删除前:
     5
    / \
   3   8
  /   / \
  1   6   9

删除5(有左右孩子):

找到右子树最小值6(后继):
用6替换5的位置:
     6
    / \
  3   8
  /       \
  1       9

删除原6结点(最多一个右孩子):
     6
    / \
  3   8
          \
        9
```

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
        else:
            # 情况1: 叶子结点
            if not node.left and not node.right:
                return None
            # 情况2: 只有一个孩子
            elif not node.left or not node.right:
                return node.left if node.left else node.right
            # 情况3: 有两个孩子
            else:
                # 找右子树的最小值(后继)
                succ_parent = node
                succ = node.right
                while succ.left:
                    succ_parent = succ
                    succ = succ.left
                # 用后继结点替换被删结点
                node.key = succ.key
                # 删除后继结点
                if succ_parent.left == succ:
                    succ_parent.left = succ.right
                else:
                    succ_parent.right = succ.right

        return node
```

---

## 5. 平衡二叉树（AVL树）<a id="avl"></a>

**核心思想**：BST的改进。**任意结点左右子树高度差（平衡因子）≤ 1**。不平衡时通过旋转调整。

**手写 AVL 插入失衡调整**（依次插入 `50, 30, 20`）：

```
插入50:   50
插入30:      50(+1)     插入20:   50(+2) ← 失衡!
            /                    /
           30                   30
                                            /
                                          20

LL失衡 → 右旋:
       30
      /  \
     20   50
```

### 四种旋转详解

| 类型 | 条件 | 操作 |
|------|--------|------|
| LL型 | BF > 1 且 key < node.left.key | 右旋 |
| RR型 | BF < -1 且 key > node.right.key | 左旋 |
| LR型 | BF > 1 且 key > node.left.key | 先左旋左子树，再右旋 |
| RL型 | BF < -1 且 key < node.right.key | 先右旋右子树，再左旋 |

**LL型（右旋）**：
```
旋转前:
     y
    / \
   x   T3
  / \
 T1  T2

旋转后:
     x
    / \
  T1   y
      / \
     T2  T3
```

**LR型（先左旋左子树，再右旋）**：
```
旋转前:
       z
      /
     y
    /
   x
  \
   T2

步骤1(左旋y):
       z
      /
     x
    / \
  T1  y
      /
     T2

步骤2(右旋z):
     x
    / \
  T1   z
      / \
     y  T3
    /
  T2
```

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

    def insert(self, node: AVLNode, key: int) -> AVLNode:
        """插入并平衡"""
        if not node:
            return AVLNode(key)
        if key < node.key:
            node.left = self.insert(node.left, key)
        elif key > node.key:
            node.right = self.insert(node.right, key)
        else:
            return node  # 已存在

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

    def add(self, key: int) -> None:
        self.root = self.insert(self.root, key)
```

---

## 6. B树 <a id="btree"></a>

**核心思想**：多路平衡查找树。所有结点（包括内部结点）的孩子数不超过m。所有叶子结点在同一层（平衡特性）。

**性质**：
- 树的高度为h，关键字数N满足：m^h ≤ N < m^(h+1)
- h层最多有 m^h 个结点，h+1层至少有 2 个结点

**手写 B树查找示例**（m=3阶B树）：

```
B树结构（m=3）:
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
  85 == 85 ✓ 找到!
```

```python
class BTreeNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []     # 关键字
        self.children = []  # 如果是叶子则为空


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

        # 在当前结点中查找
        for i in range(len(node.keys)):
            if key == node.keys[i]:
                return True
            elif key < node.keys[i]:
                # 递归搜索第i个子结点
                return self._search(node.children[i], key)

        # key比所有key都大，搜索最后一个子结点
        if not node.is_leaf:
            return self._search(node.children[-1], key)

        return False
```

---

## 7. B+树 <a id="bplustree"></a>

**核心思想**：B树的变体。**所有结点（包括内部结点）的孩子数不超过m**（不是m+1）。

**与B树的区别**：
| 特性 | B树 | B+树 |
|------|------|-------|
| 结点孩子数 | ≤ m | ≤ m |
| 内部结点关键字数 | k(m-1) ≤ k ≤ m | m-1 |
| 叶子结点关键字数 | k(m-1) ≤ k ≤ m | m-1 |
| 叶子结点孩子数 | 0 | 0 |
| 树形 | 紧凑 | 完全平衡 |

**B+树查找手写示例**（m=3阶B+树）：

```
B+树结构（m=3）:
          [50, 75, 100]
        /      |      \
   [20, 30]  [60, 70]  [85, 90]

查找 70:
第1层: 在根结点中查找
  50 < 70 < 75 → 找到第2个孩子指针
第2层: 在第2个子结点中查找
  60 < 70 → 找到第2个孩子指针
第3层: 在第2个孩子中查找
  70 == 70 ✓ 找到!

查找 25:
第1层: 在根结点中查找
  25 < 50 → 找到第1个孩子指针
第2层: 在第1个子结点中查找
  25 < 30 → 超出范围，未找到 ✗
```

**B+树插入手写示例**（在上述树中插入 65）：

```
插入65:
第1层: 根=[50, 75, 100], 65<50, 65<75 → 插入到第2子结点

第2层: 第2子结点=[60, 70], 60<65<70 → 需要分裂!

分裂第2子结点:
  提升中值65到根结点
  根=[50, 65, 75, 100] (3个关键字，超过m-1=2!)

分裂根结点:
  创建新的根结点
  将前m/2=1个关键字留在原根
  将后m-1=2个关键字放入新根
  新根=[50], 右子=[75, 100]

最终树:
       [50]
        /    \
   [20, 30] [65] [85, 90]
```

```python
class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []     # 关键字（最多m-1个）
        self.children = []  # 最多m个孩子


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
                return self._search(node.children[i], key)

        # key比所有key都大
        if key > node.keys[-1]:
            if node.is_leaf:
                return False
            return self._search(node.children[-[1]], key)

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

    def _insert(self, node: BPlusTreeNode, key: int) -> tuple:
        """递归插入，返回(节点, 是否溢出)"""
        # 实现略，涉及分裂和提升操作
        pass
```

---

## 8. 散列表（哈希表）<a id="hash"></a>

**核心思想**：通过哈希函数将关键字映射到存储位置，实现O(1)平均查找。

**装填因子**：
```
α = n / m
```
- n：已存储元素个数
- m：散列表容量
- α越小，冲突越少，查找效率越高

### 常用哈希函数

- **除留余数法**: `H(key) = key % p`（p取≤表长的最大素数）
- **直接定址法**: `H(key) = a*key + b`（不会冲突）

### 冲突处理方法

| 方法 | 思路 | 特点 |
|------|------|------|
| 拉链法 | 同义词链在一起 | 简单，删除方便 |
| 线性探测 | d₀, d₀+1, d₀+2... | 会产生堆积现象 |
| 平方探测 | d₀+1², d₀-1², d₀+2²... | 缓解堆积 |
| 双哈希 | H₁(key), H₂(key) | 减少冲突 |

### 线性探测法手写示例

**手写示例**：m=7，插入 `[3, 1, 4, 5, 2]`

```
初始: [None, None, None, None, None, None]

插入3: H(3)=3%7=3, table[3]=3
       [None, None, None, 3, None, None]

插入1: H(1)=1%7=1, table[1]=1
       [None, 1, None, 3, None, None]

插入4: H(4)=4%7=4, table[4]=4
       [None, 1, None, 3, 4, None]

插入5: H(5)=5%7=5, table[5]=5
       [None, 1, None, 3, 4, 5]

插入2: H(2)=2%7=2, table[2]=2
       [None, 1, 2, 3, 4, 5]

装填因子 α = 5/7 ≈ 0.71
```

**带冲突的线性探测示例**：m=7，插入 `[3, 1, 4, 1, 5, 2]`

```
初始: [None, None, None, None, None, None]

插入3: H(3)=3, table[3]=3
       [None, None, None, 3, None, None]

插入1: H(1)=1, table[1]=1
       [None, 1, None, 3, None, None]

插入4: H(4)=4, table[4]=4
       [None, 1, None, 3, 4, None None]

插入1: H(1)=1, table[1]=1==1 ✓ 已存在!

插入5: H(5)=5, table[5]=5
       [None, 1, None, 3, 4, 5 None]

插入2: H(2)=2, table[2]=2
       [None, 1, 2, 3, 4, 5 None]
```

### 拉链法手写示例

**手写示例**：m=5，插入 `[14, 23, 1, 9, 36, 22, 15]`

```
初始: [None, None, None, None]

插入14: H(14)=14%5=4, table[4]=[14]
       [None, None, None, [14]]

插入23: H(23)=23%5=3, table[3]=[23]
       [None, None, [23], [14]]

插入1:  H(1)=1%5=1, table[1]=[1]
       [None, [1], [23], [14]]

插入9:  H(9)=9%5=4, table[4]=[14]→[9]
       [None, [1], [23], [14, 9]]

插入36: H(36)=36%5=1, table[1]=[1]→[36]
       [None, [1, [36], [23], [14, 9]]

插入22: H(22)=22%5=2, table[2]=[22]
       [None, [1, [36], [23], [14, 9]]
       [22]

插入15: H(15)=15%5=0, table[0]=[15]
       [[15], [1, [36], [23], [14, 9]]
       [22]

装填因子 α = 7/5 = 1.4 (需要扩容!)
```

```python
class ChainingHashTable:
    """拉链法散列表"""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]

    def _hash(self, key: int) -> int:
        """除留余数法"""
        return key % self.capacity

    def insert(self, key: int) -> bool:
        """插入(拉链法)"""
        idx = self._hash(key)

        # 检查是否已存在
        curr = self.table[idx]
        while curr:
            if curr.key == key:
                return False
            curr = curr.next

        # 插入链表头
        new_node = ChainNode(key)
        new_node.next = self.table[idx]
        self.table[idx] = new_node
        return True

    def search(self, key: int) -> bool:
        """查找"""
        idx = self._hash(key)
        curr = self.table[idx]
        while curr:
            if curr.key == key:
                return True
            curr = curr.next
        return False

    def load_factor(self) -> float:
        """装填因子"""
        n = 0
        for chain in self.table:
            curr = chain
            while curr:
                n += 1
                curr = curr.next
        return n / self.capacity


class LinearProbingHashTable:
    """线性探测法散列表"""
    def __init__(self, capacity: int):
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
```

---

## 9. 考研重点 & 易错点

### 高频考点

| 考点 | 关键要点 |
|------|---------|
| **折半查找** | 只适用于有序顺序表，ASL≈log₂(n+1)-1 |
| **BST删除** | 三种情况，尤其是有两个孩子的处理 |
| **AVL旋转** | LL、RR、LR、RL四种旋转类型 |
| **B树性质** | m^h ≤ N < m^(h+1) |
| **B+树性质** | 每个结点关键字数不超过m-1 |
| **散列冲突** | 线性探测、拉链法、ASL计算 |
| **装填因子** | α=n/m，影响散列表查找效率 |

### 易错点

| 易错点 | 正确做法 |
|--------|---------|
| 折半查找 | 只能用于有序顺序表，不能用于链表 |
| BST删除后继 | 找右子树最小值(或左子树最大值) |
| AVL旋转次数 | LR和RL型需要两次旋转 |
| 线性探测循环 | 需用取模实现 `(index+1)%m` |
| 拉链法插入 | 插入到链表头，保证时间复杂度O(1) |
| B树关键字数 | 内部结点：⌈m/2⌉k⌉m，叶子：⌈m-1 |
| B+树关键字数 | 最多m-1个关键字 |

### 稳定性总结

| 算法 | 是否稳定 |
|------|---------|
| 顺序查找 | ✅ 稳定（相对顺序不变） |
| 折半查找 | ✅ 稳定 |
| BST | ❌ 不稳定 |
| AVL树 | ❌ 不稳定 |
| B树 | ❌ 不稳定 |
| B+树 | ❌ 不稳定 |
| 散列表 | 取决于冲突处理方法 |

---

## 10. 复杂度总结表

| 查找方法 | 时间复杂度(平均) | 时间复杂度(最坏) | 空间复杂度 |
|----------|-----------------|-----------------|-----------|
| 顺序查找 | O(n) | O(n) | O(1) |
| 折半查找 | O(logn) | O(logn) | O(1) |
| 分块查找 | O(√n) | O(n) | O(1) |
| BST(平均) | O(logn) | O(n) | O(n) |
| AVL树 | O(logn) | O(logn) | O(n) |
| B树 | O(logₘn) | O(logₘn) | O(n) |
| B+树 | O(logₘn) | O(logₘn) | O(n) |
| 散列表(探测) | O(1) | O(n) | O(m) |
| 散列表(拉链) | O(1) | O(n) | O(m+n) |

**注**：散列表O(1)是平均情况，最坏O(n)所有元素都冲突。

---

## 📝 完整代码示例

```python
def binary_search(arr: list, key: int) -> int:
    """折半查找"""
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        if arr[mid] == key:
            return mid
        elif arr[mid] < key:
            low = mid + 1
        else:
            high = mid - 1

    return -1


class ChainingHashTable:
    """拉链法散列表"""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]

    def insert(self, key: int) -> bool:
        idx = key % self.capacity

        # 检查是否已存在
        for item in self.table[idx]:
            if item == key:
                return False

        self.table[idx].append(key)
        return True

    def search(self, key: int) -> bool:
        idx = key % self.capacity
        return key in self.table[idx]


if __name__ == "__main__":
    # 测试折半查找
    arr = [1, 2, 3, 5, 8, 9]
    print("=" * 40)
    print("折半查找测试")
    print(f"数组: {arr}")
    print(f"查找8: {binary_search(arr, 8)}")
    print(f"查找4: {binary_search(arr, 4)}")

    # 测试散列表
    print("\n散列表测试")
    ht = ChainingHashTable(7)
    for key in [3, 1, 4, 5, 2]:
        ht.insert(key)
    print(f"插入3,1,4,5,2后: {ht.table}")
    print(f"查找4: {ht.search(4)}")
    print(f"查找6: {ht.search(6)}")
```
