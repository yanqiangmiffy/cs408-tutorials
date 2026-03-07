# 第7章 查找

> **考研要点速记**：折半查找仅适用于有序顺序表，ASL≈log₂(n+1)-1；BST的删除有三种情况；散列表的装填因子α=n/m影响查找效率。

## 1. 顺序/折半/分块查找 <a id="basic"></a>

### 顺序查找

```python
def sequential_search(arr: list, key: int) -> int:
    """
    顺序查找
    返回key的索引，未找到返回-1
    """
    for i, val in enumerate(arr):
        if val == key:
            return i
    return -1

def sequential_search_sentinel(arr: list, key: int) -> int:
    """
    顺序查找（带哨兵优化）
    减少边界检查次数
    """
    n = len(arr)
    arr.append(key)  # 哨兵

    i = 0
    while arr[i] != key:
        i += 1

    if i < n:
    arr.pop()  # 移除哨兵
        return i
    else:
        arr.pop()
        return -1
```

**ASL（平均查找长度）**：
- 查找成功：ASL = (n+1)/2
- 查找失败：ASL = n

### 折半查找

折半查找要求有序顺序表，通过比较中间元素缩小查找范围。

```python
def binary_search(arr: list, key: int) -> int:
    """
    折半查找
    返回key的索引，未找到返回-1
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

**判定树**：折半查找的判定树是一棵平衡二叉树。

**ASL**：ASL ≈ log₂(n+1) - 1

## 2. BST & AVL树 <a id="bst-avl"></a>

### 二叉搜索树（BST）

BST满足：左子树所有结点值 < 根结点值 < 右子树所有结点值。

```python
class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def search(self, key: int) -> BSTNode:
        """查找"""
        curr = self.root
        while curr:
            if key == curr.key:
                return curr
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return None

    def insert(self, key: int) -> None:
        """插入"""
        if not self.root:
            self.root = BSTNode(key)
            return

        curr = self.root
        parent = None

        while curr:
            parent = curr
            if key < curr.key:
                curr = curr.left
            elif key > curr.key:
                curr = curr.right
            else:
                return  # 已存在

        if key < parent.key:
            parent.left = BSTNode(key)
        else:
            parent.right = BSTNode(key)

    def delete(self, key: int) -> bool:
        """删除（三种情况）"""
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

        # 情况1：被删结点为叶子结点
        if not curr.left and not curr.right:
            if not parent:
                self.root = None
            elif parent.left == curr:
                parent.left = None
            else:
                parent.right = None

        # 情况2：被删结点只有一个孩子
        elif not curr.left or not curr.right:
            child = curr.left if curr.left else curr.right
            if not parent:
                self.root = child
            elif parent.left == curr:
                parent.left = child
            else:
                parent.right = child

        # 情况3：被删结点有两个孩子
        else:
            # 找右子树的最小值（后继）
            succ_parent = curr
            succ = curr.right

            while succ.left:
                succ_parent = succ
                succ = succ.left

            # 用后继结点替换被删结点
            curr.key = succ.key

            # 删除后继结点（后继结点最多只有一个右孩子）
            if succ_parent.left == succ:
                succ_parent.left = succ.right
            else:
                succ_parent.right = succ.right

        return True
```

### AVL树

AVL树是平衡因子绝对值不超过1的BST，通过四种旋转保持平衡。

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

class AVL:
    def __init__(self):
        self.root = None

    def rotate_right(self, y: AVLNode) -> AVLNode:
        """右旋（LL型）"""
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.update_height()
        x.update_height()

        return x

    def rotate_left(self, x: AVLNode) -> AVLNode:
        """左旋（RR型）"""
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

        # LL型：右旋
        if balance > 1 and key < node.left.key:
            return self.rotate_right(node)

        # RR型：左旋
        if balance < -1 and key > node.right.key:
            return self.rotate_left(node)

        # LR型：先左旋左子树，再右旋
        if balance > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # RL型：先右旋右子树，再左旋
        if balance < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def add(self, key: int) -> None:
        self.root = self.insert(self.root, key)
```

## 3. 散列表 <a id="hash"></a>

### 除留余数法 + 线性探测

```python
class LinearProbingHashTable:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.table = [None] * capacity

    def hash_func(self, key: int) -> int:
        """除留余数法"""
        return key % self.capacity

    def insert(self, key: int) -> bool:
        """插入（线性探测）"""
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
        """插入（拉链法）"""
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
```

## 考研重点 & 易错点

- ⚠️ 易错点：折半查找只能用于有序顺序表，不能用于链表
- 📌 高频考点：BST删除操作的三种情况，尤其是有两个孩子的结点处理
- ⚠️ 易错点：AVL树的四种旋转类型（LL、RR、LR、RL），LR和RL需要两次旋转
- 📌 高频考点：散列冲突处理方法（线性探测、二次探测、拉链法）及其ASL计算
- 📌 高频考点：装填因子α=n/m对散列表查找效率的影响，α越小冲突越少

## 复杂度总结表

| 查找方法 | 时间复杂度(平均) | 时间复杂度(最坏) | 空间复杂度 |
|----------|-----------------|-----------------|-----------|
| 顺序查找 | O(n) | O(n) | O(1) |
| 折半查找 | O(logn) | O(logn) | O(1) |
| BST(平衡) | O(logn) | O(n) | O(n) |
| AVL树 | O(logn) | O(logn) | O(n) |
| 散列表(探测) | O(1) | O(n) | O(m) |
| 散列表(拉链) | O(1) | O(n) | O(m+n) |
