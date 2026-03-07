# 408考研 · 绪论

> 本文档包含数据结构绪论的核心知识点总结，涵盖数据结构三要素、时间复杂度与空间复杂度的分析方法、手写推导过程和 Python 实现。适合 408 考研数据结构复习使用。

---

## 📊 知识点总览

| 编号 | 内容 | 文件 |
|------|------|------|
| 1.1 | 数据结构的基本概念、三要素 | `1_1_basic_concepts.py` |
| 1.2 | 算法的时间复杂度 | `1_2_time_complexity.py` |
| 1.3 | 算法的空间复杂度 | `1_3_space_complexity.py` |

---

## 1. 数据结构三要素

**核心思想**：数据结构 = 逻辑结构 + 存储结构 + 数据运算。研究数据元素之间的关系以及如何在计算机中高效存储和操作数据。

### 1.1 逻辑结构

**四种逻辑结构**的关系特征：

| 逻辑结构 | 关系 | 示例 |
|----------|------|------|
| 集合 | 无关系，仅同属一个集合 | {3, 1, 4, 5, 9} |
| 线性结构 | 一对一 | 数组、链表、栈、队列 |
| 树形结构 | 一对多 | 二叉树、B树、哈夫曼树 |
| 图状结构 | 多对多 | 有向图、无向图 |

**手写示例**：

```
集合:   { A, B, C, D }    无序，无关系

线性:   A → B → C → D    一对一，有前驱后继

         A
树形:   / \                一对多
       B   C
      / \
     D   E

图状:  A --- B             多对多
       | × |
       C --- D
```

### 1.2 存储结构

**四种存储结构**的对比：

| 存储结构 | 实现方式 | 优点 | 缺点 |
|----------|----------|------|------|
| 顺序存储 | 连续内存空间（数组） | 随机访问 O(1) | 插入/删除需移动元素 |
| 链式存储 | 指针链接各节点 | 插入/删除 O(1) | 无法随机访问 |
| 索引存储 | 数据 + 索引表 | 检索速度快 | 需要额外索引空间 |
| 散列存储 | 散列函数直接定位 | 查找 O(1) | 可能产生冲突 |

**Python 实现**（顺序存储 vs 链式存储）：

```python
# 顺序存储: 用连续内存空间
class SequentialStorage:
    def __init__(self, capacity=10):
        self.data = [None] * capacity
        self.length = 0

    def insert(self, index, value):
        for i in range(self.length, index, -1):  # 后移元素
            self.data[i] = self.data[i - 1]
        self.data[index] = value
        self.length += 1

# 链式存储: 用指针链接
class LinkedNode:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class LinkedStorage:
    def __init__(self):
        self.head = None

    def insert_head(self, value):
        node = LinkedNode(value)
        node.next = self.head   # 新节点指向原头
        self.head = node        # 更新头指针
```

---

## 2. 时间复杂度 (Time Complexity)

**核心思想**：衡量算法执行时间随问题规模 n 的增长趋势，用大 O 记号表示最坏情况上界。

**常见复杂度排序**：

O(1) < O(log n) < O(√n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2^n) < O(n!)

### 常见代码模式与复杂度

**手写分析过程**（求 T(n) 步骤：① 找基本操作 → ② 计算执行次数 → ③ 取最高阶项）：

```
例1: 加法规则 T(n) = O(max(f1, f2))
┌──────────────────────────────┐
│ for i in range(n):     # O(n) │
│     ...                       │
│ for i in range(n):           │
│     for j in range(n): # O(n²)│
│         ...                   │
│ → T(n) = O(n) + O(n²) = O(n²)│
└──────────────────────────────┘

例2: 乘法规则 T(n) = O(f1 × f2)
┌──────────────────────────────┐
│ for i in range(n):     # O(n) │
│     for j in range(i): # O(n) │
│         ...                   │
│ → 0+1+2+...+(n-1) = n(n-1)/2 │
│ → T(n) = O(n²)               │
└──────────────────────────────┘

例3: 对数时间
┌──────────────────────────────┐
│ i = n                        │
│ while i > 1:                 │
│     i = i // 2     # 每次减半│
│ → 循环 log₂n 次              │
│ → T(n) = O(log n)            │
└──────────────────────────────┘

例4: 递归
┌──────────────────────────────┐
│ def f(n):                     │
│     if n <= 1: return 1       │
│     return f(n-1) + f(n-2)    │
│ → 斐波那契递归: T(n) = O(2^n) │
│                               │
│ def f(n):                     │
│     if n <= 1: return 1       │
│     return f(n-1) + 1         │
│ → 线性递归: T(n) = O(n)       │
└──────────────────────────────┘
```

**增长速度对比**：

| n | O(1) | O(log n) | O(n) | O(n log n) | O(n²) | O(2^n) |
|---|------|----------|------|------------|-------|--------|
| 10 | 1 | 3 | 10 | 30 | 100 | 1024 |
| 100 | 1 | 7 | 100 | 700 | 10000 | 溢出 |
| 1000 | 1 | 10 | 1000 | 10000 | 10⁶ | 溢出 |

**Python 实现**：

```python
def constant_time(n):
    """O(1) - 常数时间"""
    x = n + 1      # 有限次操作
    return x * 2

def logarithmic_time(n):
    """O(log n) - 对数时间"""
    count = 0
    i = 1
    while i < n:
        i *= 2       # i: 1, 2, 4, 8, ... → 循环 log₂n 次
        count += 1
    return count

def linear_time(n):
    """O(n) - 线性时间"""
    total = 0
    for i in range(n):    # 循环 n 次
        total += i
    return total

def quadratic_time(n):
    """O(n²) - 平方时间"""
    count = 0
    for i in range(n):        # 外层 n 次
        for j in range(n):    # 内层 n 次 → 总共 n² 次
            count += 1
    return count
```

---

## 3. 空间复杂度 (Space Complexity)

**核心思想**：S(n) = O(g(n))，衡量算法执行过程中所需的**额外**存储空间（不包括输入数据本身）。

### 常见空间复杂度

**手写分析过程**：

```
O(1) 原地算法 — 只用常数个额外变量
┌──────────────────────────────┐
│ 冒泡排序:                     │
│   只用 i, j, swapped 三个变量 │
│   → S(n) = O(1)              │
└──────────────────────────────┘

O(log n) 递归栈
┌──────────────────────────────┐
│ 二分查找(递归版):              │
│   每层只用常数空间             │
│   递归深度 = log₂n            │
│   → S(n) = O(log n)          │
└──────────────────────────────┘

O(n) 辅助数组
┌──────────────────────────────┐
│ 归并排序:                     │
│   合并时需要 O(n) 辅助数组     │
│   → S(n) = O(n)              │
└──────────────────────────────┘

O(n²) 二维矩阵
┌──────────────────────────────┐
│ 邻接矩阵:                    │
│   存储 n 个顶点需 n×n 空间    │
│   → S(n) = O(n²)             │
└──────────────────────────────┘
```

**递归算法空间复杂度 = O(递归深度)**：

| 算法 | 递归深度 | 空间复杂度 |
|------|----------|-----------|
| 二分查找 | O(log n) | O(log n) |
| 快速排序(最好) | O(log n) | O(log n) |
| 快速排序(最坏) | O(n) | O(n) |
| 归并排序 | O(log n)+O(n) | O(n) |
| 斐波那契(朴素) | O(n) | O(n) |

**Python 实现**：

```python
def space_o1_example(arr):
    """O(1) - 原地冒泡排序"""
    n = len(arr)
    for i in range(n):
        swapped = False            # 额外变量1
        for j in range(n - i - 1): # 额外变量2
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True     # 额外变量3
        if not swapped:
            break
    # 只用了 i, j, swapped → S(n) = O(1)

def space_on_example(arr):
    """O(n) - 归并排序需要额外数组"""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = space_on_example(arr[:mid])
    right = space_on_example(arr[mid:])
    result = []  # 额外 O(n) 空间
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

---

## 🧠 考研重点速记

### 数据结构三要素
- **三要素**: 逻辑结构 + 存储结构 + 数据运算
- **逻辑结构**: 集合、线性、树形、图状
- **存储结构**: 顺序、链式、索引、散列
- **ADT** = 数据对象 + 数据关系 + 操作集合

### 时间复杂度
- **求解步骤**: ① 找基本操作 → ② 计算执行次数 T(n) → ③ 取最高阶项
- **加法规则**: T = T₁ + T₂ → O(max(f₁, f₂))
- **乘法规则**: T = T₁ × T₂ → O(f₁ × f₂)
- **log 底数不影响量级**（换底公式只差常数倍）
- **递归算法**用递推方程求解

### 空间复杂度
- **递归算法空间 = O(递归深度)**
- **原地算法**: S(n) = O(1)，只用常数个额外变量
- **空间换时间**: 散列表用 O(n) 空间换 O(1) 查找

### 常见复杂度排序
O(1) < O(log n) < O(√n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2^n) < O(n!)

---

## 📁 文件结构

```
1_introduction/
├── README.md                # 本文档
├── 1_1_basic_concepts.py    # 数据结构基本概念
├── 1_2_time_complexity.py   # 时间复杂度
└── 1_3_space_complexity.py  # 空间复杂度
```

每个 Python 文件包含：
- 📝 知识点说明文档字符串
- ⚡ 核心概念的代码演示
- 🔍 带详细输出的分析过程
- ✅ 考研要点速记

运行示例：
```bash
python 1_introduction/1_1_basic_concepts.py
python 1_introduction/1_2_time_complexity.py
python 1_introduction/1_3_space_complexity.py
```
