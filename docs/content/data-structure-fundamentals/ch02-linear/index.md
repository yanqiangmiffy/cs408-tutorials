# 第2章 线性表

> 线性表是最常用、最简单的数据结构，是后续栈、队列、串等结构的基础。掌握顺序表和链表的实现是考研的基本要求。

---

## 1. 顺序表 <a id="sequential"></a>

**核心思想**：用一组地址连续的存储单元依次存储线性表元素，逻辑相邻=物理相邻。支持随机存取，但插入删除需要移动元素。

**关键特点**：
- 优点：随机存取O(1)、空间利用率高
- 缺点：插入删除O(n)、需预分配连续空间

### 为什么顺序表“查得快、改得慢”

可以把顺序表想成一排已经按座位号坐好的同学。

- **查找快**：因为座位连续，想找第 `i` 个元素时，直接按下标定位就行，不用一个个问过去。
- **插入慢**：中间突然插进来一个人，后面的人都得整体往后挪。
- **删除慢**：中间走掉一个人，后面的人又得整体往前补位。
- **扩容麻烦**：原地坐不下时，往往得重新找一整排更大的座位，再把原来的人整体搬过去。

### 顺序表结构

```python
class SeqList:
    """
    顺序表实现
    - data: 存储数据的数组
    - length: 实际元素个数
    - capacity: 数组总容量
    """
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.length = 0
        self.data = [None] * capacity
```

### 插入操作（手写示例）

**初始状态**：`data = [1, 2, 3, None, None]`, `length = 3`

**在 index=1 处插入 99**：

```
原始:  [1, 2, 3, None, None]
          ↑
         index=1

步骤1: 元素后移（从后往前）
       [1, 2, 3, 3, None]  (data[3] = data[2])
       [1, 2, 2, 3, None]  (data[2] = data[1])

步骤2: 插入新值
       [1, 99, 2, 3, None]  (data[1] = 99)

结果: length = 4
```

**代码实现**：

```python
def insert(self, index, value):
    """在指定位置插入元素"""
    if index < 0 or index > self.length:
        raise IndexError("Index out of range")

    # 检查是否需要扩容
    if self.length >= self.capacity:
        self._resize()

    # 元素后移（从后往前，避免覆盖）
    for i in range(self.length, index, -1):
        self.data[i] = self.data[i - 1]

    # 插入新元素
    self.data[index] = value
    self.length += 1
```

### 删除操作（手写示例）

**初始状态**：`data = [1, 99, 2, 3, None]`, `length = 4`

**删除 index=1 处的元素**：

```
原始:  [1, 99, 2, 3, None]
            ↑
         index=1

步骤1: 元素前移（从前往后）
       [1, 2, 2, 3, None]  (data[1] = data[2])
       [1, 2, 3, 3, None]  (data[2] = data[3])

步骤2: 长度减1
       有效范围: [1, 2, 3]

结果: length = 3, 返回 99
```

**代码实现**：

```python
def delete(self, index):
    """删除指定位置的元素"""
    if index < 0 or index >= self.length:
        raise IndexError("Index out of range")

    value = self.data[index]

    # 元素前移（从前往后）
    for i in range(index, self.length - 1):
        self.data[i] = self.data[i + 1]

    self.length -= 1
    return value
```

### 扩容策略

```python
def _resize(self):
    """扩容为原来的2倍"""
    self.capacity *= 2
    new_data = [None] * self.capacity
    for i in range(self.length):
        new_data[i] = self.data[i]
    self.data = new_data
```

---

## 2. 单链表 <a id="singly-linked"></a>

**核心思想**：用任意存储单元存储元素，通过指针域串联。不支持随机存取，但插入删除只需修改指针。

### 为什么链表“改得灵活、查得不快”

可以把链表想成“手拉手排队”，每个人只知道自己后面是谁。

- **插入方便**：想把新结点塞进两个人中间，只要改前后两个指针，不用搬家。
- **删除方便**：找到前驱结点后，让它直接跳过当前结点即可。
- **查找慢**：你不知道第 `i` 个结点在哪，只能从头顺着指针一个个走。
- **更适合动态变化**：元素数量经常增减时，链表通常比顺序表更从容。

### 链表结点结构

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val    # 数据域
        self.next = next  # 指针域，指向下一个结点
```

### 头插法建表（手写示例）

**特点**：每次在链表头部插入，最终链表顺序与插入顺序相反

```
插入 1:  head → [1] → None

插入 2:  head → [2] → [1] → None

插入 3:  head → [3] → [2] → [1] → None

结果: 3, 2, 1  (逆序！)
```

**代码实现**：

```python
def insert_head(self, val):
    """头插法"""
    new_node = ListNode(val)
    new_node.next = self.head
    self.head = new_node
    self.length += 1
```

### 尾插法建表（手写示例）

**特点**：每次在链表尾部插入，最终链表顺序与插入顺序相同

```
插入 1:  head → [1] → None

插入 2:  head → [1] → [2] → None

插入 3:  head → [1] → [2] → [3] → None

结果: 1, 2, 3  (正序)
```

**代码实现**：

```python
def insert_tail(self, val):
    """尾插法"""
    new_node = ListNode(val)

    if not self.head:
        # 空链表，直接作为头结点
        self.head = new_node
    else:
        # 找到尾结点
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    self.length += 1
```

### 删除操作（手写示例）

**初始链表**：`head → [1] → [2] → [3] → None`

**删除 index=1（值为2的结点）**：

```
原始:  head → [1] → [2] → [3] → None
                     ↑
              要删除的结点

步骤1: 找到前驱结点（值为1）
       prev = head

步骤2: 修改前驱的next指针
       prev.next = prev.next.next

结果:  head → [1] → [3] → None
```

**代码实现**：

```python
def delete(self, index):
    """删除指定位置结点"""
    if index < 0 or index >= self.length:
        raise IndexError("Index out of range")

    if index == 0:
        # 删除头结点
        val = self.head.val
        self.head = self.head.next
    else:
        # 找到前驱结点
        prev = self.head
        for _ in range(index - 1):
            prev = prev.next

        # 删除结点
        val = prev.next.val
        prev.next = prev.next.next

    self.length -= 1
    return val
```

---

## 3. 双链表 <a id="doubly-linked"></a>

**核心思想**：每个结点有两个指针（前驱和后继），支持双向遍历，插入删除稍复杂但处理边界更方便。

### 双链表结点结构

```python
class DoublyListNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev  # 前驱指针
        self.next = next  # 后继指针
```

### 插入操作（手写示例）

**初始链表**：`None ← [A] ↔ [B] → None`

**在 A 和 B 之间插入 C**：

```
原始:  None ← [A] ↔ [B] → None
               ↑
         要插入位置

步骤1: 新结点C的前驱指向A
       C.prev = A

步骤2: 新结点C的后继指向B
       C.next = B

步骤3: A的后继指向C
       A.next = C

步骤4: B的前驱指向C
       B.prev = C

结果:  None ← [A] ↔ [C] ↔ [B] → None
```

**代码实现**（注意顺序！）

```python
def insert_after(self, node, val):
    """在指定结点后插入新结点"""
    new_node = DoublyListNode(val)

    # 指针修改顺序很重要！
    new_node.prev = node
    new_node.next = node.next

    if node.next:
        node.next.prev = new_node

    node.next = new_node
```

### 删除操作

```python
def delete_node(self, node):
    """删除指定结点"""
    if node.prev:
        node.prev.next = node.next
    else:
        self.head = node.next

    if node.next:
        node.next.prev = node.prev
```

---

## 4. 循环链表 <a id="circular"></a>

**核心思想**：最后一个结点的指针域指向头结点，形成环。适用于需要循环访问的场景。

### 判空条件

```
空链表:  head.next == head
```

### 遍历示例

```python
def traverse_circular(head):
    """遍历循环链表"""
    if not head or head.next == head:
        return

    curr = head.next  # 从第一个结点开始
    while curr != head:
        print(curr.val)
        curr = curr.next
```

---

## 5. 静态链表 <a id="static"></a>

**核心思想**：用数组模拟链表，每个元素包含数据域和游标域（模拟指针）。适合没有指针的编程语言。

### 结构示意

```
索引:  0    1    2    3    4    5
data: [A,   B,   C,   D,   None, E]
next: [3,   0,   5,   -1,  -1,   2]  游标

head = 1

链表顺序: B → A → D → E → C → None
         ↓
        idx=1
         ↓
        idx=0
         ↓
        idx=3
         ↓
        idx=5
         ↓
        idx=2
         ↓
        idx=-1 (结束)
```

---

## 6. 考研重点 & 易错点

### 高频考点

| 考点 | 关键要点 |
|------|---------|
| **顺序表插入/删除** | 平均移动 n/2 个元素，时间复杂度 O(n) |
| **链表插入/删除** | 需要修改指针，注意边界情况 |
| **双链表指针修改** | 插入时4步操作，顺序不能乱 |
| **循环链表判空** | `head.next == head` 而非 `head == None` |
| **顺序表 vs 链表** | 根据实际场景选择 |

### 易错点

| 易错点 | 正确做法 |
|--------|---------|
| 头插法建表 | 得到的是逆序链表 |
| 链表删除头结点 | 需要单独处理，没有前驱结点 |
| 双链表指针顺序 | 修改顺序：新→前，新→后，前→新，后→新 |
| 循环链表遍历 | 终止条件是 `curr == head` 而非 `curr.next is None` |
| 静态链表游标 | -1 表示链表结束 |

### 应用场景选择

| 场景 | 推荐结构 | 原因 |
|------|----------|------|
| 需要频繁随机访问 | 顺序表 | 下标访问O(1) |
| 频繁插入删除、不常访问 | 链表 | 插入删除O(1) |
| 已知数据量，变动少 | 顺序表 | 空间连续、利用率高 |
| 数据量不确定，频繁增删 | 链表 | 动态分配、无需扩容 |
| 需要双向遍历 | 双链表 | 支持前后移动 |

---

## 7. 性能对比表

| 操作 | 顺序表 | 单链表 | 双链表 |
|------|--------|--------|--------|
| 按索引访问 | O(1) | O(n) | O(n) |
| 按值查找 | O(n) | O(n) | O(n) |
| 头部插入 | O(n) | O(1) | O(1) |
| 尾部插入 | O(1) | O(n) | O(1) |
| 已知位置插入 | O(n) | O(1) | O(1) |
| 已知位置删除 | O(n) | O(1) | O(1) |
| 空间 | 预分配连续 | 动态分散 | 动态分散 + 额外指针 |

---

## 📝 完整代码示例

```python
class SeqList:
    """顺序表完整实现"""
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.length = 0
        self.data = [None] * capacity

    def insert(self, index, value):
        if index < 0 or index > self.length:
            raise IndexError("Index out of range")
        if self.length >= self.capacity:
            self._resize()
        for i in range(self.length, index, -1):
            self.data[i] = self.data[i-1]
        self.data[index] = value
        self.length += 1

    def delete(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")
        value = self.data[index]
        for i in range(index, self.length-1):
            self.data[i] = self.data[i+1]
        self.length -= 1
        return value

    def _resize(self):
        self.capacity *= 2
        new_data = [None] * self.capacity
        for i in range(self.length):
            new_data[i] = self.data[i]
        self.data = new_data


class LinkedList:
    """单链表完整实现"""
    def __init__(self):
        self.head = None
        self.length = 0

    def insert_head(self, val):
        new_node = ListNode(val)
        new_node.next = self.head
        self.head = new_node
        self.length += 1

    def insert_tail(self, val):
        new_node = ListNode(val)
        if not self.head:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node
        self.length += 1

    def delete(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")
        if index == 0:
            val = self.head.val
            self.head = self.head.next
        else:
            prev = self.head
            for _ in range(index-1):
                prev = prev.next
            val = prev.next.val
            prev.next = prev.next.next
        self.length -= 1
        return val


if __name__ == "__main__":
    # 测试顺序表
    seq_list = SeqList(5)
    for i in range(3):
        seq_list.insert(i, i + 1)
    print(f"顺序表: {seq_list.data[:seq_list.length]}")

    # 测试链表
    linked_list = LinkedList()
    for i in range(3):
        linked_list.insert_head(i + 1)
    print(f"链表(头插): ", end="")
    curr = linked_list.head
    while curr:
        print(curr.val, end=" -> ")
        curr = curr.next
    print("None")
```

## 常考题型与相关算法题

### 常考点

- 顺序表插入、删除时元素移动次数的计算。
- 单链表头插法 / 尾插法建表过程。
- 双链表插入删除时四条指针的修改顺序。
- 循环链表判空条件和静态链表的游标思想。

### 相关算法题

| 题目 | 训练点 |
|------|--------|
| [03 从尾到头打印链表](/coding-interview-offer/03) | 链表遍历与栈思想 |
| [14 链表中倒数第k个结点](/coding-interview-offer/14) | 双指针 |
| [15 反转链表](/coding-interview-offer/15) | 指针反转 |
| [16 合并两个排序的链表](/coding-interview-offer/16) | 有序链表操作 |
| [55 链表中环的入口结点](/coding-interview-offer/55) | 快慢指针 |
| [56 删除链表中重复的结点](/coding-interview-offer/56) | 边界结点处理 |
