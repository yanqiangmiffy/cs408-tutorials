# 第5章 树与二叉树

> 树是重要的非线性数据结构，二叉树是树的特例。掌握二叉树遍历、哈夫曼树和并查集是考研的核心内容。

---

## 5.1 树

### 5.1.1 树的定义

**树**是n（n≥0）个结点的有限集合。当n=0时，称为空树；当n>0时，满足：

1. 有且仅有一个特定的称为**根**（Root）的结点
2. 其余结点可分为m（m>0）个互不相交的有限集合T₁,T₂,...,Tₘ，其中每个集合本身又是一棵树，称为根的**子树**（SubTree）

### 5.1.2 树的基本术语

| 术语 | 定义 |
|------|------|
| **根结点** | 树中唯一的没有前驱的结点 |
| **叶子结点** | 度为0的结点，没有子结点 |
| **非叶子结点** | 度不为0的结点 |
| **结点的度** | 结点拥有的子树个数 |
| **树的度** | 树内各结点度的最大值 |
| **孩子/双亲** | 某结点的子树的根称为该结点的孩子，该结点称为孩子的双亲 |
| **兄弟** | 同一双亲的孩子互为兄弟 |
| **祖先/子孙** | 从根到某结点的路径上的所有结点都是该结点的祖先，该结点的所有子树中的结点都是该结点的子孙 |
| **层次** | 根为第1层，其孩子为第2层，依此类推 |
| **树的深度** | 树中结点的最大层次 |
| **有序树/无序树** | 子树有次序的树称为有序树，否则为无序树 |
| **森林** | m（m≥0）棵互不相交的树的集合 |

### 5.1.3 树的性质

1. 树中的结点数等于所有结点的度数之和加1
2. 度为k的树中至少有k+1个结点
3. 深度为h的k叉树最多有 (k^h - 1)/(k - 1) 个结点
4. n个结点的k叉树的最小深度为 ⌈logₖ[n(k-1)+1]⌉

---

## 5.2 二叉树

### 5.2.1 二叉树的定义

**二叉树**是n（n≥0）个结点的有限集合，满足：

1. n=0时为空二叉树
2. n>0时由一个根结点和两个互不相交的、分别称为左子树和右子树的二叉树组成

**注意**：二叉树是有序树，左子树和右子树是有区别的，即使为空也有区别。

### 二叉树的5种基本形态

```
1. 空树
2. 只有根结点
3. 只有左子树
4. 只有右子树
5. 既有左子树又有右子树
```

### 特殊二叉树

| 类型 | 定义 |
|------|------|
| **满二叉树** | 深度为h，有2^h - 1个结点的二叉树 |
| **完全二叉树** | 深度为h，前h-1层是满的，第h层从左到右连续排列 |
| **二叉排序树** | 左子树<根<右子树 |
| **平衡二叉树** | 左右子树深度差不超过1 |

### 二叉树核心特性速记

| 维度 | 结论 |
|------|------|
| **有序性** | 二叉树是有序树，左子树和右子树不能交换看待 |
| **孩子个数** | 每个结点最多两个孩子，因此“度”最大只能是 2 |
| **空子树** | 左子树和右子树都允许为空，空子树在递归定义中同样有意义 |
| **存储方式** | 完全二叉树更适合顺序存储，普通二叉树通常用链式存储 |
| **遍历价值** | 先序便于复制结构，中序常用于 BST 的有序输出，层序适合按层问题 |
| **唯一还原** | 无重复结点时，先序+中序 或 中序+后序可以唯一确定二叉树 |

### 5.2.2 二叉树的性质（必考！）

| 性质 | 内容 |
|------|------|
| 1 | 非空二叉树上第k层最多有 2^(k-1) 个结点 |
| 2 | 深度为h的二叉树最多有 2^h - 1 个结点 |
| 3 | n₀ = n₂ + 1（叶子结点数 = 度为2的结点数 + 1） |
| 4.1 | 完全二叉树中，编号为i的结点，左孩子编号2i（若存在） |
| 4.2 | 完全二叉树中，编号为i的结点，右孩子编号2i+1（若存在） |
| 4.3 | 完全二叉树中，编号为i的结点（i>1），双亲编号⌊i/2⌋ |
| 5 | n个结点的完全二叉树深度为 ⌊log₂n⌋ + 1 |

**性质3的证明思路**：
- 每个度2的结点产生2条边，度1的结点产生1条边，叶子结点产生0条边
- 总边数 = n₂ × 2 + n₁ × 1
- 总边数 = n - 1（树中边数 = 结点数 - 1）
- 因此：n = n₀ + n₁ + n₂
- 代入得：n₀ = n₂ + 1

### 5.2.3 二叉树的存储结构

#### 1. 顺序存储（适合完全二叉树）

```python
class SequentialBinaryTree:
    """顺序存储的二叉树"""
    def __init__(self, size):
        self.tree = [None] * (size + 1)  # 1-based indexing

    def insert(self, index, value):
        if 1 <= index < len(self.tree):
            self.tree[index] = value

    def get_left_child(self, index):
        left_idx = 2 * index
        return self.tree[left_idx] if left_idx < len(self.tree) else None

    def get_right_child(self, index):
        right_idx = 2 * index + 1
        return self.tree[right_idx] if right_idx < len(self.tree) else None

    def get_parent(self, index):
        parent_idx = index // 2
        return self.tree[parent_idx] if parent_idx >= 1 else None
```

**顺序存储的缺点**：对于非完全二叉树，会浪费大量存储空间

#### 2. 链式存储（通用）

```python
class TreeNode:
    """二叉链表存储"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left   # 左孩子指针
        self.right = right # 右孩子指针


class TriTreeNode:
    """三叉链表存储（方便找双亲）"""
    def __init__(self, val=0, left=None, right=None, parent=None):
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent  # 双亲指针
```

---

## 5.3 二叉树的遍历

### 5.3.1 先/中/后序遍历

#### 先序遍历（根-左-右）

**顺序**：先访问根结点，再遍历左子树，最后遍历右子树

```python
# 递归实现
def preorder_recursive(root: TreeNode) -> list:
    result = []
    def dfs(node):
        if not node:
            return
        result.append(node.val)  # 访问根
        dfs(node.left)           # 遍历左子树
        dfs(node.right)          # 遍历右子树
    dfs(root)
    return result

# 非递归实现（栈）
def preorder_iterative(root: TreeNode) -> list:
    if not root:
        return []
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:   # 先压右孩子
            stack.append(node.right)
        if node.left:    # 后压左孩子
            stack.append(node.left)
    return result
```

#### 中序遍历（左-根-右）

**顺序**：先遍历左子树，再访问根结点，最后遍历右子树

```python
# 递归实现
def inorder_recursive(root: TreeNode) -> list:
    result = []
    def dfs(node):
        if not node:
            return
        dfs(node.left)
        result.append(node.val)
        dfs(node.right)
    dfs(root)
    return result

# 非递归实现（栈）
def inorder_iterative(root: TreeNode) -> list:
    result = []
    stack = []
    curr = root
    while curr or stack:
        # 一直向左走，压栈
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

#### 后序遍历（左-右-根）

**顺序**：先遍历左子树，再遍历右子树，最后访问根结点

```python
# 递归实现
def postorder_recursive(root: TreeNode) -> list:
    result = []
    def dfs(node):
        if not node:
            return
        dfs(node.left)
        dfs(node.right)
        result.append(node.val)
    dfs(root)
    return result

# 非递归实现（栈）
def postorder_iterative(root: TreeNode) -> list:
    if not root:
        return []
    result = []
    stack = [(root, False)
    while stack:
        node, visited = stack.pop()
        if visited:
            result.append(node.val)
        else:
            stack.append((node, True))
            if node.right:
                stack.append((node.right, False))
            if node.left:
                stack.append((node.left, False))
    return result
```

### 5.3.2 层次遍历（BFS）

**顺序**：按层从上到下，每层从左到右访问

```python
from collections import deque

def level_order(root: TreeNode) -> list:
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

### 遍历示例（手写演示）

**二叉树结构**：

```
        A
       / \
      B   C
     / \   \
    D   E   F
```

#### 先序遍历（根-左-右）手写过程

```
访问顺序:
1. 访问根 A，输出 A
2. 递归遍历左子树
   2.1 访问根 B，输出 B
   2.2 递归遍历左子树
       2.2.1 访问根 D，输出 D
       2.2.2 D无子树，返回
   2.3 递归遍历右子树
       2.3.1 访问根 E，输出 E
       2.3.2 E无子树，返回
3. 递归遍历右子树
   3.1 访问根 C，输出 C
   3.2 递归遍历左子树，为空
   3.3 递归遍历右子树
       3.3.1 访问根 F，输出 F
       3.3.2 F无子树，返回

结果: A B D E C F
```

#### 中序遍历（左-根-右）手写过程

```
访问顺序:
1. 递归遍历左子树
   1.1 递归遍历左子树
       1.1.1 访问根 D，输出 D
   1.2 访问根 B，输出 B
   1.3 递归遍历右子树
       1.3.1 访问根 E，输出 E
2. 访问根 A，输出 A
3. 递归遍历右子树
   3.1 递归遍历左子树，为空
   3.2 访问根 C，输出 C
   3.3 递归遍历右子树
       3.3.1 访问根 F，输出 F

结果: D B E A C F
```

#### 后序遍历（左-右-根）手写过程

```
访问顺序:
1. 递归遍历左子树
   1.1 递归遍历左子树
       1.1.1 访问根 D，输出 D
   1.2 递归遍历右子树
       1.2.1 访问根 E，输出 E
   1.3 访问根 B，输出 B
2. 递归遍历右子树
   2.1 递归遍历左子树，为空
   2.2 递归遍历右子树
       2.2.1 访问根 F，输出 F
   2.3 访问根 C，输出 C
3. 访问根 A，输出 A

结果: D E B F C A
```

#### 层次遍历（BFS）手写过程

```
初始: queue=[A], visited=[]
第1轮: 出队A, 访问A
      入队B, C
      queue=[B,C], visited=[A]
第2轮: 出队B, 访问B
      入队D, E
      queue=[C,D,E], visited=[A,B]
第3轮: 出队C, 访问C
      入队F
      queue=[D,E,F], visited=[A,B,C]
第4轮: 出队D, 访问D
      D无子树
      queue=[E,F], visited=[A,B,C,D]
第5轮: 出队E, 访问E
      E无子树
      queue=[F], visited=[A,B,C,D,E]
第6轮: 出队F, 访问F
      F无子树
      queue=[], visited=[A,B,C,D,E,F]

结果: A B C D E F
```

| 遍历方式 | 结果 |
|----------|------|
| 先序遍历（根-左-右） | A B D E C F |
| 中序遍历（左-根-右） | D B E A C F |
| 后序遍历（左-右-根） | D E B F C A |
| 层次遍历 | A B C D E F |

### 5.3.3 由遍历序列构造二叉树

**核心原理**：
- 先序序列：第一个元素是根
- 中序序列：根左边是左子树，右边是右子树
- 后序序列：最后一个元素是根

```python
def build_tree_from_preorder_inorder(preorder: list, inorder: list) -> TreeNode:
    """根据先序和中序序列构造二叉树"""
    if not preorder or not inorder:
        return None

    # 先序第一个是根
    root_val = preorder[0]
    root = TreeNode(root_val)

    # 找根在中序中的位置
    root_idx = inorder.index(root_val)

    # 递归构造左右子树
    root.left = build_tree_from_preorder_inorder(
        preorder[1:1 + root_idx],           # 先序的左子树部分
        inorder[:root_idx]                   # 中序的左子树部分
    )
    root.right = build_tree_from_preorder_inorder(
        preorder[1 + root_idx:],              # 先序的右子树部分
        inorder[root_idx + 1:]                # 中序的右子树部分
    )
    return root


def build_tree_from_inorder_postorder(inorder: list, postorder: list) -> TreeNode:
    """根据中序和后序序列构造二叉树"""
    if not inorder or not postorder:
        return None

    # 后序最后一个是根
    root_val = postorder[-1]
    root = TreeNode(root_val)

    # 找根在中序中的位置
    root_idx = inorder.index(root_val)

    # 递归构造左右子树
    root.left = build_tree_from_inorder_postorder(
        inorder[:root_idx],                   # 中序的左子树部分
        postorder[:root_idx]                  # 后序的左子树部分
    )
    root.right = build_tree_from_inorder_postorder(
        inorder[root_idx + 1:],               # 中序的右子树部分
        postorder[root_idx:-1]                # 后序的右子树部分
    )
    return root
```

**注意**：由先序和后序序列不能唯一确定一棵二叉树，因为无法区分左右子树。

---

## 5.4 线索二叉树

### 5.4.1 线索二叉树的概念

**核心思想**：二叉树有n个结点，2n个指针域，其中n+1个空指针。线索二叉树利用这些空指针存储前驱和后继信息。

**优点**：
- 无需递归或栈即可线性遍历二叉树
- 对已线索化的结点，查找中序前驱和后继更方便

### 5.4.2 线索二叉树的存储结构

```python
class ThreadTreeNode:
    """线索二叉树结点"""
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None
        self.ltag = 0  # 0: 左孩子, 1: 前驱线索
        self.rtag = 0  # 0: 右孩子, 1: 后继线索
```

**标志位含义**：
- `ltag = 0`：left指向左孩子；`ltag = 1`：left指向前驱
- `rtag = 0`：right指向右孩子；`rtag = 1`：right指向后继

### 5.4.3 二叉树的线索化

```python
def in_threading(node: ThreadTreeNode, pre: list) -> None:
    """中序线索化"""
    if not node:
        return

    # 线索化左子树
    in_threading(node.left, pre)

    # 处理当前结点的左指针
    if not node.left:
        node.ltag = 1
        node.left = pre[0]  # 前驱线索

    # 处理前驱结点的右指针
    if pre[0] and not pre[0].right:
        pre[0].rtag = 1
        pre[0].right = node  # 后继线索

    # 更新前驱指针
    pre[0] = node

    # 线索化右子树
    in_threading(node.right, pre)


def create_in_threaded_tree(root: ThreadTreeNode) -> None:
    """创建中序线索二叉树"""
    pre = [None]  # 使用列表以便在递归中修改
    in_threading(root, pre)

    # 处理最后一个结点的右线索
    if pre[0]:
        pre[0].rtag = 1
```

### 5.4.4 在线索二叉树中找前驱后继

```python
def find_first_node(root: ThreadTreeNode) -> ThreadTreeNode:
    """找到中序遍历的第一个结点（最左下角）"""
    while root and root.ltag == 0:  # 有左孩子
        root = root.left
    return root


def find_next_node(node: ThreadTreeNode) -> ThreadTreeNode:
    """找到中序遍历的下一个结点（后继）"""
    if node.rtag == 1:  # 有后继线索
        return node.right
    else:  # 有右孩子，找右子树的最左结点
        node = node.right
        while node and node.ltag == 0:
            node = node.left
        return node


def in_order_traverse_threaded(root: ThreadTreeNode) -> list:
    """利用线索二叉树进行中序遍历"""
    result = []
    node = find_first_node(root)
    while node:
        result.append(node.val)
        node = find_next_node(node)
    return result
```

---

## 5.5 树和森林

### 5.5.1 树的存储结构

#### 1. 双亲表示法

```python
class ParentTree:
    """双亲表示法"""
    def __init__(self, size):
        self.nodes = [None] * size      # 数据域
        self.parent = [-1] * size      # 双亲位置

    def insert(self, index, value, parent_idx=-1):
        self.nodes[index] = value
        self.parent[index] = parent_idx
```

**优点**：找双亲方便，O(1)
**缺点**：找孩子困难，需要遍历整个数组

#### 2. 孩子表示法

```python
class ChildNode:
    """孩子结点"""
    def __init__(self, child_idx, next=None):
        self.child_idx = child_idx  # 孩子在表中的位置
        self.next = next           # 下一个孩子


class ChildTree:
    """孩子表示法"""
    def __init__(self, size):
        self.nodes = [None] * size        # 数据域
        self.children = [None] * size     # 孩子链表头指针

    def add_child(self, parent_idx, child_idx):
        """为parent_idx添加孩子child_idx"""
        new_child = ChildNode(child_idx, self.children[parent_idx])
        self.children[parent_idx] = new_child
```

#### 3. 孩子兄弟表示法（常用）

```python
class CSNode:
    """孩子兄弟表示法（二叉链表表示树）"""
    def __init__(self, val=0, first_child=None, next_sibling=None):
        self.val = val
        self.first_child = first_child  # 第一个孩子
        self.next_sibling = next_sibling  # 下一个兄弟
```

**优点**：
- 可以将树转换为二叉树
- 便于实现树的遍历

### 5.5.2 树、森林与二叉树的转换

**转换规则**：

| 转换方向 | 规则 |
|----------|------|
| 树→二叉树 | 左孩子指针指向第一个孩子，右孩子指针指向下一个兄弟 |
| 森林→二叉树 | 将森林中各树的根视为兄弟，按树→二叉树规则转换 |
| 二叉树→树 | 二叉树的左子树转换为树的子树，右子树转换为兄弟森林 |
| 二叉树→森林 | 从根开始，右子树转换为森林中的树 |

#### 树转二叉树

```python
def tree_to_binary(tree_root) -> TreeNode:
    """树转二叉树（孩子兄弟表示法转二叉树）"""
    if not tree_root:
        return None

    # 创建二叉树根结点
    binary = TreeNode(tree_root.val)

    # 树的第一个孩子 -> 二叉树的左孩子
    if tree_root.first_child:
        binary.left = tree_to_binary(tree_root.first_child)

    # 树的下一个兄弟 -> 二叉树的右孩子
    if tree_root.next_sibling:
        binary.right = tree_to_binary(tree_root.next_sibling)

    return binary
```

#### 二叉树转树

```python
def binary_to_tree(binary_root) -> CSNode:
    """二叉树转树（二叉树转孩子兄弟表示法）"""
    if not binary_root:
        return None

    # 创建树结点
    tree = CSNode(binary_root.val)

    # 二叉树的左孩子 -> 树的第一个孩子
    if binary_root.left:
        tree.first_child = binary_to_tree(binary_root.left)

    # 二叉树的右孩子 -> 树的下一个兄弟
    if binary_root.right:
        tree.next_sibling = binary_to_tree(binary_root.right)

    return tree
```

### 5.5.3 树和森林的遍历

#### 树的遍历

| 遍历方式 | 定义 |
|----------|------|
| **先根遍历** | 先访问根，再依次先根遍历各子树 |
| **后根遍历** | 依次后根遍历各子树，最后访问根 |

#### 森林的遍历

| 遍历方式 | 定义 |
|----------|------|
| **先序遍历** | 依次先序遍历森林中的每一棵树 |
| **中序遍历** | 依次中序遍历森林中的每一棵树 |

**重要对应关系**：

| 树/森林遍历 | 对应二叉树遍历 |
|-------------|----------------|
| 树的先根遍历 | 对应二叉树的先序遍历 |
| 树的后根遍历 | 对应二叉树的中序遍历 |
| 森林的先序遍历 | 对应二叉树的先序遍历 |
| 森林的中序遍历 | 对应二叉树的中序遍历 |

```python
def tree_preorder(tree_root: CSNode) -> list:
    """树的先根遍历"""
    if not tree_root:
        return []
    result = [tree_root.val]
    # 遍历所有子树（兄弟关系）
    child = tree_root.first_child
    while child:
        result.extend(tree_preorder(child))
        child = child.next_sibling
    return result


def tree_postorder(tree_root: CSNode) -> list:
    """树的后根遍历"""
    if not tree_root:
        return []
    result = []
    # 先遍历所有子树
    child = tree_root.first_child
    while child:
        result.extend(tree_postorder(child))
        child = child.next_sibling
    # 最后访问根
    result.append(tree_root.val)
    return result
```

---

## 5.6 哈夫曼树

### 5.6.1 哈夫曼树的基本概念

**哈夫曼树**（最优二叉树）：带权路径长度（WPL）最小的二叉树

**带权路径长度（WPL）**：
- 结点的带权路径长度 = 结点的权值 × 结点的层次
- 树的带权路径长度 = 所有叶子结点的带权路径长度之和

### 5.6.2 哈夫曼树的构建步骤

1. 统计每个字符的频率作为权值
2. 每个字符创建叶子结点，按权值构成最小堆
3. 每次取出两个最小权值的结点，合并为新结点
4. 新结点权值为两子结点权值之和
5. 重复直到只剩一个结点（根结点）

### 5.6.3 哈夫曼编码

**前缀编码**：没有任何一个编码是另一个编码的前缀
**哈夫曼编码**：在哈夫曼树中，从根到每个叶子结点的路径构成编码（左0右1）

### 5.6.4 哈夫曼树构建详细示例

**输入**: `"ABACBCA"`

**步骤1**：统计字符频率
```
字符   A   B   C
频率   3   2   2
```

**步骤2**：创建叶子节点并构建最小堆
```
初始堆: [(A,3), (B,2), (C,2)]
```

**步骤3**：取出两个最小权值节点合并
```
第1轮合并:
  取出最小两个: B(2), C(2)
  创建新节点: 权值 = 2 + 2 = 4
  堆状态: [(A,3), (BC,4)]

第2轮合并:
  取出最小两个: A(3), BC(4)
  创建新节点: 权值 = 3 + 4 = 7
  堆状态: [(ABC,7)]
```

**最终哈夫曼树**：
```
      ABC(7)
      /    \
    A(3)  BC(4)
          /    \
       B(2)   C(2)
```

### 5.6.5 哈夫曼编码生成

**编码规则**：从根到叶子结点，左走记0，右走记1

```
A: 根→左           编码 = 0
B: 根→右→左       编码 = 10
C: 根→右→右       编码 = 11
```

**编码表**：
```
字符   频率   编码   编码长度
  A     3      0        1
  B     2      10       2
  C     2      11       2
```

### 5.6.6 WPL（带权路径长度）计算

**公式**：WPL = Σ(权值 × 层次)

```
A: 3 × 1 = 3
B: 2 × 2 = 4
C: 2 × 2 = 4
───────────────
WPL = 3 + 4 + 4 = 11
```

**编码验证**（原串 `"ABACBCA"` 编码后长度）：
```
原串长度 = 7
总编码长度 = 3×1 + 2×2 + 2×2 = 11
压缩比 = 7/11 ≈ 0.636 (每个字符平均用1.57位)
```

### 5.6.7 Python实现

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


def calculate_wpl(root: HuffmanNode, depth: int = 0) -> int:
    """计算带权路径长度（WPL）"""
    if not root:
        return 0
    if root.char is not None:  # 叶子节点
        return root.freq * depth
    return calculate_wpl(root.left, depth + 1) + calculate_wpl(root.right, depth + 1)
```

---

## 5.7 并查集（Union-Find）

**核心思想**：维护不相交集合，支持两个操作：find（查找根结点）和union（合并两个集合）

### 5.7.1 并查集的基本操作

| 操作 | 说明 |
|--------|------|
| `find(x)` | 查找x所在集合的根结点 |
| `union(x, y)` | 合并x和y所在的集合 |
| `connected(x, y)` | 判断x和y是否在同一集合 |

### 5.7.2 两种优化

1. **路径压缩**：find时将沿途所有结点直接指向根
2. **按秩合并**：union时将矮树挂到高树上

### 5.7.3 并查集操作示例

**初始**：5个元素，各自独立
```
parent = [0, 1, 2, 3, 4]  # 每个元素是自己的根
```

**union(0, 1)**：合并0和1
```
parent = [0, 0, 2, 3, 4]
集合: {0, 1}, {2}, {3}, {4}
```

**union(2, 3)**：合并2和3
```
parent = [0, 0, 2, 2, 4]
集合: {0, 1}, {2, 3}, {4}
```

**find(1)**：查找1的根
```
1 → parent[1]=0 → parent[0]=0 (根)
返回 0
```

**connected(1, 3)**：判断1和3是否连通
```
find(1) = = 2
0 != 2 → 不连通
```

**union(1, 3)**：合并集合{0,1}和集合{2,3}
```
parent = [0, 0, 0, 2, 4]
集合: {0, 1, 2, 3}, {4}
```

### 5.7.4 路径压缩示例

**当前状态**：`parent = [0, 0, 1, 2, 4]`
```
find(3): 3 → 2 → 1 → 0 (根)
路径压缩后:
parent = [0, 0, 0, 0, 4]
         3直接指向根0
```

### 5.7.5 Python实现

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

## 5.8 考研重点 & 易错点

### 高频考点

| 考点 | 关键要害 |
|------|---------|
| **二叉树性质** | n₀ = n₂ + 1 是必考点 |
| **遍历顺序** | 先、中、后序的区别和还原 |
| **完全二叉树** | 编号关系、深度计算 |
| **哈夫曼树** | 构建过程、WPL计算、编码生成 |
| **并查集** | 路径压缩、按秩合并 |
| **线索二叉树** | 线索化、找前驱后继 |
| **树转二叉树** | 孩子兄弟表示法 |

### 易错点

| 易错点 | 正确做法 |
|--------|---------|
| n₀ = n₂ + 1 | 只适用于非空二叉树 |
| 线索二叉树标志位 | 0表示孩子指针，1表示线索 |
| 哈夫曼树编码 | 左0右1编码是约定，可互换 |
| 并查集未优化 | 时间复杂度O(n)，优化后接近O(1) |
| 完全二叉树编号 | 从1开始，左孩子2i，右孩子2i+1 |
| 树转二叉树 | 左孩子→第一个孩子，右孩子→下一个兄弟 |

### 应用场景

| 场景 | 数据结构 | 原因 |
|------|----------|------|
| 表达式树 | 二叉树 | 自然表示运算层次 |
| 文件系统 | 树 | 层次结构 |
| 数据压缩 | 哈夫曼树 | 最优前缀编码 |
| 连通性问题 | 并查集 | 高效合并查询 |
| 线性遍历二叉树 | 线索二叉树 | 无需递归或栈 |
| 语法分析树 | 树/二叉树 | 表示语法结构 |

---

## 5.9 复杂度总结表

| 操作 | 时间复杂度 | 空间复杂度 |
|------|-----------|-----------|
| 二叉树递归遍历 | O(n) | O(h)栈空间 |
| 二叉树非递归遍历 | O(n) | O(n) |
| 层次遍历 | O(n) | O(n)队列 |
| 由先中序构造二叉树 | O(n) | O(n) |
| 哈夫曼树构建 | O(nlogn) | O(n) |
| 并查集查找(未优化) | O(h) | O(1) |
| 并查集查找(路径压缩) | O(α(n))≈O(1) | O(1) |
| 并查集合并 | O(α(n))≈O(1) | O(1) |
| 线索二叉树找后继 | O(1) | O(1) |

---

## 5.10 常考题型与相关算法题

### 二叉树常考点

- 二叉树五种基本形态、满二叉树与完全二叉树的区别。
- `n₀ = n₂ + 1`、完全二叉树编号关系、深度公式。
- 先序 / 中序 / 后序 / 层序遍历及其手写过程。
- 由遍历序列还原二叉树时，哪些组合可以唯一确定。
- 哈夫曼树的 WPL 计算、编码生成与最优性。
- 并查集的路径压缩、按秩合并和连通性应用。

### 相关算法题

| 题目 | 训练点 |
|------|--------|
| [04 重建二叉树](/ch09-offer/04) | 由先序 + 中序还原二叉树 |
| [22 从上往下打印二叉树](/ch09-offer/22) | 层序遍历 |
| [23 二叉搜索树的后序遍历序列](/ch09-offer/23) | BST 性质判断 |
| [24 二叉树中和为某一值的路径](/ch09-offer/24) | DFS + 路径记录 |
| [39 平衡二叉树](/ch09-offer/39) | 高度计算与平衡判断 |
| [57 二叉树的下一个结点](/ch09-offer/57) | 中序后继 |
| [61 序列化二叉树](/ch09-offer/61) | 树的序列化 / 反序列化 |
| [62 二叉搜索树的第k个结点](/ch09-offer/62) | BST 中序遍历应用 |

---

## 📝 完整代码示例

```python
class TreeNode:
    """二叉树结点"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ============ 二叉树遍历 ============

def preorder_traversal(root: TreeNode) -> list:
    """先序遍历（递归）"""
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


def postorder_traversal(root: TreeNode) -> list:
    """后序遍历（递归）"""
    result = []
    def dfs(node):
        if not node:
            return
        dfs(node.left)
        dfs(node.right)
        result.append(node.val)
    dfs(root)
    return result


def level_order_traversal(root: TreeNode) -> list:
    """层次遍历"""
    from collections import deque
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


# ============ 由遍历序列构造二叉树 ============

def build_tree(preorder: list, inorder: list) -> TreeNode:
    """由先序和中序序列构造二叉树"""
    if not preorder or not inorder:
        return None
    root_val = preorder[0]
    root = TreeNode(root_val)
    root_idx = inorder.index(root_val)
    root.left = build_tree(preorder[1:1+root_idx], inorder[:root_idx])
    root.right = build_tree(preorder[1+root_idx:], inorder[root_idx+1:])
    return root


# ============ 并查集 ============

class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        root_x, root_y = self.find(x), self.find(y)
        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1


# ============ 测试代码 ============

if __name__ == "__main__":
    # 构建示例二叉树
    #        A
    #       / \
    #      B   C
    #     / \   \
    #    D   E   F
    root = TreeNode('A',
                 TreeNode('B', TreeNode('D'), TreeNode('E')),
                 TreeNode('C', None, TreeNode('F')))

    print("=" * 40)
    print("二叉树遍历测试")
    print("=" * 40)
    print(f"先序遍历: {preorder_traversal(root)}")
    print(f"中序遍历: {inorder_traversal(root)}")
    print(f"后序遍历: {postorder_traversal(root)}")
    print(f"层次遍历: {level_order_traversal(root)}")

    # 并查集测试
    print("\n" + "=" * 40)
    print("并查集测试")
    print("=" * 40)
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(2, 3)
    print(f"1和3是否连通: {uf.connected(1, 3)}")
    uf.union(1, 3)
    print(f"合并后1和3是否连通: {uf.connected(1, 3)}")
```
