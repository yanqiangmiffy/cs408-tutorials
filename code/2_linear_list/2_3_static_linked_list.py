"""
静态链表 (Static Linked List)

核心思想: 用数组模拟链表,  用「游标」(数组下标) 代替指针
适用场景: 不支持指针的语言 (如早期 Fortran)

结构: 每个数组元素包含 data 和 next (下一个元素的下标)
     next = -1 表示链表结束
     通常 arr[0] 作为备用链表的头 (空闲空间管理)

考研要点:
  - 静态链表是用数组实现的链表
  - 插入/删除不需要移动元素,只需修改游标
  - 但不能随机访问, 需要从头遍历
  - 需要预先分配固定大小的数组
"""


class StaticLinkedList:
    """静态链表"""

    def __init__(self, capacity=10):
        self.capacity = capacity
        # 每个元素: [data, next_cursor]
        self.data = [None] * capacity
        self.cursor = [-1] * capacity

        # 初始化备用链表: 0 → 1 → 2 → ... → capacity-1
        # arr[0] 不存数据，是备用链表的头
        for i in range(capacity - 1):
            self.cursor[i] = i + 1
        self.cursor[capacity - 1] = -1  # 备用链表尾

        # arr[capacity-1] 不存数据, 存放第一个有数据节点的下标
        # 这里我们用 self.head 表示数据链表的头
        self.head = -1  # 空表
        self.free_head = 0  # 备用链表头

    def _malloc(self):
        """从备用链表中分配一个空闲节点"""
        if self.free_head == -1:
            print("  空间已满!")
            return -1
        idx = self.free_head
        self.free_head = self.cursor[idx]
        return idx

    def _free(self, idx):
        """将节点归还备用链表"""
        self.cursor[idx] = self.free_head
        self.data[idx] = None
        self.free_head = idx

    def insert(self, index, value):
        """在第 index 个位置插入 (1-indexed)"""
        new_idx = self._malloc()
        if new_idx == -1:
            return False

        self.data[new_idx] = value

        if index == 1:
            self.cursor[new_idx] = self.head
            self.head = new_idx
        else:
            # 找到第 index-1 个节点
            p = self.head
            for _ in range(index - 2):
                if p == -1:
                    self._free(new_idx)
                    return False
                p = self.cursor[p]
            self.cursor[new_idx] = self.cursor[p]
            self.cursor[p] = new_idx
        return True

    def delete(self, index):
        """删除第 index 个位置的元素 (1-indexed)"""
        if self.head == -1:
            return None

        if index == 1:
            del_idx = self.head
            self.head = self.cursor[del_idx]
        else:
            p = self.head
            for _ in range(index - 2):
                if p == -1:
                    return None
                p = self.cursor[p]
            del_idx = self.cursor[p]
            if del_idx == -1:
                return None
            self.cursor[p] = self.cursor[del_idx]

        deleted = self.data[del_idx]
        self._free(del_idx)
        return deleted

    def display(self):
        """遍历数据链表"""
        result = []
        p = self.head
        while p != -1:
            result.append(self.data[p])
            p = self.cursor[p]
        return result

    def display_array(self):
        """展示底层数组状态"""
        print(f"  {'下标':>4s} {'数据':>6s} {'游标':>6s}")
        print(f"  {'─' * 20}")
        for i in range(self.capacity):
            d = self.data[i] if self.data[i] is not None else "空"
            c = self.cursor[i]
            marker = ""
            if i == self.head:
                marker = " ← 数据头"
            if i == self.free_head:
                marker = " ← 空闲头"
            print(f"  {i:>4d} {str(d):>6s} {c:>6d}{marker}")


def basic_demo():
    """静态链表基本操作"""
    print("=" * 60)
    print("静态链表演示")
    print("=" * 60)

    sll = StaticLinkedList(8)

    print(f"\n  --- 初始状态 (空表) ---")
    sll.display_array()

    # 插入元素
    print(f"\n  --- 依次插入 A, B, C, D ---")
    for i, v in enumerate(['A', 'B', 'C', 'D'], 1):
        sll.insert(i, v)
    print(f"  数据链表: {sll.display()}")
    sll.display_array()

    # 中间插入
    print(f"\n  --- 在位序2插入 X ---")
    sll.insert(2, 'X')
    print(f"  数据链表: {sll.display()}")
    sll.display_array()

    # 删除
    print(f"\n  --- 删除位序3 ---")
    deleted = sll.delete(3)
    print(f"  删除的值: {deleted}")
    print(f"  数据链表: {sll.display()}")
    sll.display_array()

    print()


if __name__ == "__main__":
    basic_demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 静态链表 = 用数组模拟链表
     数组元素: (data, cursor/游标)
     cursor 存的是下一个元素的数组下标

  2. 两条链表:
     数据链表: 存放实际数据
     备用链表: 管理空闲空间 (类似 malloc/free)

  3. 优缺点:
     优点: 插入/删除不需移动元素
     缺点: 不能随机存取, 容量固定

  4. 适用场景:
     不支持指针的低级语言
    """)
