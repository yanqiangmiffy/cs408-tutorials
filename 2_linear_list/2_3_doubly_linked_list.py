"""
双链表 (Doubly Linked List)

存储方式: 每个节点包含 prior(前驱指针)、data(数据域)、next(后继指针)

与单链表的区别:
  - 可以向前遍历 (单链表只能向后)
  - 插入/删除操作需要修改两个方向的指针
  - 空间开销更大 (多一个 prior 指针)

时间复杂度:
  - 在给定节点前/后插入: O(1) (无需找前驱)
  - 删除给定节点: O(1) (可直接访问前驱)
  - 按位查找: O(n)

考研要点:
  - 插入操作的四步指针修改及顺序
  - 与单链表操作的区别和优势
"""


class DNode:
    """双链表节点"""
    def __init__(self, data=None):
        self.data = data
        self.prior = None  # 前驱指针
        self.next = None   # 后继指针

    def __repr__(self):
        return f"DNode({self.data})"


class DoublyLinkedList:
    """带头节点的双链表"""

    def __init__(self):
        self.head = DNode()  # 头节点
        self.length = 0

    @staticmethod
    def from_values(values):
        """尾插法建表"""
        dll = DoublyLinkedList()
        tail = dll.head
        for v in values:
            node = DNode(v)
            node.prior = tail
            tail.next = node
            tail = node
            dll.length += 1
        return dll

    def insert_after(self, p, value):
        """在节点 p 之后插入值为 value 的新节点

        四步操作 (顺序很重要!):
        ① s.next = p.next      新节点指向p的后继
        ② if p.next: p.next.prior = s  后继的前驱改为新节点
        ③ s.prior = p          新节点的前驱指向p
        ④ p.next = s           p的后继指向新节点
        """
        s = DNode(value)
        s.next = p.next            # ①
        if p.next:
            p.next.prior = s       # ②
        s.prior = p                # ③
        p.next = s                 # ④
        self.length += 1
        return True

    def insert(self, index, value):
        """在第 index 个位置插入 (1-indexed)"""
        p = self._get_node(index - 1)
        if p is None:
            return False
        return self.insert_after(p, value)

    def delete_node(self, p):
        """删除节点 p

        两步操作:
        ① p.prior.next = p.next     前驱的后继 = p的后继
        ② if p.next: p.next.prior = p.prior  后继的前驱 = p的前驱
        """
        if p is None or p == self.head:
            return False
        p.prior.next = p.next      # ①
        if p.next:
            p.next.prior = p.prior # ②
        self.length -= 1
        return True

    def delete(self, index):
        """删除第 index 个位置的节点 (1-indexed)"""
        p = self._get_node(index)
        if p is None:
            return None
        data = p.data
        self.delete_node(p)
        return data

    def _get_node(self, index):
        """获取第 index 个节点 (0=头节点)"""
        if index < 0:
            return None
        p = self.head
        j = 0
        while p and j < index:
            p = p.next
            j += 1
        return p

    def display(self):
        result = []
        p = self.head.next
        while p:
            result.append(p.data)
            p = p.next
        return result

    def display_with_arrow(self):
        parts = ["H"]
        p = self.head.next
        while p:
            parts.append(str(p.data))
            p = p.next
        parts.append("NULL")
        return " ⇄ ".join(parts)

    def traverse_backward(self):
        """反向遍历 (从最后一个节点到第一个)"""
        # 先找到最后一个节点
        p = self.head
        while p.next:
            p = p.next
        # 反向遍历
        result = []
        while p != self.head:
            result.append(p.data)
            p = p.prior
        return result


def basic_demo():
    """基本操作演示"""
    print("=" * 60)
    print("双链表基本操作")
    print("=" * 60)

    dll = DoublyLinkedList.from_values([10, 20, 30, 40, 50])
    print(f"\n  双链表: {dll.display_with_arrow()}")

    # 正向遍历
    print(f"\n  正向遍历: {dll.display()}")
    # 反向遍历
    print(f"  反向遍历: {dll.traverse_backward()}")

    # 插入
    print(f"\n  --- 插入操作 ---")
    dll.insert(3, 25)
    print(f"  在位序3插入25: {dll.display_with_arrow()}")

    # 删除
    print(f"\n  --- 删除操作 ---")
    deleted = dll.delete(4)
    print(f"  删除位序4: 值={deleted}")
    print(f"  结果: {dll.display_with_arrow()}")

    print()


def pointer_demo():
    """详细展示指针修改过程"""
    print("=" * 60)
    print("双链表插入操作的指针修改过程")
    print("=" * 60)

    print("""
  在 p 节点后插入 s:

  修改前:
    ... ⇄ [p] ⇄ [q] ⇄ ...

  四步操作:
    ① s.next = p.next        s → q
    ② p.next.prior = s       q.prior → s
    ③ s.prior = p            s.prior → p
    ④ p.next = s             p → s

  修改后:
    ... ⇄ [p] ⇄ [s] ⇄ [q] ⇄ ...

  ⚠️ ①②必须在④之前! 否则 p.next 被修改后找不到 q

  ─────────────────────────────────────

  删除节点 p:

  修改前:
    ... ⇄ [prev] ⇄ [p] ⇄ [next] ⇄ ...

  两步操作:
    ① p.prior.next = p.next    prev → next
    ② p.next.prior = p.prior   next.prior → prev

  修改后:
    ... ⇄ [prev] ⇄ [next] ⇄ ...
    """)


if __name__ == "__main__":
    basic_demo()
    pointer_demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 双链表 vs 单链表:
     优势: 可以O(1)找前驱，方便前插和删除
     劣势: 空间开销大 (多一个prior指针)

  2. 插入四步 (在p后插入s):
     ① s.next = p.next
     ② p.next.prior = s    (if p.next 存在)
     ③ s.prior = p
     ④ p.next = s
     注意: ①②要在④之前!

  3. 删除两步 (删除p):
     ① p.prior.next = p.next
     ② p.next.prior = p.prior  (if p.next 存在)

  4. 适用场景: 需要频繁双向遍历的场景
    """)
