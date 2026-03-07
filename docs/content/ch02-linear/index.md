# 第2章 线性表

> **考研要点速记**：线性表是n个数据元素的有限序列；顺序表支持随机存取，插入删除操作时间复杂度O(n)；链表不支持随机存取，插入删除操作只需修改指针，时间复杂度O(1)（已知位置）。

## 1. 顺序表 <a id="sequential"></a>

顺序表是用一组地址连续的存储单元依次存储线性表中的数据元素，使得逻辑上相邻的元素在物理位置上也相邻。

### 基本操作实现

```python
class SeqList:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.length = 0
        self.data = [None] * capacity

    def insert(self, index, value):
        """在指定位置插入元素"""
        if index < 0 or index > self.length:
            raise IndexError("Index out of range")
        if self.length >= self.capacity:
            self._resize()
        # 元素后移
        for i in range(self.length, index, -1):
            self.data[i] = self.data[i-1]
        self.data[index] = value
        self.length += 1

    def delete(self, index):
        """删除指定位置的元素"""
        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")
        value = self.data[index]
        # 元素前移
        for i in range(index, self.length-1):
            self.data[i] = self.data[i+1]
        self.length -= 1
        return value

    def _resize(self):
        """扩容为原来的2倍"""
        self.capacity *= 2
        new_data = [None] * self.capacity
        for i in range(self.length):
            new_data[i] = self.data[i]
        self.data = new_data
```

**时间复杂度**：
- 插入/删除：O(n)（平均需要移动n/2个元素）
- 随机访问：O(1)
- 扩容：O(n)（摊还分析为O(1)）

## 2. 单链表 <a id="singly-linked"></a>

单链表是用任意的存储单元存储线性表中的数据元素，每个结点包含数据域和指向下一个结点的指针域。

### 基本操作实现

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None
        self.length = 0

    def insert_head(self, val):
        """头插法"""
        new_node = ListNode(val)
        new_node.next = self.head
        self.head = new_node
        self.length += 1

    def insert_tail(self, val):
        """尾插法"""
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
        """删除指定位置结点"""
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
```

## 3. 双链表 <a id="doubly-linked"></a>

双链表的每个结点有两个指针，分别指向其前驱结点和后继结点，可以方便地进行双向遍历。

**插入操作指针修改顺序（重点！）**：
1. 新结点的前驱指向要插入位置的前驱
2. 新结点的后继指向要插入位置的后继
3. 前驱结点的后继指向新结点
4. 后继结点的前驱指向新结点

## 4. 循环链表 <a id="circular"></a>

循环链表的最后一个结点的指针域指向头结点，整个链表形成一个环。判空条件：`head.next == head`。

## 5. 静态链表 <a id="static"></a>

静态链表用数组模拟链表，每个数组元素包含数据域和游标域，游标指示下一个元素在数组中的位置，适合没有指针的编程语言。

## 考研重点 & 易错点

- ⚠️ 易错点：头插法和尾插法建表的区别，头插法得到的链表是逆序的
- 📌 高频考点：链表的插入、删除操作，尤其是边界情况（头结点、尾结点处理）
- ⚠️ 易错点：双链表插入删除时的指针修改顺序，容易丢失指针
- 📌 高频考点：顺序表和链表的对比与应用场景选择

## 顺序表 vs 链表对比表

| 性能指标 | 顺序表 | 链表 |
|----------|--------|------|
| 存取方式 | 随机存取 | 顺序存取 |
| 查找（按值） | O(n) | O(n) |
| 查找（按索引） | O(1) | O(n) |
| 插入/删除（已知位置） | O(n) | O(1) |
| 空间利用率 | 高（连续存储） | 低（指针开销） |
| 扩容 | 耗时（需要复制元素） | 方便（只需分配结点） |
