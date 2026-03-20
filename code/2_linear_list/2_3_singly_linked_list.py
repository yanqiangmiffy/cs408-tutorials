"""
单链表 (Singly Linked List)

存储方式: 每个节点包含数据域和指针域 (next)
头节点: 不存数据，仅作为链表入口，简化边界处理

时间复杂度:
  - 头插/头删: O(1)
  - 按位查找: O(n)
  - 按值查找: O(n)
  - 在给定节点后插入: O(1)
  - 在给定节点后删除: O(1)

考研要点:
  - 头插法建表: 逆序
  - 尾插法建表: 顺序
  - 带头节点 vs 不带头节点
  - 插入/删除操作的指针修改顺序
"""


class Node:
    """单链表节点"""
    def __init__(self, data=None):
        self.data = data
        self.next = None

    def __repr__(self):
        return f"Node({self.data})"


class SinglyLinkedList:
    """带头节点的单链表"""

    def __init__(self):
        self.head = Node()  # 头节点 (不存数据)
        self.length = 0

    # ===== 建表操作 =====
    @staticmethod
    def from_head_insert(values):
        """头插法建表 → 结果逆序"""
        sll = SinglyLinkedList()
        for v in values:
            node = Node(v)
            node.next = sll.head.next
            sll.head.next = node
            sll.length += 1
        return sll

    @staticmethod
    def from_tail_insert(values):
        """尾插法建表 → 结果顺序"""
        sll = SinglyLinkedList()
        tail = sll.head  # 尾指针始终指向最后一个节点
        for v in values:
            node = Node(v)
            tail.next = node
            tail = node
            sll.length += 1
        return sll

    # ===== 按位查找 =====
    def get_elem(self, index):
        """按位查找 (1-indexed)，返回第 index 个节点

        思路: 从头节点出发，向后遍历 index 次
        """
        if index < 0:
            return None
        p = self.head  # p 指向头节点 (第0个节点)
        j = 0
        while p and j < index:
            p = p.next
            j += 1
        return p

    # ===== 按值查找 =====
    def locate_elem(self, value):
        """按值查找，返回第一个值为 value 的节点"""
        p = self.head.next
        while p:
            if p.data == value:
                return p
            p = p.next
        return None

    # ===== 插入操作 =====
    def insert(self, index, value):
        """在第 index 个位置插入元素 (1-indexed)

        关键: 找到第 index-1 个节点 (前驱)
        注意指针修改顺序: 先让新节点指向后继，再让前驱指向新节点
        """
        p = self.get_elem(index - 1)  # 找前驱
        if p is None:
            print(f"  插入失败: 位序 {index} 不合法")
            return False
        node = Node(value)
        node.next = p.next   # ① 新节点指向后继
        p.next = node        # ② 前驱指向新节点
        self.length += 1
        return True

    def insert_after(self, p, value):
        """在节点 p 之后插入 → O(1)"""
        if p is None:
            return False
        node = Node(value)
        node.next = p.next
        p.next = node
        self.length += 1
        return True

    def insert_before(self, p, value):
        """在节点 p 之前插入 (偷天换日法) → O(1)

        技巧: 实际在 p 后插入新节点，然后交换 p 和新节点的数据
        """
        if p is None:
            return False
        node = Node(p.data)   # 新节点数据 = p 的数据
        node.next = p.next
        p.next = node
        p.data = value        # p 的数据改为要插入的值
        self.length += 1
        return True

    # ===== 删除操作 =====
    def delete(self, index):
        """删除第 index 个位置的节点 (1-indexed)

        关键: 找到第 index-1 个节点 (前驱)
        """
        p = self.get_elem(index - 1)  # 找前驱
        if p is None or p.next is None:
            print(f"  删除失败: 位序 {index} 不合法")
            return None
        q = p.next       # q 是要删除的节点
        p.next = q.next  # 前驱直接指向后继
        deleted = q.data
        self.length -= 1
        return deleted

    def delete_node(self, p):
        """删除给定节点 p (偷天换日法) → O(1)

        技巧: 将后继节点的数据拷贝到 p，然后删除后继
        注意: 不能删除最后一个节点 (无后继)
        """
        if p is None or p.next is None:
            print("  无法用此方法删除最后一个节点!")
            return False
        q = p.next
        p.data = q.data    # 拷贝后继数据
        p.next = q.next    # 跳过后继
        self.length -= 1
        return True

    # ===== 辅助方法 =====
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
        return " → ".join(parts)

    def __len__(self):
        return self.length


def build_demo():
    """演示头插法和尾插法建表"""
    print("=" * 60)
    print("单链表的建立")
    print("=" * 60)

    values = [1, 2, 3, 4, 5]
    print(f"\n  输入序列: {values}")

    # 头插法
    sll1 = SinglyLinkedList.from_head_insert(values)
    print(f"\n  头插法建表 (逆序):")
    print(f"  {sll1.display_with_arrow()}")
    print(f"  说明: 每次在头部插入，先进的被推到后面")

    # 尾插法
    sll2 = SinglyLinkedList.from_tail_insert(values)
    print(f"\n  尾插法建表 (顺序):")
    print(f"  {sll2.display_with_arrow()}")
    print(f"  说明: 每次在尾部追加，保持原始顺序")
    print()


def insert_delete_demo():
    """演示插入和删除"""
    print("=" * 60)
    print("单链表的插入和删除")
    print("=" * 60)

    sll = SinglyLinkedList.from_tail_insert([10, 20, 30, 40, 50])
    print(f"\n  初始: {sll.display_with_arrow()}")

    # 按位插入
    print(f"\n  --- 按位插入 ---")
    sll.insert(3, 25)
    print(f"  在位序3插入25: {sll.display_with_arrow()}")
    print(f"  步骤: 找到位序2的节点(20)，在其后插入25")

    # 后插操作
    print(f"\n  --- 后插操作 O(1) ---")
    node_30 = sll.locate_elem(30)
    sll.insert_after(node_30, 35)
    print(f"  在30后插入35: {sll.display_with_arrow()}")

    # 前插操作(偷天换日法)
    print(f"\n  --- 前插操作 (偷天换日法) O(1) ---")
    node_40 = sll.locate_elem(40)
    sll.insert_before(node_40, 38)
    print(f"  在40前插入38: {sll.display_with_arrow()}")
    print(f"  技巧: 实际在40后插新节点，然后交换数据")

    # 按位删除
    print(f"\n  --- 按位删除 ---")
    deleted = sll.delete(2)
    print(f"  删除位序2: 值={deleted}")
    print(f"  结果: {sll.display_with_arrow()}")

    print()


def search_demo():
    """演示查找操作"""
    print("=" * 60)
    print("单链表的查找")
    print("=" * 60)

    sll = SinglyLinkedList.from_tail_insert([10, 20, 30, 40, 50])
    print(f"\n  链表: {sll.display_with_arrow()}")

    # 按位查找
    print(f"\n  --- 按位查找 O(n) ---")
    for i in [1, 3, 5]:
        node = sll.get_elem(i)
        print(f"  GetElem({i}) = {node.data if node else None}")

    # 按值查找
    print(f"\n  --- 按值查找 O(n) ---")
    for v in [30, 60]:
        node = sll.locate_elem(v)
        print(f"  LocateElem({v}) = {node if node else '未找到'}")

    print()


if __name__ == "__main__":
    build_demo()
    insert_delete_demo()
    search_demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 头插法 → 逆序; 尾插法 → 顺序

  2. 插入操作指针修改顺序 (在 p 之后插入 s):
     s.next = p.next   ← 先连后面
     p.next = s         ← 再连前面
     (顺序不能反! 否则丢失后继)

  3. 删除操作 (删除 p 的后继 q):
     q = p.next
     p.next = q.next

  4. 偷天换日法 (前插 / 删除自身):
     核心思想: 拷贝数据 + 操作后继节点
     局限: 不能删除最后一个节点

  5. 时间复杂度: 查找 O(n), 给定前驱后插入/删除 O(1)
    """)
