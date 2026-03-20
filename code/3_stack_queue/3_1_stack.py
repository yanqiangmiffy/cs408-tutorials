"""
栈 (Stack)

核心概念: 后进先出 (LIFO - Last In First Out)
只允许在栈顶进行插入和删除操作

两种实现:
  1. 顺序栈: 用数组实现，top 指针指向栈顶
  2. 链栈: 用链表实现，头节点为栈顶

时间复杂度: 入栈/出栈/取栈顶 均为 O(1)

考研要点:
  - 顺序栈 top 的初始值 (-1 或 0) 影响入栈出栈操作
  - 共享栈: 两个栈共享一个数组，栈满条件
  - n 个不同元素入栈，出栈序列的合法性判断
  - 卡特兰数: C(2n,n)/(n+1) 种合法出栈序列
"""


# ==========================================
# 1. 顺序栈
# ==========================================

class SeqStack:
    """顺序栈 (top 初始为 -1)"""

    def __init__(self, capacity=10):
        self.data = [None] * capacity
        self.top = -1           # 栈顶指针，-1 表示空栈
        self.capacity = capacity

    def is_empty(self):
        return self.top == -1

    def is_full(self):
        return self.top == self.capacity - 1

    def push(self, value):
        """入栈: ① top++  ② data[top] = value"""
        if self.is_full():
            print(f"  栈满! 无法入栈 {value}")
            return False
        self.top += 1
        self.data[self.top] = value
        return True

    def pop(self):
        """出栈: ① 取 data[top]  ② top--"""
        if self.is_empty():
            print(f"  栈空! 无法出栈")
            return None
        value = self.data[self.top]
        self.top -= 1
        return value

    def peek(self):
        """取栈顶元素 (不出栈)"""
        if self.is_empty():
            return None
        return self.data[self.top]

    def display(self):
        return list(self.data[:self.top + 1])

    def __len__(self):
        return self.top + 1


# ==========================================
# 2. 链栈
# ==========================================

class LinkNode:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkStack:
    """链栈 (不带头节点，栈顶为链表头)"""

    def __init__(self):
        self.top = None
        self.length = 0

    def is_empty(self):
        return self.top is None

    def push(self, value):
        """入栈: 头插"""
        node = LinkNode(value)
        node.next = self.top
        self.top = node
        self.length += 1

    def pop(self):
        """出栈: 删除头节点"""
        if self.is_empty():
            return None
        value = self.top.data
        self.top = self.top.next
        self.length -= 1
        return value

    def peek(self):
        if self.is_empty():
            return None
        return self.top.data

    def display(self):
        result = []
        p = self.top
        while p:
            result.append(p.data)
            p = p.next
        return result  # 栈顶在前


# ==========================================
# 3. 共享栈
# ==========================================

class SharedStack:
    """共享栈: 两个栈共享一个数组

    栈1: 从左往右增长，top1 初始为 -1
    栈2: 从右往左增长，top2 初始为 capacity
    栈满条件: top1 + 1 == top2
    """

    def __init__(self, capacity=10):
        self.data = [None] * capacity
        self.top1 = -1
        self.top2 = capacity
        self.capacity = capacity

    def push(self, stack_id, value):
        if self.top1 + 1 == self.top2:
            print(f"  共享栈已满!")
            return False
        if stack_id == 1:
            self.top1 += 1
            self.data[self.top1] = value
        else:
            self.top2 -= 1
            self.data[self.top2] = value
        return True

    def pop(self, stack_id):
        if stack_id == 1:
            if self.top1 == -1:
                return None
            value = self.data[self.top1]
            self.top1 -= 1
        else:
            if self.top2 == self.capacity:
                return None
            value = self.data[self.top2]
            self.top2 += 1
        return value

    def display(self):
        s1 = self.data[:self.top1 + 1]
        s2 = self.data[self.top2:][::-1]
        return s1, s2


def stack_demo():
    """栈基本操作演示"""
    print("=" * 60)
    print("栈的基本操作")
    print("=" * 60)

    # 顺序栈
    print("\n  --- 顺序栈 ---")
    s = SeqStack(5)
    for v in [10, 20, 30]:
        s.push(v)
        print(f"  入栈 {v}: {s.display()}, top={s.top}")

    print(f"  栈顶元素: {s.peek()}")
    while not s.is_empty():
        v = s.pop()
        print(f"  出栈 {v}: {s.display()}")

    # 链栈
    print("\n  --- 链栈 ---")
    ls = LinkStack()
    for v in ['A', 'B', 'C']:
        ls.push(v)
        print(f"  入栈 {v}: {ls.display()}")

    while not ls.is_empty():
        v = ls.pop()
        print(f"  出栈 {v}: {ls.display()}")

    # 共享栈
    print("\n  --- 共享栈 ---")
    ss = SharedStack(8)
    for v in [1, 2, 3]:
        ss.push(1, v)
    for v in [9, 8, 7]:
        ss.push(2, v)
    s1, s2 = ss.display()
    print(f"  栈1: {s1}")
    print(f"  栈2: {s2}")
    print(f"  栈满条件: top1+1 == top2 → {ss.top1 + 1} == {ss.top2}? {ss.top1 + 1 == ss.top2}")

    print()


def valid_sequence_demo():
    """判断出栈序列的合法性"""
    print("=" * 60)
    print("出栈序列合法性判断")
    print("=" * 60)

    def is_valid_pop_sequence(push_seq, pop_seq):
        """判断 pop_seq 是否是 push_seq 的合法出栈序列"""
        stack = []
        j = 0
        for v in push_seq:
            stack.append(v)
            while stack and j < len(pop_seq) and stack[-1] == pop_seq[j]:
                stack.pop()
                j += 1
        return j == len(pop_seq)

    push_seq = [1, 2, 3, 4, 5]
    test_cases = [
        [4, 5, 3, 2, 1],  # ✓
        [4, 3, 5, 1, 2],  # ✗
        [1, 2, 3, 4, 5],  # ✓
        [5, 4, 3, 2, 1],  # ✓
        [3, 1, 2, 4, 5],  # ✗
    ]

    print(f"\n  入栈序列: {push_seq}")
    for pop_seq in test_cases:
        valid = is_valid_pop_sequence(push_seq, pop_seq)
        mark = "✓" if valid else "✗"
        print(f"  {mark} 出栈序列 {pop_seq}")

    print(f"\n  卡特兰数: n=5 时合法序列数 = C(10,5)/6 = 42")
    print()


if __name__ == "__main__":
    stack_demo()
    valid_sequence_demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 顺序栈操作 (top 初始 -1):
     入栈: s.data[++s.top] = x
     出栈: x = s.data[s.top--]
     栈空: top == -1
     栈满: top == MaxSize - 1

  2. 顺序栈操作 (top 初始 0):
     入栈: s.data[s.top++] = x
     出栈: x = s.data[--s.top]
     栈空: top == 0
     栈满: top == MaxSize

  3. 共享栈:
     栈满: top1 + 1 == top2
     栈1空: top1 == -1
     栈2空: top2 == MaxSize

  4. 卡特兰数:
     n 个元素入栈，合法出栈序列数 = C(2n,n)/(n+1)
    """)
