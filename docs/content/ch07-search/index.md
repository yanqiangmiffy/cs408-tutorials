# 第7章 查找

> 查找是计算机中的基本操作，根据给定值在数据结构中定位对应元素。掌握折半查找、BST、AVL和散列表是考研的核心内容。

---

## 1. 顺序查找 <a id="basic"></a>

**核心思想**：从第一个元素开始，逐个比较，直到找到目标或遍历完所有元素。

**手写示例**：在 `[3, 1, 4, 1, 5, 2]` 中查找 `4`

```
索引:   0   1   2   3   4   5
数组: [ 3,  1,  4,  1,  5,  2]

i=0: 3 != 4, 继续
i=1: 1 != 4, 继续
i=2: 4 == 4 ✓ 找到！

返回: 2
```

**ASL（平均查找长度）**：
- 查找成功：ASL = (n+1)/2 = (6+1)/2 = 3.5
- 查找失败：ASL = n = 6

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

**判定树**：折半查找的判定树是一棵平衡二叉树。

**ASL**：ASL ≈ log₂(n+1) - 1

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
        elif arr[mid] < key:
            low = mid + 1
        else:
            high = mid - 1

    return -1
```

---

### 分块查找

**核心思想**：块间有序、块内无序。先在索引表折半查找确定块，再在块内顺序查找。

**优势**：不需要全部元素有序，只需块间有序。

---

## 3. 二叉搜索树（BST）<a id="bst-avl"></a>

**核心思想**：左子树所有结点值 < 根结点值 < 右子树所有结点值。

### BST查找

```python
class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


def bst_search(root: BSTNode, key: int) -> BSTNode:
    """BST查找"""
    curr = root
    while curr:
        if key == curr.key:
            return curr
        elif key < curr.key:
            curr = curr.left
        else:
            curr = curr.right
    return None
```

### BST删除（三种情况）

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
  /       \
  1       9
```

### BST完整实现

```python
class BST:
    def __init__(self):
        self.root = None

    def delete(self, key: int) -> bool:
        """删除(三种情况)"""
        curr = self.root
        parent = None

        # 查找要删除的结点
        while curr and curr.key != key:
            parent = curr
            if key < curr.key:
                curr = curr.left
            else:
                curr = curr.right

        if not curr:
            return False  # 未找到

        # 情况1: 被删结点为叶子结点
        if not curr.left and not curr.right:
            if not parent:
                self.root = None
            elif parent.left == curr:
                parent.left = None
            else:
                parent.right = None

        # 情况2: 被删结点只有一个孩子
        elif not curr.left or not curr.right:
            child = curr.left if curr.left else curr.right
            if not parent:
                self.root = child
            elif parent.left == curr:
                parent.left = child
            else:
                parent.right = child

        # 情况3: 被删结点有两个孩子
        else:
            # 找右子树的最小值(后继)
            succ_parent = curr
            succ = curr.right
            while succ.left:
                succ_parent = succ
                succ = succ.left

            # 用后继结点替换被删结点
            curr.key = succ.key

            # 删除后继结点(后继结点最多只有一个右孩子)
            if succ_parent.left == succ:
                succ_parent.left = succ.right
            else:
                succ_parent.right = succ.right

        return True
```

---

## 4. AVL树 <a id="avl"></a>

**核心思想**：平衡因子绝对值不超过1的BST。平衡因子 = 左子树高度 - 右子树高度。

### 四种旋转

| 类型 | 条件 | 操作 |
|------|--------|------|
| LL型 | BF > 1 且 key < node.left.key | 右旋 |
| RR型 | BF < -1 且 key > node.right.key | 左旋 |
| LR型 | BF > 1 且 key > node.left.key | 先左旋左子树，再右旋 |
| RL型 | BF < -1 且 key < node.right.key | 先右旋右子树，再左旋 |

### 旋转图示

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

### AVL完整实现

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

## 5. 散列表（哈希表）<a id="hash"></a>

**核心思想**：通过哈希函数将关键字映射到存储位置，实现O(1)平均查找。

### 装填因子

```
α = n / m
```
- n：已存储元素个数
- m：散列表容量
- α越小，冲突越少，查找效率越高

### 除留余数法

**哈希函数**：`hash(key) = key % m`

### 线性探测法

**核心思想**：冲突时，向后逐个查找空位。

**手写示例**：m=7，插入 [3, 1, 4, 1, 5, 2]

```
初始: [None, None, None, None, None, None, None]

插入3: hash(3)=3, table[3]=3
       [None, None, None, 3, None, None, None]

插入1: hash(1)=1, table[1]=1
       [None, 1, None, 3, None, None, None]

插入4: hash(4)=4, table[4]=4
       [None, 1, None, 3, 4, None, None]

插入1: hash(1)=1, table[1]=1==1, 已存在!
       [None, 1, None, 3, 4, None, None]

插入5: hash(5)=5, table[5]=5
       [None, 1, None, 3, 4, 5, None]

插入2: hash(2)=2, table[2]=2
       [None, 1, 2, 3, 4, 5, None]

装填因子 α = 5/7 ≈ 0.71
```

```python
class LinearProbingHashTable:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.table = [None] * capacity

    def hash_func(self, key: int) -> int:
        """除留余数法"""
        return key % self.capacity

    def insert(self, key: int) -> bool:
        """插入(线性探测)"""
        index = self.hash_func(key)
        start = index

        while self.table[index] is not None:
            if self.table[index] == key:
                return False  # 已存在
            index = (index + 1) % self.capacity
            if index == start:
                return False  # 表满

        self.table[index] = key
        return True

    def search(self, key: int) -> int:
        """查找，返回索引，未找到返回-1"""
        index = self.hash_func(key)
        start = index

        while self.table[index] is not None:
            if self.table[index] == key:
                return index
            index = (index + 1) % self.capacity
            if index == start:
                break

        return -1

    def load_factor(self) -> float:
        """装填因子"""
        n = sum(1 for x in self.table if x is not None)
        return n / self.capacity
```

### 拉链法

**核心思想**：冲突时，将元素链到同一下标位置。

**手写示例**：m=5，插入 [3, 1, 4, 8, 5, 2]

```
初始: [None, None, None, None, None]

插入3: hash(3)=3, table[3]=[3]
       [None, None, None, [3], None]

插入1: hash(1)=1, table[1]=[1]
       [None, [1], None, [3], None]

插入4: hash(4)=4, table[4]=[4]
       [None, [1], None, [3], [4]]

插入8: hash(8)=3, table[3]=[3]→[8]
       [None, [1], None, [3,8], [4]]

插入5: hash(5)=0, table[0]=[5]
       [[5], [1], None, [3,8], [4]]

插入2: hash(2)=2, table[2]=[2]
       [[5], [1], [2], [3,8], [4]]
```

```python
class ChainNode:
    def __init__(self, key):
        self.key = key
        self.next = None


class ChainingHashTable:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.table = [None] * capacity

    def hash_func(self, key: int) -> int:
        """除留余数法"""
        return key % self.capacity

    def insert(self, key: int) -> bool:
        """插入(拉链法)"""
        index = self.hash_func(key)

        # 检查是否已存在
        curr = self.table[index]
        while curr:
            if curr.key == key:
                return False
            curr = curr.next

        # 插入表头
        new_node = ChainNode(key)
        new_node.next = self.table[index]
        self.table[index] = new_node
        return True

    def search(self, key: int) -> bool:
        """查找"""
        index = self.hash_func(key)
        curr = self.table[index]
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
```

---

---

## 6. 考研重点 & 易错点

### 高频考点

| 考点 | 关键要点 |
|------|---------|
| **折半查找** | 只适用于有序顺序表，ASL≈log₂(n+1)-1 |
| **BST删除** | 三种情况，尤其是有两个孩子的处理 |
| **AVL旋转** | LL、RR、LR、RL四种旋转类型 |
| **散列冲突** | 线性探测、拉链法及其ASL计算 |
|**装填因子** | α=n/m，影响散列表查找效率 |

### 易错点

| 易错点 | 正确做法 |
|--------|---------|
| 折半查找 | 只能用于有序顺序表，不能用于链表 |
| BST删除后继 | 找右子树最小值(或左子树最大值) |
| AVL旋转次数 | LR和RL型需要两次旋转 |
| 线性探测循环 | 需用取模实现 `(index+1)%m` |
| 拉链法插入 | 插入到链表头，保证时间复杂度O(1) |

### 稳定性总结

| 算法 | 是否稳定 |
|------|---------|
| 顺序查找 | ✅ 稳定（相对顺序不变） |
| 折半查找 | ✅ 稳定 |
| BST | ❌ 不稳定 |
| AVL树 | ❌ 不稳定 |
| 散列表 | 取决于冲突处理方法 |

---

## 7. 复杂度总结表

| 查找方法 | 时间复杂度(平均) | 时间复杂度(最坏) | 空间复杂度 |
|----------|-----------------|-----------------|-----------|
| 顺序查找 | O(n) | O(n) | O(1) |
| 折半查找 | O(logn) | O(logn) | O(1) |
| BST(平均) | O(logn) | O(n) | O(n) |
| AVL树 | O(logn) | O(logn) | O(n) |
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


class LinearProbingHashTable:
    """散列表-线性探测"""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.table = [None] * capacity

    def insert(self, key: int) -> bool:
        index = key % self.capacity
        start = index

        while self.table[index] is not None:
            if self.table[index] == key:
                return False
            index = (index + 1) % self.capacity
            if index == start:
                return False

        self.table[index] = key
        return True

    def search(self, key: int) -> int:
        index = key % self.capacity
        start = index

        while self.table[index] is not None:
            if self.table[index] == key:
                return index
            index = (index + 1) % self.capacity
            if index == start:
                break

        return -1


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
    ht = LinearProbingHashTable(7)
    for key in [3, 1, 4, 5, 2]:
        ht.insert(key)
    print(f"插入3,1,4,5,2后: {ht.table}")
    print(f"查找4: {ht.search(4)}")
    print(f"查找6: {ht.search(6)}")
```
