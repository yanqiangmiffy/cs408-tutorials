"""
数据结构的基本概念

核心知识点:
  1. 数据结构三要素: 逻辑结构、存储结构、数据运算
  2. 逻辑结构: 集合、线性、树形、图状
  3. 存储结构: 顺序存储、链式存储、索引存储、散列存储
  4. 数据类型 vs 抽象数据类型 (ADT)

考研要点:
  - 逻辑结构与存储结构的区别
  - 四种逻辑结构的特征
  - 四种存储结构的优缺点
"""


# ==========================================
# 1. 逻辑结构示例
# ==========================================

def logical_structures_demo():
    """演示四种逻辑结构"""
    print("=" * 60)
    print("逻辑结构示例")
    print("=" * 60)

    # 1. 集合结构: 元素之间没有关系
    set_structure = {3, 1, 4, 1, 5, 9, 2, 6}
    print(f"\n1. 集合结构: {set_structure}")
    print(f"   特点: 元素之间除「同属一个集合」外无其他关系")

    # 2. 线性结构: 一对一
    linear_structure = [10, 20, 30, 40, 50]
    print(f"\n2. 线性结构: {linear_structure}")
    print(f"   特点: 元素之间一对一关系，有前驱和后继")
    print(f"   例子: 数组、链表、栈、队列")

    # 3. 树形结构: 一对多
    tree_structure = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [], 'E': [], 'F': []
    }
    print(f"\n3. 树形结构:")
    print(f"         A")
    print(f"        / \\")
    print(f"       B   C")
    print(f"      / \\   \\")
    print(f"     D   E   F")
    print(f"   特点: 元素之间一对多关系")

    # 4. 图状结构: 多对多
    graph_structure = {
        'A': ['B', 'C'],
        'B': ['A', 'C', 'D'],
        'C': ['A', 'B', 'D'],
        'D': ['B', 'C']
    }
    print(f"\n4. 图状结构:")
    print(f"     A --- B")
    print(f"     |  ×  |")
    print(f"     C --- D")
    print(f"   特点: 元素之间多对多关系")
    print()


# ==========================================
# 2. 存储结构示例
# ==========================================

class SequentialStorage:
    """顺序存储: 用连续内存空间存储"""
    def __init__(self, capacity=10):
        self.data = [None] * capacity
        self.length = 0
        self.capacity = capacity

    def insert(self, index, value):
        if self.length >= self.capacity:
            print(f"  存储已满，无法插入")
            return False
        # 后移元素
        for i in range(self.length, index, -1):
            self.data[i] = self.data[i - 1]
        self.data[index] = value
        self.length += 1
        return True

    def display(self):
        return self.data[:self.length]


class LinkedNode:
    """链式存储: 用指针链接各节点"""
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedStorage:
    """链式存储示例"""
    def __init__(self):
        self.head = None

    def insert_head(self, value):
        node = LinkedNode(value)
        node.next = self.head
        self.head = node

    def display(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result


def storage_structures_demo():
    """演示存储结构"""
    print("=" * 60)
    print("存储结构示例")
    print("=" * 60)

    # 1. 顺序存储
    print("\n1. 顺序存储 (数组)")
    seq = SequentialStorage(5)
    for i, v in enumerate([10, 20, 30]):
        seq.insert(i, v)
    print(f"   初始: {seq.display()}")
    seq.insert(1, 15)  # 在位置1插入15
    print(f"   插入15到位置1: {seq.display()}")
    print(f"   优点: 随机访问 O(1)")
    print(f"   缺点: 插入/删除需移动元素 O(n)")

    # 2. 链式存储
    print("\n2. 链式存储 (链表)")
    linked = LinkedStorage()
    for v in [30, 20, 10]:
        linked.insert_head(v)
    print(f"   链表: {linked.display()}")
    linked.insert_head(5)
    print(f"   头插5: {linked.display()}")
    print(f"   优点: 插入/删除只需改指针 O(1)")
    print(f"   缺点: 无法随机访问，需从头遍历 O(n)")

    # 3. 索引存储
    print("\n3. 索引存储")
    data = ["张三", "李四", "王五", "赵六"]
    index_table = {1001: 0, 1002: 1, 1003: 2, 1004: 3}
    print(f"   数据: {data}")
    print(f"   索引表: {index_table}")
    print(f"   通过索引 1003 查找: {data[index_table[1003]]}")
    print(f"   优点: 检索速度快")
    print(f"   缺点: 需要额外索引表空间")

    # 4. 散列存储
    print("\n4. 散列存储")
    hash_table = {}
    keys = ["apple", "banana", "cherry"]
    for key in keys:
        h = hash(key) % 10
        hash_table[h] = key
    print(f"   散列存储: 通过散列函数直接定位")
    print(f"   优点: O(1) 查找")
    print(f"   缺点: 可能产生冲突")
    print()


# ==========================================
# 3. 抽象数据类型 (ADT)
# ==========================================

def adt_demo():
    """演示抽象数据类型的概念"""
    print("=" * 60)
    print("抽象数据类型 (ADT) 示例")
    print("=" * 60)

    print("""
  ADT 复数 {
      数据对象: D = {real, imag | real, imag ∈ R}
      数据关系: R = {<real, imag>}
      操作集合:
          Create(real, imag)  → 创建复数
          Add(c1, c2)         → 复数加法
          Multiply(c1, c2)    → 复数乘法
          GetReal(c)          → 取实部
          GetImag(c)          → 取虚部
  }
    """)

    # 实现 ADT 复数
    class Complex:
        """复数 ADT 的 Python 实现"""
        def __init__(self, real=0, imag=0):
            self.real = real
            self.imag = imag

        def add(self, other):
            return Complex(self.real + other.real, self.imag + other.imag)

        def multiply(self, other):
            r = self.real * other.real - self.imag * other.imag
            i = self.real * other.imag + self.imag * other.real
            return Complex(r, i)

        def __repr__(self):
            sign = '+' if self.imag >= 0 else '-'
            return f"{self.real} {sign} {abs(self.imag)}i"

    c1 = Complex(3, 4)
    c2 = Complex(1, 2)
    print(f"  c1 = {c1}")
    print(f"  c2 = {c2}")
    print(f"  c1 + c2 = {c1.add(c2)}")
    print(f"  c1 × c2 = {c1.multiply(c2)}")
    print()


if __name__ == "__main__":
    logical_structures_demo()
    storage_structures_demo()
    adt_demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 数据结构三要素:
     逻辑结构 + 存储结构 + 数据运算

  2. 逻辑结构分类:
     集合 | 线性 | 树形 | 图状

  3. 存储结构分类:
     顺序 | 链式 | 索引 | 散列

  4. 逻辑结构 vs 存储结构:
     逻辑结构: 数据元素之间的逻辑关系 (与存储无关)
     存储结构: 逻辑结构在计算机中的表示 (物理实现)

  5. ADT = 数据对象 + 数据关系 + 操作集合
    """)
