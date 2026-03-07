# 第3章 栈与队列

> **考研要点速记**：栈是后进先出(LIFO)的线性表，队列是先进先出(FIFO)的线性表；循环队列用取模运算实现，判满条件：(rear+1)%MaxSize == front。

## 1. 栈 <a id="stack"></a>

栈是只允许在一端进行插入或删除操作的线性表。栈顶(top)是允许操作的一端，栈底(bottom)是不允许操作的一端。

### 顺序栈实现

```python
class SeqStack:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.data = [None] * capacity
        self.top = -1  # top指向栈顶元素位置，-1表示空栈

    def is_empty(self):
        """判空"""
        return self.top == -1

    def is_full(self):
        """判满"""
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

两个栈共享一个数组空间，栈底分别在数组两端，栈顶向中间延伸。

```python
class SharedStack:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.data = [None] * capacity
        self.top1 = -1      # 栈1栈顶（从0开始）
        self.top2 = capacity  # 栈2栈顶（从capacity-1开始）

    def is_full(self):
        """判满：两栈顶相遇则满"""
        return self.top1 + 1 == self.top2

    def push(self, stack_num, x):
        """向指定栈入栈，stack_num为1或2"""
        if self.is_full():
            raise OverflowError("Shared stack is full")
        if stack_num == 1:
            self.top1 += 1
            self.data[self.top1] = x
        else:
            self.top2 -= 1
            self.data[self.top2] = x
```

## 2. 队列 <a id="queue"></a>

队列是只允许在一端进行插入（队尾），在另一端进行删除（队头）的线性表。

### 循环队列

解决顺序队列假溢出问题，使用取模运算实现。

```python
class CircularQueue:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.data = [None] * capacity
        self.front = 0  # 队头指针，指向队头元素
        self.rear = 0   # 队尾指针，指向队尾元素的下一个位置

    def is_empty(self):
        """判空：front == rear"""
        return self.front == self.rear

    def is_full(self):
        """判满：(rear + 1) % capacity == front"""
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

## 3. 栈的应用 <a id="applications"></a>

### 括号匹配

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

    return not stack
```

### 中缀表达式转后缀表达式

```python
def infix_to_postfix(expression: str) -> str:
    """中缀表达式转后缀表达式"""
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

## 4. 矩阵压缩 <a id="matrix"></a>

### 对称矩阵

对称矩阵满足a[i][j] = a[j][i]，只需存储下三角（或上三角）部分。

存储下标计算（行优先）：
```
k = i*(i-1)/2 + j - 1  (i >= j)
```

### 三对角矩阵

三对角矩阵的非零元素集中在主对角线及其上下两条对角线上。

存储下标计算：
```
k = 2*i + j - 3
```

## 考研重点 & 易错点

- ⚠️ 易错点：循环队列的判空和判满条件容易混淆，空时front==rear，满时(rear+1)%capacity==front
- 📌 高频考点：括号匹配、表达式求值的栈实现
- ⚠️ 易错点：共享栈的栈顶指针初始值和增长方向：栈1从-1开始向右增长，栈2从capacity开始向左增长
- 📌 高频考点：矩阵压缩存储的下标计算公式推导

## 复杂度总结表

| 操作 | 顺序栈 | 链栈 | 循环队列 | 链队列 |
|------|--------|------|----------|--------|
| 入队/入栈 | O(1) | O(1) | O(1) | O(1) |
| 出队/出栈 | O(1) | O(1) | O(1) | O(1) |
| 取队头/栈顶 | O(1) | O(1) | O(1) | O(1) |
| 空间 | 预分配 | 动态分配 | 预分配 | 动态分配 |
