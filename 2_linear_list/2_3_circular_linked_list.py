"""
循环链表 (Circular Linked List)

1. 循环单链表: 最后一个节点的 next 指向头节点
2. 循环双链表: 最后一个节点的 next 指向头节点，头节点的 prior 指向最后一个节点

特点:
  - 从任一节点出发都可以遍历整个链表
  - 判空条件不同于普通链表
  - 常用「尾指针」表示循环单链表 (方便 O(1) 访问首尾)

考研要点:
  - 判空条件: head.next == head (而非 head.next == None)
  - 循环单链表用尾指针的优势
  - 两个循环链表的合并操作
"""


# ==========================================
# 循环单链表
# ==========================================

class CSNode:
    """循环单链表节点"""
    def __init__(self, data=None):
        self.data = data
        self.next = None


class CircularSinglyLinkedList:
    """带头节点的循环单链表"""
    def __init__(self):
        self.head = CSNode()
        self.head.next = self.head  # 空表: head.next 指向自己

    def is_empty(self):
        """判空: head.next == head"""
        return self.head.next == self.head

    def insert_tail(self, value):
        """尾插法"""
        node = CSNode(value)
        p = self.head
        while p.next != self.head:
            p = p.next
        node.next = self.head
        p.next = node

    def display(self):
        if self.is_empty():
            return []
        result = []
        p = self.head.next
        while p != self.head:
            result.append(p.data)
            p = p.next
        return result

    def display_circular(self):
        if self.is_empty():
            return "H → (H)"
        parts = ["H"]
        p = self.head.next
        while p != self.head:
            parts.append(str(p.data))
            p = p.next
        parts.append("(H)")
        return " → ".join(parts)


class CircularWithRear:
    """只用尾指针表示的循环单链表 (不带头节点)

    优势: O(1) 访问表头和表尾
    表头: rear.next
    表尾: rear
    """
    def __init__(self):
        self.rear = None

    def is_empty(self):
        return self.rear is None

    def insert_head(self, value):
        """头插 O(1)"""
        node = CSNode(value)
        if self.is_empty():
            node.next = node
            self.rear = node
        else:
            node.next = self.rear.next
            self.rear.next = node

    def insert_tail(self, value):
        """尾插 O(1)"""
        self.insert_head(value)
        self.rear = self.rear.next  # 新节点成为新的尾

    def delete_head(self):
        """删除表头 O(1)"""
        if self.is_empty():
            return None
        head_node = self.rear.next
        if head_node == self.rear:
            self.rear = None
        else:
            self.rear.next = head_node.next
        return head_node.data

    def display(self):
        if self.is_empty():
            return []
        result = []
        p = self.rear.next  # 从表头开始
        while True:
            result.append(p.data)
            if p == self.rear:
                break
            p = p.next
        return result

    @staticmethod
    def merge(list_a, list_b):
        """合并两个循环链表 O(1)

        步骤:
        ① 保存 A 的表头: p = A.rear.next
        ② A 的尾连 B 的头: A.rear.next = B.rear.next
        ③ B 的尾连 A 的头: B.rear.next = p
        ④ 合并后尾指针为 B.rear
        """
        if list_a.is_empty():
            return list_b
        if list_b.is_empty():
            return list_a
        p = list_a.rear.next       # ① A的表头
        list_a.rear.next = list_b.rear.next  # ② A尾→B头
        list_b.rear.next = p       # ③ B尾→A头
        # 合并后尾指针为 B.rear
        merged = CircularWithRear()
        merged.rear = list_b.rear
        return merged


# ==========================================
# 循环双链表
# ==========================================

class CDNode:
    """循环双链表节点"""
    def __init__(self, data=None):
        self.data = data
        self.prior = None
        self.next = None


class CircularDoublyLinkedList:
    """带头节点的循环双链表"""
    def __init__(self):
        self.head = CDNode()
        self.head.next = self.head    # 空表
        self.head.prior = self.head   # 空表

    def is_empty(self):
        """判空: head.next == head"""
        return self.head.next == self.head

    def insert_tail(self, value):
        """尾插：在头节点的 prior (即最后一个节点) 后插入"""
        node = CDNode(value)
        tail = self.head.prior     # 当前尾节点
        node.next = self.head      # 新节点指向头
        node.prior = tail          # 新节点前驱为原尾
        tail.next = node           # 原尾指向新节点
        self.head.prior = node     # 头的前驱指向新节点 (新尾)

    def delete_node(self, p):
        """删除节点 p"""
        if p == self.head:
            return False
        p.prior.next = p.next
        p.next.prior = p.prior
        return True

    def display(self):
        result = []
        p = self.head.next
        while p != self.head:
            result.append(p.data)
            p = p.next
        return result

    def display_backward(self):
        result = []
        p = self.head.prior
        while p != self.head:
            result.append(p.data)
            p = p.prior
        return result


def circular_singly_demo():
    """循环单链表演示"""
    print("=" * 60)
    print("循环单链表")
    print("=" * 60)

    csll = CircularSinglyLinkedList()
    for v in [10, 20, 30, 40]:
        csll.insert_tail(v)
    print(f"\n  循环单链表: {csll.display_circular()}")
    print(f"  注意: 最后一个节点指回头节点 H")
    print(f"  判空条件: head.next == head? {csll.is_empty()}")

    # 尾指针版本
    print(f"\n  --- 尾指针表示的循环链表 ---")
    cr = CircularWithRear()
    for v in [1, 2, 3, 4, 5]:
        cr.insert_tail(v)
    print(f"  链表: {cr.display()}")
    print(f"  尾节点 rear = {cr.rear.data}")
    print(f"  头节点 rear.next = {cr.rear.next.data}")
    print(f"  优势: O(1) 访问首尾!")

    # 合并
    print(f"\n  --- 两个循环链表合并 O(1) ---")
    a = CircularWithRear()
    for v in [1, 2, 3]:
        a.insert_tail(v)
    b = CircularWithRear()
    for v in [4, 5, 6]:
        b.insert_tail(v)
    print(f"  A = {a.display()}")
    print(f"  B = {b.display()}")
    merged = CircularWithRear.merge(a, b)
    print(f"  合并后: {merged.display()}")

    print()


def circular_doubly_demo():
    """循环双链表演示"""
    print("=" * 60)
    print("循环双链表")
    print("=" * 60)

    cdll = CircularDoublyLinkedList()
    for v in [10, 20, 30, 40]:
        cdll.insert_tail(v)

    print(f"\n  正向: {cdll.display()}")
    print(f"  反向: {cdll.display_backward()}")
    print(f"  判空: head.next == head? {cdll.is_empty()}")
    print(f"  head.next = {cdll.head.next.data}, head.prior = {cdll.head.prior.data}")
    print()


if __name__ == "__main__":
    circular_singly_demo()
    circular_doubly_demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 判空条件:
     循环单链表: head.next == head
     循环双链表: head.next == head 且 head.prior == head

  2. 尾指针的优势:
     表头 = rear.next  → O(1)
     表尾 = rear       → O(1)
     普通单链表找尾需 O(n)

  3. 合并两个循环链表 O(1):
     ① 保存 A 表头
     ② A尾 → B头   (A.rear.next = B.rear.next)
     ③ B尾 → A头   (B.rear.next = p)

  4. 循环链表适用场景:
     约瑟夫问题、轮转调度、循环缓冲区
    """)
