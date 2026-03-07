# 408考研 · 栈、队列和数组总结

> 本文档包含栈、队列和特殊矩阵压缩存储的完整总结，涵盖各种实现方式、经典应用、手写操作过程和 Python 实现。适合 408 考研数据结构复习使用。

---

## 📊 知识点总览

| 编号 | 内容 | 文件 |
|------|------|------|
| 3.1 | 栈(顺序栈/链栈/共享栈) | `3_1_stack.py` |
| 3.2 | 队列(循环队列/链队列/双端队列) | `3_2_queue.py` |
| 3.3 | 栈的应用(括号匹配/表达式求值) | `3_3_stack_applications.py` |
| 3.4 | 特殊矩阵的压缩存储 | `3_4_matrix_compression.py` |

---

## 1. 栈 (Stack) — LIFO

**核心思想**：后进先出 (LIFO)，只允许在**栈顶**进行插入(入栈 Push)和删除(出栈 Pop)操作。

### 1.1 顺序栈

**关键步骤**（top 初始为 -1）：
1. 入栈：`top++`，然后 `data[top] = value`
2. 出栈：取 `data[top]`，然后 `top--`
3. 栈空：`top == -1`；栈满：`top == MaxSize - 1`

**手写操作过程**（依次入栈 `A, B, C` 再全部出栈）：

```
初始        → [__, __, __, __, __]  top=-1 (空栈)
Push A      → [A,  __, __, __, __]  top=0
Push B      → [A,  B,  __, __, __]  top=1
Push C      → [A,  B,  C,  __, __]  top=2
Pop → C     → [A,  B,  __, __, __]  top=1
Pop → B     → [A,  __, __, __, __]  top=0
Pop → A     → [__, __, __, __, __]  top=-1 (空栈)

出栈顺序: C, B, A (后进先出!)
```

> ⚠️ **top 初始值影响操作**：若 top 初始为 0，入栈变为 `data[top++] = value`，出栈变为 `value = data[--top]`

**Python 实现**：

```python
class SeqStack:
    def __init__(self, capacity=10):
        self.data = [None] * capacity
        self.top = -1
        self.capacity = capacity

    def push(self, value):
        """入栈: ① top++ ② data[top] = value"""
        if self.top == self.capacity - 1:
            return False  # 栈满
        self.top += 1
        self.data[self.top] = value
        return True

    def pop(self):
        """出栈: ① 取 data[top] ② top--"""
        if self.top == -1:
            return None  # 栈空
        value = self.data[self.top]
        self.top -= 1
        return value
```

### 1.2 共享栈

**核心思想**：两个栈共享一个数组。栈1从左向右增长(top1 初始-1)，栈2从右向左增长(top2 初始 MaxSize)。

**手写操作过程**（容量=8）：

```
初始        → [__, __, __, __, __, __, __, __]
               ↑top1=-1                    ↑top2=8

栈1 Push 1  → [1,  __, __, __, __, __, __, __]  top1=0
栈1 Push 2  → [1,  2,  __, __, __, __, __, __]  top1=1
栈2 Push 9  → [1,  2,  __, __, __, __, __, 9]   top2=7
栈2 Push 8  → [1,  2,  __, __, __, __, 8,  9]   top2=6

栈满条件: top1 + 1 == top2
```

---

## 2. 队列 (Queue) — FIFO

**核心思想**：先进先出 (FIFO)，队尾入队(EnQueue)，队头出队(DeQueue)。

### 2.1 循环队列

**关键步骤**：
1. 入队：`data[rear] = value`，`rear = (rear + 1) % MaxSize`
2. 出队：`value = data[front]`，`front = (front + 1) % MaxSize`
3. 利用取模运算实现"循环"

**判空/判满的三种方法**：

| 方法 | 判空 | 判满 | 代价 |
|------|------|------|------|
| 牺牲一个单元 | `front == rear` | `(rear+1) % M == front` | 浪费一个空间 |
| 增设 size 变量 | `size == 0` | `size == MaxSize` | 多一个变量 |
| 增设 tag 标志 | `front==rear && tag==0` | `front==rear && tag==1` | 多一个标志 |

**手写操作过程**（MaxSize=5，牺牲一个单元法）：

```
初始              front=0, rear=0, 队列: []
EnQueue(A)        front=0, rear=1, 队列: [A]
EnQueue(B)        front=0, rear=2, 队列: [A, B]
EnQueue(C)        front=0, rear=3, 队列: [A, B, C]
EnQueue(D)        front=0, rear=4, 队列: [A, B, C, D]
                  (rear+1)%5==0==front → 队满! 实际只存4个

DeQueue → A       front=1, rear=4, 队列: [B, C, D]
EnQueue(E)        front=1, rear=0, 队列: [B, C, D, E]  rear循环到0
                  (rear+1)%5==1==front → 又满了!

队列长度 = (rear - front + MaxSize) % MaxSize
         = (0 - 1 + 5) % 5 = 4
```

**Python 实现**：

```python
class CircularQueue:
    def __init__(self, capacity=5):
        self.data = [None] * capacity
        self.front = 0
        self.rear = 0
        self.capacity = capacity

    def is_empty(self):
        return self.front == self.rear

    def is_full(self):
        return (self.rear + 1) % self.capacity == self.front

    def enqueue(self, value):
        if self.is_full():
            return False
        self.data[self.rear] = value
        self.rear = (self.rear + 1) % self.capacity
        return True

    def dequeue(self):
        if self.is_empty():
            return None
        value = self.data[self.front]
        self.front = (self.front + 1) % self.capacity
        return value

    def length(self):
        return (self.rear - self.front + self.capacity) % self.capacity
```

---

## 3. 栈的应用

### 3.1 括号匹配

**核心思想**：遇到左括号入栈，遇到右括号弹出栈顶检查是否匹配。

**手写操作过程**（检查 `{[()]}`）：

```
字符    操作         栈状态
 {      入栈          [{]
 [      入栈          [{, []
 (      入栈          [{, [, (]
 )      弹出(匹配     [{, []
 ]      弹出[匹配     [{]
 }      弹出{匹配     []         ← 栈空，匹配成功 ✓
```

**手写操作过程**（检查 `{[}]` — 不匹配）：

```
字符    操作         栈状态
 {      入栈          [{]
 [      入栈          [{, []
 }      弹出[ ≠ }     失败 ✗     ← 括号不匹配!
```

### 3.2 中缀转后缀表达式

**核心思想**：操作数直接输出；运算符比较优先级，高的先出栈再入栈。

**手写操作过程**（中缀: `A + B * C - D`）：

```
字符    操作              栈         输出
 A      输出              []         A
 +      入栈              [+]        A
 B      输出              [+]        A B
 *      *优先级>+,入栈    [+, *]     A B
 C      输出              [+, *]     A B C
 -      弹出*,弹出+,入-   [-]        A B C * +
 D      输出              [-]        A B C * + D
结束    弹出-              []         A B C * + D -

后缀表达式: A B C * + D -
```

**Python 实现**（括号匹配）：

```python
def bracket_match(expr):
    """括号匹配检查"""
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in expr:
        if ch in '([{':
            stack.append(ch)
        elif ch in ')]}':
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return len(stack) == 0
```

---

## 4. 特殊矩阵的压缩存储

**核心思想**：利用特殊矩阵的规律，只存储有意义的元素，节省空间。

### 对称矩阵

只存储下三角 + 主对角线，共 n(n+1)/2 个元素。

**手写地址映射**（下标从1开始）：

```
矩阵 (4×4):           一维存储 B[]:
  1  5  1  3           k = i(i-1)/2 + j - 1  (i≥j, 下三角)
  5  2  4  7           k = j(j-1)/2 + i - 1  (i<j, 转置)
  1  4  3  6
  3  7  6  4           B = [1, 5, 2, 1, 4, 3, 3, 7, 6, 4]
                            ↑a11 ↑a21 ↑a22 ↑a31 ...

例: a(3,2) → k = 3×2/2 + 2 - 1 = 4  →  B[4] = 4 ✓
```

### 三对角矩阵

每行最多3个非零元素（主对角线及上下相邻对角线）。

**手写地址映射**（下标从1开始）：

```
  1  2  0  0             映射公式:
  3  4  5  0             k = 2i + j - 3
  0  6  7  8
  0  0  9  10            例: a(2,3) → k = 2×2+3-3 = 4 → B[4]=5 ✓
                          共存 3n-2 个元素
```

---

## 🧠 考研重点速记

### 栈
- **LIFO**，top 初始值影响入栈出栈代码
- **合法出栈序列**: 卡特兰数 C(2n,n)/(n+1)
- **共享栈栈满**: `top1 + 1 == top2`

### 队列
- **FIFO**，循环队列用取模实现循环
- **队列长度**: `(rear - front + MaxSize) % MaxSize`
- **判满三种方法**: 牺牲空间/size变量/tag标志

### 栈的应用
- **括号匹配**: 左括号入栈，右括号弹出检查
- **中缀转后缀**: 操作数直输出，运算符比较优先级
- **后缀表达式求值**: 遇操作数入栈，遇运算符弹两个运算

### 矩阵压缩
- **对称矩阵**: k = i(i-1)/2 + j - 1（i ≥ j）
- **三对角矩阵**: k = 2i + j - 3
- **稀疏矩阵**: 三元组表 (i, j, value)

---

## 📁 文件结构

```
3_stack_queue/
├── README.md                    # 本文档
├── 3_1_stack.py                 # 栈(顺序栈/链栈/共享栈)
├── 3_2_queue.py                 # 队列(循环队列/链队列)
├── 3_3_stack_applications.py    # 栈的应用(括号匹配/表达式)
└── 3_4_matrix_compression.py    # 特殊矩阵压缩存储
```

每个 Python 文件包含：
- 📝 算法说明文档字符串
- ⚡ 标准实现（类+方法）
- 🔍 带详细输出的 verbose 版本
- ✍️ 手写操作过程模拟
- ✅ 测试用例

运行示例：
```bash
python 3_stack_queue/3_1_stack.py
python 3_stack_queue/3_2_queue.py
python 3_stack_queue/3_3_stack_applications.py
python 3_stack_queue/3_4_matrix_compression.py
```
