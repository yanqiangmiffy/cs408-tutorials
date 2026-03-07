"""
顺序表 (Sequential List / Array List)

存储方式: 用一组连续的存储单元存储线性表的数据元素
地址计算: LOC(ai) = LOC(a1) + (i-1) × sizeof(ElemType)

时间复杂度:
  - 按下标访问: O(1)  (随机存取)
  - 插入: 平均 O(n)  (需移动 n/2 个元素)
  - 删除: 平均 O(n)  (需移动 (n-1)/2 个元素)
  - 按值查找: O(n)

考研要点:
  - 顺序表支持随机存取
  - 插入/删除的平均移动元素个数
  - 静态分配 vs 动态分配
"""


class SequentialList:
    """顺序表的实现 (动态分配版本)"""

    def __init__(self, capacity=10):
        self.data = [None] * capacity  # 存储空间
        self.length = 0                # 当前长度
        self.capacity = capacity       # 最大容量

    def _expand(self):
        """容量不足时扩容 (倍增策略)"""
        new_capacity = self.capacity * 2
        new_data = [None] * new_capacity
        for i in range(self.length):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity
        print(f"  [扩容] {self.capacity // 2} → {self.capacity}")

    # ===== 插入操作 =====
    def insert(self, index, value):
        """在第 index 个位置插入元素 value (1-indexed, 即位序)

        合法范围: 1 <= index <= length + 1
        """
        if index < 1 or index > self.length + 1:
            print(f"  插入失败: 位序 {index} 不合法 (范围 1~{self.length + 1})")
            return False
        if self.length >= self.capacity:
            self._expand()
        # 从后往前移动元素
        for j in range(self.length, index - 1, -1):
            self.data[j] = self.data[j - 1]
        self.data[index - 1] = value  # 位序转下标
        self.length += 1
        return True

    # ===== 删除操作 =====
    def delete(self, index):
        """删除第 index 个位置的元素 (1-indexed)

        返回被删除的元素值
        """
        if index < 1 or index > self.length:
            print(f"  删除失败: 位序 {index} 不合法 (范围 1~{self.length})")
            return None
        deleted = self.data[index - 1]
        # 从前往后移动元素
        for j in range(index - 1, self.length - 1):
            self.data[j] = self.data[j + 1]
        self.data[self.length - 1] = None
        self.length -= 1
        return deleted

    # ===== 查找操作 =====
    def get_elem(self, index):
        """按位查找 (1-indexed) → O(1)"""
        if index < 1 or index > self.length:
            return None
        return self.data[index - 1]

    def locate_elem(self, value):
        """按值查找，返回位序 (1-indexed) → O(n)"""
        for i in range(self.length):
            if self.data[i] == value:
                return i + 1
        return 0  # 未找到

    def display(self):
        """显示顺序表"""
        return list(self.data[:self.length])

    def __len__(self):
        return self.length

    def __repr__(self):
        return f"SequentialList({self.display()})"


def insert_delete_demo():
    """演示插入和删除操作"""
    print("=" * 60)
    print("顺序表的插入和删除操作")
    print("=" * 60)

    sl = SequentialList(5)
    # 初始化
    for v in [10, 20, 30, 40]:
        sl.insert(sl.length + 1, v)
    print(f"\n  初始顺序表: {sl.display()}, 长度={sl.length}")

    # 插入
    print(f"\n  --- 插入操作 ---")
    print(f"  在位序3插入25:")
    sl.insert(3, 25)
    print(f"  结果: {sl.display()}")
    print(f"  说明: 25 插入到第3个位置，30、40 后移")

    print(f"\n  在末尾插入50:")
    sl.insert(sl.length + 1, 50)
    print(f"  结果: {sl.display()}")

    # 删除
    print(f"\n  --- 删除操作 ---")
    deleted = sl.delete(2)
    print(f"  删除位序2的元素: {deleted}")
    print(f"  结果: {sl.display()}")
    print(f"  说明: 20 被删除，25、30、40、50 前移")

    print()


def search_demo():
    """演示查找操作"""
    print("=" * 60)
    print("顺序表的查找操作")
    print("=" * 60)

    sl = SequentialList()
    for v in [10, 20, 30, 40, 50]:
        sl.insert(sl.length + 1, v)
    print(f"\n  顺序表: {sl.display()}")

    # 按位查找
    print(f"\n  --- 按位查找 GetElem(i) → O(1) ---")
    for i in [1, 3, 5]:
        print(f"  GetElem({i}) = {sl.get_elem(i)}")

    # 按值查找
    print(f"\n  --- 按值查找 LocateElem(e) → O(n) ---")
    for v in [30, 60]:
        pos = sl.locate_elem(v)
        if pos:
            print(f"  LocateElem({v}) = 位序{pos}")
        else:
            print(f"  LocateElem({v}) = 未找到")

    print()


def verbose_insert(sl, index, value):
    """带详细输出的插入操作"""
    print(f"\n  插入 {value} 到位序 {index}:")
    print(f"  当前: {sl.display()}, 长度={sl.length}")

    if index < 1 or index > sl.length + 1:
        print(f"  位序不合法!")
        return

    move_count = sl.length - index + 1
    print(f"  需要移动 {move_count} 个元素 (从位序{index}到{sl.length})")

    sl.insert(index, value)
    print(f"  结果: {sl.display()}")


def move_count_analysis():
    """分析平均移动次数"""
    print("=" * 60)
    print("插入/删除的平均移动次数分析")
    print("=" * 60)
    print("""
  插入操作 (在第 i 个位置插入):
    移动次数 = n - i + 1
    i 取值范围: 1 ~ n+1
    平均移动次数 = Σ(n-i+1) / (n+1) = n/2

  删除操作 (删除第 i 个位置):
    移动次数 = n - i
    i 取值范围: 1 ~ n
    平均移动次数 = Σ(n-i) / n = (n-1)/2

  ┌──────────┬──────────────┬───────────────┐
  │  操作    │ 最好情况     │ 最坏情况      │
  │──────────│──────────────│───────────────│
  │  插入    │ O(1) 表尾    │ O(n) 表头     │
  │  删除    │ O(1) 表尾    │ O(n) 表头     │
  │  查找    │ O(1) 按下标  │ O(n) 按值     │
  └──────────┴──────────────┴───────────────┘
    """)


if __name__ == "__main__":
    insert_delete_demo()
    search_demo()
    move_count_analysis()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 顺序表特点:
     - 随机存取: O(1) 按下标访问
     - 存储密度高: 不需要额外指针空间
     - 插入/删除需移动大量元素

  2. 静态 vs 动态分配:
     静态: 数组大小固定，满了不能扩
     动态: 可以 realloc 扩容（但需拷贝）

  3. 地址公式:
     LOC(ai) = LOC(a1) + (i-1) × sizeof(ElemType)
    """)
