"""
队列 (Queue)

核心概念: 先进先出 (FIFO - First In First Out)
只允许在队尾入队、队头出队

两种实现:
  1. 循环队列 (顺序实现): 用数组 + 取模实现循环
  2. 链队列: 用链表实现，front 指向队头，rear 指向队尾

时间复杂度: 入队/出队 均为 O(1)

考研要点:
  - 循环队列判空/判满的三种方法
  - 循环队列的队列长度公式
  - 双端队列的概念
"""


# ==========================================
# 1. 循环队列 (牺牲一个存储单元)
# ==========================================

class CircularQueue:
    """循环队列 - 牺牲一个单元区分队空和队满

    队空: front == rear
    队满: (rear + 1) % MaxSize == front
    队长: (rear - front + MaxSize) % MaxSize
    """

    def __init__(self, capacity=6):
        self.data = [None] * capacity
        self.front = 0  # 指向队头元素
        self.rear = 0   # 指向队尾元素的下一个位置
        self.capacity = capacity

    def is_empty(self):
        return self.front == self.rear

    def is_full(self):
        return (self.rear + 1) % self.capacity == self.front

    def enqueue(self, value):
        """入队"""
        if self.is_full():
            print(f"  队满! 无法入队 {value}")
            return False
        self.data[self.rear] = value
        self.rear = (self.rear + 1) % self.capacity  # 取模循环
        return True

    def dequeue(self):
        """出队"""
        if self.is_empty():
            print(f"  队空!")
            return None
        value = self.data[self.front]
        self.front = (self.front + 1) % self.capacity
        return value

    def peek(self):
        if self.is_empty():
            return None
        return self.data[self.front]

    def size(self):
        return (self.rear - self.front + self.capacity) % self.capacity

    def display(self):
        result = []
        i = self.front
        while i != self.rear:
            result.append(self.data[i])
            i = (i + 1) % self.capacity
        return result


# ==========================================
# 2. 循环队列 (使用 size 变量)
# ==========================================

class CircularQueueWithSize:
    """循环队列 - 用 size 区分队空和队满

    不浪费存储单元
    队空: size == 0
    队满: size == MaxSize
    """

    def __init__(self, capacity=5):
        self.data = [None] * capacity
        self.front = 0
        self.rear = 0
        self._size = 0
        self.capacity = capacity

    def is_empty(self):
        return self._size == 0

    def is_full(self):
        return self._size == self.capacity

    def enqueue(self, value):
        if self.is_full():
            return False
        self.data[self.rear] = value
        self.rear = (self.rear + 1) % self.capacity
        self._size += 1
        return True

    def dequeue(self):
        if self.is_empty():
            return None
        value = self.data[self.front]
        self.front = (self.front + 1) % self.capacity
        self._size -= 1
        return value

    def size(self):
        return self._size


# ==========================================
# 3. 链队列
# ==========================================

class QueueNode:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedQueue:
    """链队列 (带头节点)"""

    def __init__(self):
        self.head = QueueNode()   # 头节点
        self.front = self.head    # front 指向头节点
        self.rear = self.head     # rear 指向头节点

    def is_empty(self):
        return self.front == self.rear

    def enqueue(self, value):
        """入队: 在队尾插入"""
        node = QueueNode(value)
        self.rear.next = node
        self.rear = node

    def dequeue(self):
        """出队: 删除队头元素

        注意: 如果删除的是最后一个元素，需要修改 rear
        """
        if self.is_empty():
            return None
        p = self.front.next  # 队头元素
        self.front.next = p.next
        if self.rear == p:   # 如果删的是最后一个
            self.rear = self.front
        return p.data

    def peek(self):
        if self.is_empty():
            return None
        return self.front.next.data

    def display(self):
        result = []
        p = self.front.next
        while p:
            result.append(p.data)
            p = p.next
        return result


# ==========================================
# 4. 双端队列
# ==========================================

class Deque:
    """双端队列: 两端都可以入队和出队

    特殊限制:
    - 输入受限的双端队列: 只允许一端入队，两端出队
    - 输出受限的双端队列: 两端入队，只允许一端出队
    """

    def __init__(self):
        self.data = []

    def push_front(self, value):
        """队头入队"""
        self.data.insert(0, value)

    def push_rear(self, value):
        """队尾入队"""
        self.data.append(value)

    def pop_front(self):
        """队头出队"""
        if not self.data:
            return None
        return self.data.pop(0)

    def pop_rear(self):
        """队尾出队"""
        if not self.data:
            return None
        return self.data.pop()

    def display(self):
        return list(self.data)


def circular_queue_demo():
    """循环队列演示"""
    print("=" * 60)
    print("循环队列")
    print("=" * 60)

    cq = CircularQueue(6)  # 实际可用 5 个位置
    print(f"\n  容量={cq.capacity}, 可用={cq.capacity - 1}")

    for v in [10, 20, 30, 40, 50]:
        ok = cq.enqueue(v)
        status = "✓" if ok else "✗ 队满"
        print(f"  入队 {v}: {status} → {cq.display()}, "
              f"front={cq.front}, rear={cq.rear}")

    print()
    for _ in range(3):
        v = cq.dequeue()
        print(f"  出队 {v} → {cq.display()}, "
              f"front={cq.front}, rear={cq.rear}")

    # 继续入队 (体现循环)
    for v in [60, 70, 80]:
        ok = cq.enqueue(v)
        status = "✓" if ok else "✗ 队满"
        print(f"  入队 {v}: {status} → {cq.display()}, "
              f"front={cq.front}, rear={cq.rear}")

    print(f"\n  队列长度 = (rear - front + capacity) % capacity")
    print(f"           = ({cq.rear} - {cq.front} + {cq.capacity}) % {cq.capacity} = {cq.size()}")
    print()


def linked_queue_demo():
    """链队列演示"""
    print("=" * 60)
    print("链队列")
    print("=" * 60)

    lq = LinkedQueue()
    for v in ['A', 'B', 'C', 'D']:
        lq.enqueue(v)
        print(f"  入队 {v}: {lq.display()}")

    while not lq.is_empty():
        v = lq.dequeue()
        print(f"  出队 {v}: {lq.display()}")
    print()


def deque_demo():
    """双端队列演示"""
    print("=" * 60)
    print("双端队列")
    print("=" * 60)

    dq = Deque()
    print(f"\n  --- 操作序列 ---")
    dq.push_rear(1)
    print(f"  队尾入 1: {dq.display()}")
    dq.push_rear(2)
    print(f"  队尾入 2: {dq.display()}")
    dq.push_front(0)
    print(f"  队头入 0: {dq.display()}")
    dq.push_rear(3)
    print(f"  队尾入 3: {dq.display()}")

    v = dq.pop_front()
    print(f"  队头出 {v}: {dq.display()}")
    v = dq.pop_rear()
    print(f"  队尾出 {v}: {dq.display()}")

    print(f"""
  双端队列的特殊限制:
  ┌─────────────────────────────────────────┐
  │ 输入受限: 只能从一端入队，两端都可出队   │
  │ 输出受限: 两端都可入队，只能从一端出队   │
  │ 栈: 只能从一端入队+出队 (特殊的双端队列) │
  └─────────────────────────────────────────┘
    """)


if __name__ == "__main__":
    circular_queue_demo()
    linked_queue_demo()
    deque_demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 循环队列三种判空满方法:
     ① 牺牲一个单元: 空 front==rear, 满 (rear+1)%M==front
     ② 增加 size: 空 size==0, 满 size==MaxSize
     ③ 增加 tag: 空 tag==0且front==rear, 满 tag==1且front==rear

  2. 循环队列长度:
     length = (rear - front + MaxSize) % MaxSize

  3. 链队列:
     入队: rear.next = new_node; rear = new_node
     出队: front.next = front.next.next
     注意: 删除最后一个元素时要修改 rear!

  4. 双端队列:
     判断合法输出序列时，注意是否有限制
    """)
