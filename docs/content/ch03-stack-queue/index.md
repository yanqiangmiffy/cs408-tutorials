# 第3章 栈与队列

> 栈和队列是受限的线性表，是编程中最常用的抽象数据类型。栈用于函数调用、表达式求值等场景；队列用于任务调度、广度优先搜索等场景。

---

## 1. 栈（Stack）<a id="stack"></a>

**核心思想**：后进先出（LIFO, Last-In-First-Out）。只允许在一端（栈顶）进行插入和删除操作，另一端（栈底）封闭。

**生活类比**：摞盘子，只能从最上面取放。

### 顺序栈结构

```python
class SeqStack:
    """
    顺序栈实现
    - data: 存储栈元素的数组
    - top: 栈顶指针，指向栈顶元素的位置
    - capacity: 栈的总容量
    """
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.data = [None] * capacity
        self.top = -1  # -1 表示空栈
```

### 栈操作（手写示例）

**初始状态**：`data = [None, None, None]`, `top = -1`

**入栈 push(1), push(2), push(3)**：

```
初始:       data = [None, None, None]
                   top = -1 (空栈)

push(1):     data = [  1, None, None]
                   top =  0  ↑

push(2):     data = [  1,    2, None]
                   top =  1      ↑

push(3):     data = [  1,    2,    3]
                   top =  2         ↑ (栈顶)
```

**出栈 pop() × 3**：

```
pop():       data = [  1,    2,    3]  返回 3
                   top =  1      ↑

pop():       data = [  1,    2,    3]  返回 2
                   top =  0  ↑

pop():       data = [  1,    2,    3]  返回 1
                   top = -1 (空栈)
```

### 完整代码实现

```python
class SeqStack:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.data = [None] * capacity
        self.top = -1

    def is_empty(self):
        """判空: top == -1"""
        return self.top == -1

    def is_full(self):
        """判满: top == capacity - 1"""
        return self.top == self.capacity - 1

    def push(self, x):
        """入栈"""
        if self.is_full():
            raise OverflowError("Stack overflow")
        self.top += 1
        self.data[self.top] = x

    def pop(self):
        """出栈"""
        if self.is_empty():
            raise IndexError("Stack underflow")
        x = self.data[self.top]
        self.top -= 1
        return x

    def get_top(self):
        """获取栈顶元素（不出栈）"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.data[self.top]
```

### 共享栈

**核心思想**：两个栈共享同一个数组，栈底分别在数组两端，栈顶向中间生长。

**判满条件**：`top1 + 1 == top2`（两栈顶相遇）

```
索引:   0    1    2    3    4    5    6    7
数据:  [ ,   ,   ,   ,   ,   ,   ,   ]
        ↑                              ↑
       top1=-1                        top2=8
       栈1底                         栈2底

栈1向右生长 ←→ 栈2向左生长
```

```python
class SharedStack:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.data = [None] * capacity
        self.top1 = -1         # 栈1栈顶（从0开始）
        self.top2 = capacity    # 栈2栈顶（从capacity-1开始）

    def is_full(self):
        """判满：两栈顶相遇"""
        return self.top1 + 1 == self.top2

    def push(self, stack_num, x):
        """stack_num: 1或2"""
        if self.is_full():
            raise OverflowError("Shared stack is full")

        if stack_num == 1:
            self.top1 += 1
            self.data[self.top1] = x
        else:
            self.top2 -= 1
            self.data[self.top2] = x

    def pop(self, stack_num):
        if stack_num == 1:
            if self.top1 == -1:
                raise IndexError("Stack 1 is empty")
            x = self.data[self.top1]
            self.top1 -= 1
        else:
            if self.top2 == self.capacity:
                raise IndexError("Stack 2 is empty")
            x = self.data[self.top2]
            self.top2 += 1
        return x
```

---

## 2. 队列（Queue）<a id="queue"></a>

**核心思想**：先进先出（FIFO, First-In-First-Out）。只允许在一端（队尾）插入，另一端（队头）删除。

**生活类比**：排队买票，先来先走。

### 循环队列

**核心思想**：把数组看成环形，通过取模运算 `%` 实现指针循环移动。解决"假溢出"问题。

**假溢出问题**：队尾已到数组末尾但队头前面有空位，无法继续入队。

#### 循环队列指针示意

```
索引:   0    1    2    3    4    5    6    7
数据:  [A,   B,   C,   D,   ,   ,   ,   ]
        ↑                        ↑
       front                    rear

front指向队头元素，rear指向队尾元素的下一个位置

有效长度 = (rear - front + capacity) % capacity = 4
```

#### 循环队列操作（手写示例）

**初始**：`capacity = 5`, `front = 0`, `rear = 0`（空队列）

**入队 enqueue(1), enqueue(2), enqueue(3)**：

```
初始:       [ ,   ,   ,   ,   ]
            ↑↑
           rear/front (空队列)

enqueue(1): [1,   ,   ,   ,   ]
            ↑    ↑
           front rear

enqueue(2): [1,   2,   ,   ,   ]
            ↑         ↑
           front     rear

enqueue(3): [1,   2,   3,   ,   ]
            ↑              ↑
           front          rear
```

**出队 dequeue()**：

```
dequeue():  [1,   2,   3,   ,   ]  返回1
                 ↑    ↑
               front rear
```

**循环入队 enqueue(4), enqueue(5)**：

```
enqueue(4): [1,   2,   3,   4,   ]
                 ↑         ↑
               front     rear

enqueue(5): [1,   2,   3,   4,   5]
                 ↑              ↑
               front          rear
```

**循环出队 dequeue(), enqueue(6)**：

```
dequeue():  [1,   2,   3,   4,   5]  返回2
                      ↑         ↑
                    front     rear

enqueue(6): [6,   2,   3,   4,   5]  rear循环到0
                      ↑    ↑
                    rear front
```

#### 完整代码实现

```python
class CircularQueue:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.data = [None] * capacity
        self.front = 0  # 队头指针
        self.rear = 0   # 队尾指针

    def is_empty(self):
        """判空: front == rear"""
        return self.front == self.rear

    def is_full(self):
        """判满: (rear + 1) % capacity == front"""
        # 牺牲一个空间区分空和满
        return (self.rear + 1) % self.capacity == self.front

    def size(self):
        """队列长度"""
        return (self.rear - self.front + self.capacity) % self.capacity

    def enqueue(self, x):
        """入队"""
        if self.is_full():
            raise OverflowError("Queue is full")
        self.data[self.rear] = x
        self.rear = (self.rear + 1) % self.capacity

    def dequeue(self):
        """出队"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        x = self.data[self.front]
        self.front = (self.front + 1) % self.capacity
        return x

    def get_front(self):
        """获取队头元素"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.data[self.front]
```

---

## 3. 栈的应用 <a id="applications"></a>

### 括号匹配

**核心思想**：遇到左括号入栈，遇到右括号出栈并匹配，最后栈为空则匹配成功。

**手写示例**：检查 `{[()]}` 是否匹配

```
字符栈分析:
'{'  入栈 → ['{'        栈: {
'['  入栈 → ['{', '[']    栈: {[
'('  入栈 → ['{', '[', '('] 栈: {[
')'  出栈匹配 → ['{', '[']  栈: {[  匹配成功
']'  出栈匹配 → ['{']        栈: {  匹配成功
'}'  出栈匹配 → []             栈:    匹配成功

结果: 栈为空 → 匹配成功！
```

**手写示例**：检查 `{[)}` 是否匹配

```
字符栈分析:
'{'  入栈 → ['{']        栈: {
'['  入栈 → ['{', '[']    栈: {[
')'  出栈匹配 → 失败！(预期']'，实际')')

结果: 不匹配！
```

```python
def is_valid_parentheses(s: str) -> bool:
    """检查括号是否匹配"""
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in mapping:  # 右括号
            top = stack.pop() if stack else '#'
            if top != mapping[char]:
                return False
        else:  # 左括号
            stack.append(char)

    return not stack  # 栈为空则全部匹配
```

### 中缀表达式转后缀表达式

**核心思想**：用栈存储运算符，按优先级处理。后缀表达式（逆波兰）没有括号，可以直接计算。

**运算符优先级**：`'(' > '^' > '*/' > '+-'`

**手写示例**：`a + b * (c - d) / e`

```
字符    操作数栈    运算符栈    输出
-----------------------------------------
'a'     -          -          a
'+'     -          +          a
'b'     -          +          a b
'*'     -          + *        a b
'('     -          + * (      a b
'c'     -          + * (      a b c
'-'     -          + * ( -    a b c
'd'     -          + * ( -    a b c d
')'     弹出直到(   + *        a b c d -
'/'     /优先<*    + /        a b c d -
'e'     -          + /        a b c d - e
结束     弹出全部     -          a b c d - e * / +

结果: a b c d - e * / +
```

```python
def infix_to_postfix(expression: str) -> str:
    """中缀转后缀表达式"""
    stack = []
    result = []
    priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    i = 0
    while i < len(expression):
        ch = expression[i]

        if ch.isalnum():  # 操作数
            num = ch
            while i + 1 < len(expression) and expression[i+1].isalnum():
                i += 1
                num += expression[i]
            result.append(num)

        elif ch == '(':
            stack.append(ch)

        elif ch == ')':
            while stack and stack[-1] != '(':
                result.append(stack.pop())
            stack.pop()  # 弹出'('

        else:  # 运算符
            while (stack and stack[-1] != '(' and
                   stack[-1] in priority and
                   priority[stack[-1]] >= priority[ch]):
                result.append(stack.pop())
            stack.append(ch)

        i += 1

    while stack:
        result.append(stack.pop())

    return ' '.join(result)
```

---

## 4. 矩阵压缩 <a id="matrix"></a>

**核心思想**：利用矩阵的特殊结构（对称、带状）减少存储空间。

### 对称矩阵

**特点**：`a[i][j] = a[j][i]`，只存储下三角（或上三角）部分。

**存储策略**：用一维数组按行优先存储下三角元素。

**下标计算公式**：
```
k = i * (i - 1) / 2 + j - 1   (i >= j, 行优先)
```

**示例**：4阶对称矩阵

```
原始矩阵 (4×4，需16个单元):
    0   1   2   3
0  [ 1   2   3   4 ]
1  [ 2   5   6   7 ]
2  [ 3   6   8   9 ]
3  [ 4   7   9  10 ]

压缩后 (下三角，10个单元):
索引:  0   1   2   3   4   5   6   7   8   9
数据: [ 1,  2,  5,  3,  6,  8,  4,  7,  9, 10 ]
      ↓
     i=0,j=0
        ↓↓
      i=1,j=0  i=1,j=1

访问 a[2][1] (i=2,j=1):
k = 2×(2-1)/2 + 1 - 1 = 1 + 0 = 1
data[1] = 5 ✓
```

### 三对角矩阵

**特点**：非零元素集中在主对角线及其上下两条对角线上。

**存储策略**：用一维数组按行优先存储非零元素。

**下标计算公式**：
```
k = 2 * i + j - 3
```

**示例**：5阶三对角矩阵

```
原始矩阵 (5×5):
    0   1   2   3   4
0  [ 0   2   3   0   0 ]
1  [ 1   0   4   5   0 ]
2  [ 0   6   0   7   8 ]
3  [ 0   0   9   0  10 ]
4  [ 0   0   0  11   0 ]

压缩后 (存储三条对角线):
索引:  0   1   2   3   4   5   6   7   8   9  10  11  12
数据: [ 2,  3,  1,  4,  5,  6,  7,  8,  9, 10, 11 ]

访问 a[2][1] (i=2,j=1):
k = 2×2 + 1 - 3 = 2
data[2] = 6 ✓
```

---

## 5. 考研重点 & 易错点

### 高频考点

| 考点 | 关键要点 |
|------|---------|
| **栈和队列的特点** | 栈LIFO，队列FIFO |
| **循环队列判空/判满** | 空：front==rear；满：(rear+1)%capacity==front |
| **括号匹配** | 左括号入栈，右括号出栈匹配 |
| **表达式转换** | 按优先级处理运算符 |
| **矩阵压缩** | 对称矩阵和三对角矩阵的下标计算 |

### 易错点

| 易错点 | 正确做法 |
|--------|---------|
| 循环队列判空/判满 | 判满牺牲一个空间，或加size标记 |
| 共享栈的栈顶指针 | 栈1从-1向右，栈2从capacity向左 |
| 栈溢出/下溢 | 入栈前判满，出栈前判空 |
| 矩阵压缩下标 | 对称矩阵：i*(i-1)/2 + j - 1 |
| 表达式转换括号 | 遇到'('入栈，遇到')'弹出至'(' |

### 应用场景

| 场景 | 数据结构 | 原因 |
|------|----------|------|
| 函数调用 | 栈 | 后调用先返回 |
| 撤销操作 | 栈 | 后操作先撤销 |
| 表达式求值 | 栈 | 运算符优先级 |
| 任务调度 | 队列 | 先来先服务 |
| 广度优先搜索 | 队列 | 层序遍历 |
| 缓冲区 | 循环队列 | 空间复用 |

---

## 6. 复杂度总结表

| 操作 | 顺序栈 | 链栈 | 循环队列 | 链队列 |
|------|--------|------|----------|--------|
| 入栈/入队 | O(1) | O(1) | O(1) | O(1) |
| 出栈/出队 | O(1) | O(1) | O(1) | O(1) |
| 取栈顶/队头 | O(1) | O(1) | O(1) | O(1) |
| 判空/判满 | O(1) | O(1) | O(1) | O(1) |
| 空间 | 预分配 | 动态分配 | 预分配 | 动态分配 |

---

## 📝 完整代码示例

```python
class SeqStack:
    """顺序栈"""
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.data = [None] * capacity
        self.top = -1

    def push(self, x):
        if self.top == self.capacity - 1:
            raise OverflowError("Stack overflow")
        self.top += 1
        self.data[self.top] = x

    def pop(self):
        if self.top == -1:
            raise IndexError("Stack underflow")
        x = self.data[self.top]
        self.top -= 1
        return x


class CircularQueue:
    """循环队列"""
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.data = [None] * capacity
        self.front = 0
        self.rear = 0

    def enqueue(self, x):
        if (self.rear + 1) % self.capacity == self.front:
            raise OverflowError("Queue is full")
        self.data[self.rear] = x
        self.rear = (self.rear + 1) % self.capacity

    def dequeue(self):
        if self.front == self.rear:
            raise IndexError("Queue is empty")
        x = self.data[self.front]
        self.front = (self.front + 1) % self.capacity
        return x


def is_valid_parentheses(s: str) -> bool:
    """括号匹配"""
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if top != mapping[char]:
                return False
        else:
            stack.append(char)
    return not stack


if __name__ == "__main__":
    # 测试栈
    stack = SeqStack(5)
    for i in range(3):
        stack.push(i + 1)
    print(f"栈顶元素: {stack.data[stack.top]}")

    # 测试括号匹配
    print(f"{{[()]}} 是否匹配: {is_valid_parentheses('{[()]}')}")
    print(f"{{[)}} 是否匹配: {is_valid_parentheses('{[)')}")
```

## 常考题型与相关算法题

### 常考点

- 顺序栈判空 `top == -1` 与判满条件。
- 循环队列判空 `front == rear`、判满 `(rear + 1) % MaxSize == front`。
- 中缀转后缀时运算符优先级与括号处理。
- 栈的应用：括号匹配、表达式求值、单调栈。

### 相关算法题

| 题目 | 训练点 |
|------|--------|
| [05 用两个栈实现队列](/ch09-offer/05) | 栈与队列互相模拟 |
| [20 包含min函数的栈](/ch09-offer/20) | 辅助栈 |
| [21 栈的压入、弹出序列](/ch09-offer/21) | 栈序列合法性 |
| LeetCode 20. 有效的括号 | 栈的经典应用 |
| LeetCode 150. 逆波兰表达式求值 | 后缀表达式 |
| LeetCode 239. 滑动窗口最大值 | 队列 / 单调队列 |
