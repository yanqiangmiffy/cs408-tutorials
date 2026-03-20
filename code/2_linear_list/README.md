# 408考研 · 线性表总结

> 本文档包含线性表的完整总结，涵盖顺序表、单链表、双链表、循环链表和静态链表的基本操作、手写操作过程和 Python 实现。适合 408 考研数据结构复习使用。

---

## 📊 操作对比总览

| 操作 | 顺序表 | 单链表 | 双链表 | 循环链表 |
|------|--------|--------|--------|----------|
| 按下标访问 | O(1) ✅ | O(n) | O(n) | O(n) |
| 头插 | O(n) | O(1) ✅ | O(1) ✅ | O(1) ✅ |
| 尾插 | O(1) | O(n)/O(1)* | O(1)* | O(1) ✅ |
| 按位插入 | O(n) | O(n) | O(n) | O(n) |
| 按位删除 | O(n) | O(n) | O(1)** | O(n) |
| 查找(按值) | O(n) | O(n) | O(n) | O(n) |
| 存储密度 | 高 | 低 | 更低 | 低 |

> \* 需要尾指针  \*\* 已知节点位置时
>
> **助记**：顺序表查快改慢，链表改快查慢

---

## 1. 顺序表 (Sequential List)

**核心思想**：用一组**连续**的存储单元依次存储线性表的数据元素。支持随机存取，通过地址公式 LOC(aᵢ) = LOC(a₁) + (i-1) × sizeof(ElemType) 可直接定位任意元素。

**关键步骤**：
1. 插入：从最后一个元素开始，逐个后移，腾出位置
2. 删除：从被删位置的下一个开始，逐个前移
3. 按位查找 O(1)，按值查找 O(n)

**手写操作过程**（初始: `[10, 20, 30, 40]`，在位序3插入25）：

```
初始                → [10, 20, 30, 40, __]  length=4
第1步 40后移        → [10, 20, 30, 40, 40]  data[4]=data[3]
第2步 30后移        → [10, 20, 30, 30, 40]  data[3]=data[2]
第3步 插入25到位序3 → [10, 20, 25, 30, 40]  data[2]=25
完成                → [10, 20, 25, 30, 40]  length=5
```

**手写操作过程**（删除位序2的元素 20）：

```
初始                → [10, 20, 25, 30, 40]  length=5
第1步 25前移        → [10, 25, 25, 30, 40]  data[1]=data[2]
第2步 30前移        → [10, 25, 30, 30, 40]  data[2]=data[3]
第3步 40前移        → [10, 25, 30, 40, 40]  data[3]=data[4]
完成                → [10, 25, 30, 40, __]  length=4, 返回20
```

**Python 实现**：

```python
class SequentialList:
    def __init__(self, capacity=10):
        self.data = [None] * capacity
        self.length = 0
        self.capacity = capacity

    def insert(self, index, value):
        """在第 index 个位置插入 (1-indexed)"""
        if index < 1 or index > self.length + 1:
            return False
        # 从后往前移动元素
        for j in range(self.length, index - 1, -1):
            self.data[j] = self.data[j - 1]
        self.data[index - 1] = value
        self.length += 1
        return True

    def delete(self, index):
        """删除第 index 个位置的元素 (1-indexed)"""
        if index < 1 or index > self.length:
            return None
        deleted = self.data[index - 1]
        for j in range(index - 1, self.length - 1):
            self.data[j] = self.data[j + 1]
        self.length -= 1
        return deleted

    def get_elem(self, index):
        """按位查找 O(1)"""
        return self.data[index - 1]

    def locate_elem(self, value):
        """按值查找 O(n)"""
        for i in range(self.length):
            if self.data[i] == value:
                return i + 1
        return 0
```

---

## 2. 单链表 (Singly Linked List)

**核心思想**：每个节点包含**数据域**和**指针域**(next)。头插法建表结果逆序，尾插法建表结果顺序。带头节点可简化边界处理。

**关键步骤**：
1. 头插法：新节点指向原首节点，头节点指向新节点 → 逆序
2. 尾插法：尾指针的 next 指向新节点，更新尾指针 → 顺序
3. 插入/删除的关键是找到**前驱节点**
4. 偷天换日法：在给定节点"前"插入或删除自身 → O(1)

**手写操作过程**（头插法建表: 输入 `[1, 2, 3]`）：

```
初始            → head → ∅
插入1 (头插)    → head → [1] → ∅
插入2 (头插)    → head → [2] → [1] → ∅
插入3 (头插)    → head → [3] → [2] → [1] → ∅
结果: 逆序!
```

**手写操作过程**（尾插法建表: 输入 `[1, 2, 3]`）：

```
初始            → head → ∅,  tail=head
插入1 (尾插)    → head → [1] → ∅,  tail→[1]
插入2 (尾插)    → head → [1] → [2] → ∅,  tail→[2]
插入3 (尾插)    → head → [1] → [2] → [3] → ∅,  tail→[3]
结果: 顺序!
```

**手写操作过程**（在第2个位置插入值 15）：

```
初始        → head → [10] → [20] → [30] → ∅
第1步       找到第1个节点 p = [10] (前驱)
第2步       创建新节点 s = [15]
第3步       s.next = p.next          [15] → [20]
第4步       p.next = s               [10] → [15]
结果        → head → [10] → [15] → [20] → [30] → ∅
```

> ⚠️ **注意指针修改顺序**：先让新节点指向后继 `s.next = p.next`，再让前驱指向新节点 `p.next = s`。顺序反了会导致断链！

**Python 实现**：

```python
class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = Node()  # 头节点 (不存数据)

    @staticmethod
    def from_head_insert(values):
        """头插法建表 → 逆序"""
        L = SinglyLinkedList()
        for v in values:
            s = Node(v)
            s.next = L.head.next
            L.head.next = s
        return L

    @staticmethod
    def from_tail_insert(values):
        """尾插法建表 → 顺序"""
        L = SinglyLinkedList()
        tail = L.head
        for v in values:
            s = Node(v)
            tail.next = s
            tail = s
        return L

    def insert(self, index, value):
        """在第 index 个位置插入 (1-indexed)"""
        p = self.head
        for _ in range(index - 1):
            p = p.next
        s = Node(value)
        s.next = p.next   # ① 先连后继
        p.next = s         # ② 再连前驱
```

---

## 3. 双链表 (Doubly Linked List)

**核心思想**：每个节点有 `prior` 和 `next` 两个指针，可双向遍历。已知节点时可直接找前驱，删除操作更方便。

**手写操作过程**（在节点 p 之后插入节点 s）：

```
前:  ... ↔ [p] ↔ [q] ↔ ...            q = p.next

① s.next = p.next      s → [q]       新节点连后继
② p.next.prior = s     [q] ← s       后继的前驱指向新节点
③ s.prior = p          [p] ← s       新节点连前驱
④ p.next = s           [p] → s       前驱连新节点

后:  ... ↔ [p] ↔ [s] ↔ [q] ↔ ...
```

**手写操作过程**（删除节点 p 的后继节点 q）：

```
前:  ... ↔ [p] ↔ [q] ↔ [r] ↔ ...

① p.next = q.next      [p] → [r]     前驱跳过 q
② q.next.prior = p     [p] ← [r]     后继的前驱跳过 q

后:  ... ↔ [p] ↔ [r] ↔ ...           q 被删除
```

**Python 实现**：

```python
class DNode:
    def __init__(self, data=None):
        self.data = data
        self.prior = None
        self.next = None

def insert_after(p, s):
    """在节点 p 之后插入节点 s"""
    s.next = p.next        # ① s 连后继
    if p.next:
        p.next.prior = s   # ② 后继连 s
    s.prior = p            # ③ s 连前驱
    p.next = s             # ④ 前驱连 s

def delete_next(p):
    """删除节点 p 的后继节点"""
    q = p.next
    if q is None:
        return
    p.next = q.next        # ① 前驱跳过 q
    if q.next:
        q.next.prior = p   # ② 后继跳过 q
    return q.data
```

---

## 4. 循环链表 (Circular Linked List)

**核心思想**：最后一个节点的 next 指向头节点（单循环）或首节点（不带头节点），形成环。判空和遍历终止条件与普通链表不同。

**手写示例**：

```
普通单链表:   head → [A] → [B] → [C] → ∅

循环单链表:   head → [A] → [B] → [C] ─┐
              ↑                        │
              └────────────────────────┘

循环双链表:
              ┌──────────────────────────┐
              ↓                          │
         head ↔ [A] ↔ [B] ↔ [C] ────────┘
              ↑                          │
              └──────────────────────────┘
```

| 判断条件 | 普通链表 | 循环链表 |
|----------|----------|----------|
| 表空 | `head.next == None` | `head.next == head` |
| 到表尾 | `p.next == None` | `p.next == head` |

---

## 5. 静态链表 (Static Linked List)

**核心思想**：用数组模拟链表，每个元素包含 data 和 next(游标/下标)。适用于不支持指针的语言。

**手写示例**（数组模拟链表）：

```
下标:   0     1     2     3     4     5
data:  [__]  [A]   [C]   [__]  [B]   [__]
next:  [ 1]  [ 4]  [-1]  [ 5]  [ 2]  [ 3]

逻辑顺序: 0→1→4→2  即 head → A → B → C → ∅
空闲链:   3→5→3... 即 free: 3 → 5 → ...
```

---

## 🧠 考研重点速记

### 顺序表 vs 链表

| 特性 | 顺序表 | 链表 |
|------|--------|------|
| 存取方式 | 随机存取 O(1) | 顺序存取 O(n) |
| 插入/删除 | O(n) 需移动元素 | O(1) 只改指针 |
| 存储密度 | 高 (无指针开销) | 低 (有指针域) |
| 空间分配 | 预先分配 | 动态分配 |

### 选择建议
- **表长可预估、查询多** → 顺序表
- **频繁插入删除、表长不确定** → 链表

### 插入/删除的平均移动次数
- **插入**: 平均移动 n/2 个元素
- **删除**: 平均移动 (n-1)/2 个元素
- **地址公式**: LOC(aᵢ) = LOC(a₁) + (i-1) × sizeof(ElemType)

### 链表操作要点
1. **头插法** → 逆序；**尾插法** → 顺序
2. **插入指针顺序**: 先 `s.next = p.next`，再 `p.next = s`
3. **删除**: `p.next = p.next.next`（找前驱是关键）
4. **偷天换日法**: 拷贝数据 + 操作后继节点 → O(1) 前插/删除自身

---

## 📁 文件结构

```
2_linear_list/
├── README.md                   # 本文档
├── 2_2_sequential_list.py      # 顺序表
├── 2_3_singly_linked_list.py   # 单链表
├── 2_3_doubly_linked_list.py   # 双链表
├── 2_3_circular_linked_list.py # 循环链表
└── 2_3_static_linked_list.py   # 静态链表
```

每个 Python 文件包含：
- 📝 算法说明文档字符串
- ⚡ 标准实现（类+方法）
- 🔍 带详细输出的 verbose 版本
- ✍️ 手写操作过程模拟
- ✅ 测试用例

运行示例：
```bash
python 2_linear_list/2_2_sequential_list.py
python 2_linear_list/2_3_singly_linked_list.py
python 2_linear_list/2_3_doubly_linked_list.py
python 2_linear_list/2_3_circular_linked_list.py
python 2_linear_list/2_3_static_linked_list.py
```
