"""
散列表 (Hash Table)

核心思想: 通过散列函数将关键字映射到存储位置
理想情况: O(1) 查找

散列函数:
  1. 除留余数法: H(key) = key % p  (p 取不大于表长的最大素数)
  2. 直接定址法: H(key) = a*key + b
  3. 数字分析法: 取关键字中分布均匀的若干位

冲突处理:
  1. 开放定址法:
     - 线性探测: H_i = (H(key) + i) % m
     - 平方探测: H_i = (H(key) ± i²) % m
     - 双散列: H_i = (H(key) + i*H2(key)) % m
  2. 拉链法: 每个位置一个链表

考研要点:
  - 手算散列表的构造过程
  - 计算 ASL (成功和失败)
  - 装填因子 α = n/m 对性能的影响
"""


# ==========================================
# 1. 拉链法 (Separate Chaining)
# ==========================================

class HashTableChaining:
    """拉链法散列表"""

    def __init__(self, size=13):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0

    def _hash(self, key):
        """除留余数法"""
        return key % self.size

    def insert(self, key):
        idx = self._hash(key)
        if key not in self.table[idx]:
            self.table[idx].append(key)
            self.count += 1

    def search(self, key):
        idx = self._hash(key)
        comparisons = 0
        for k in self.table[idx]:
            comparisons += 1
            if k == key:
                return True, comparisons
        return False, comparisons

    def delete(self, key):
        idx = self._hash(key)
        if key in self.table[idx]:
            self.table[idx].remove(key)
            self.count -= 1
            return True
        return False

    def display(self):
        for i in range(self.size):
            chain = " → ".join(str(k) for k in self.table[i])
            print(f"  {i:>3d}: {chain if chain else '(空)'}")

    def asl_success(self):
        """计算成功 ASL"""
        total = 0
        for chain in self.table:
            for i in range(len(chain)):
                total += i + 1
        return total / self.count if self.count else 0

    def asl_fail(self):
        """计算失败 ASL"""
        total = sum(len(chain) for chain in self.table)
        return total / self.size


# ==========================================
# 2. 开放定址法 - 线性探测
# ==========================================

class HashTableLinearProbing:
    """线性探测法散列表"""

    EMPTY = None
    DELETED = "DELETED"

    def __init__(self, size=13):
        self.size = size
        self.table = [self.EMPTY] * size
        self.count = 0

    def _hash(self, key):
        return key % self.size

    def insert(self, key):
        if self.count >= self.size:
            print("  散列表已满!")
            return False
        idx = self._hash(key)
        i = 0
        while i < self.size:
            pos = (idx + i) % self.size
            if self.table[pos] is self.EMPTY or self.table[pos] == self.DELETED:
                self.table[pos] = key
                self.count += 1
                return True
            if self.table[pos] == key:
                return False  # 已存在
            i += 1
        return False

    def search(self, key):
        idx = self._hash(key)
        comparisons = 0
        i = 0
        while i < self.size:
            pos = (idx + i) % self.size
            comparisons += 1
            if self.table[pos] is self.EMPTY:
                return False, comparisons
            if self.table[pos] == key:
                return True, comparisons
            i += 1
        return False, comparisons

    def delete(self, key):
        idx = self._hash(key)
        i = 0
        while i < self.size:
            pos = (idx + i) % self.size
            if self.table[pos] is self.EMPTY:
                return False
            if self.table[pos] == key:
                self.table[pos] = self.DELETED  # 懒删除
                self.count -= 1
                return True
            i += 1
        return False

    def display(self):
        for i in range(self.size):
            val = self.table[i]
            if val is self.EMPTY:
                print(f"  {i:>3d}: (空)")
            elif val == self.DELETED:
                print(f"  {i:>3d}: (已删)")
            else:
                print(f"  {i:>3d}: {val}")

    def asl_success(self):
        """成功 ASL"""
        total = 0
        for key_val in self.table:
            if key_val is not self.EMPTY and key_val != self.DELETED:
                _, comps = self.search(key_val)
                total += comps
        return total / self.count if self.count else 0

    def asl_fail(self):
        """失败 ASL: 对每个散列地址, 计算到第一个空位的探测次数"""
        total = 0
        for i in range(self.size):
            j = 0
            while j < self.size:
                pos = (i + j) % self.size
                j += 1
                if self.table[pos] is self.EMPTY:
                    break
            total += j
        return total / self.size


# ==========================================
# 3. 开放定址法 - 平方探测
# ==========================================

class HashTableQuadraticProbing:
    """平方探测法: H_i = (H(key) + i²) % m"""

    EMPTY = None

    def __init__(self, size=13):
        self.size = size
        self.table = [self.EMPTY] * size
        self.count = 0

    def _hash(self, key):
        return key % self.size

    def insert(self, key):
        idx = self._hash(key)
        for i in range(self.size):
            # 按 0, 1, -1, 4, -4, 9, -9, ... 探测
            for sign in [1, -1]:
                if i == 0 and sign == -1:
                    continue
                pos = (idx + sign * i * i) % self.size
                if self.table[pos] is self.EMPTY:
                    self.table[pos] = key
                    self.count += 1
                    return True
                if self.table[pos] == key:
                    return False
        return False

    def display(self):
        for i in range(self.size):
            val = self.table[i]
            print(f"  {i:>3d}: {val if val is not self.EMPTY else '(空)'}")


def chaining_demo():
    """拉链法演示"""
    print("=" * 60)
    print("拉链法散列表")
    print("=" * 60)

    ht = HashTableChaining(13)
    keys = [19, 14, 23, 1, 68, 20, 84, 27, 55, 11, 10, 79]

    print(f"\n  散列函数: H(key) = key % {ht.size}")
    print(f"  插入序列: {keys}")

    for k in keys:
        h = ht._hash(k)
        ht.insert(k)
        print(f"  H({k:>2d}) = {h:>2d}")

    print(f"\n  散列表:")
    ht.display()

    print(f"\n  ASL(成功) = {ht.asl_success():.2f}")
    print(f"  ASL(失败) = {ht.asl_fail():.2f}")
    print(f"  装填因子 α = {ht.count}/{ht.size} = {ht.count / ht.size:.2f}")
    print()


def linear_probing_demo():
    """线性探测法演示"""
    print("=" * 60)
    print("线性探测法散列表")
    print("=" * 60)

    ht = HashTableLinearProbing(13)
    keys = [19, 14, 23, 1, 68, 20, 84, 27, 55, 11, 10, 79]

    print(f"\n  散列函数: H(key) = key % {ht.size}")
    print(f"  插入序列: {keys}")
    print(f"\n  插入过程:")

    for k in keys:
        h = ht._hash(k)
        ht.insert(k)
        # 找实际位置
        for i in range(ht.size):
            if ht.table[i] == k:
                if i == h:
                    print(f"  H({k:>2d}) = {h:>2d} → 位置 {i} (无冲突)")
                else:
                    print(f"  H({k:>2d}) = {h:>2d} → 位置 {i} (冲突, 线性探测)")
                break

    print(f"\n  散列表:")
    ht.display()

    print(f"\n  --- 查找 ---")
    for k in [23, 55, 15]:
        found, comps = ht.search(k)
        mark = "✓" if found else "✗"
        print(f"  {mark} 查找 {k}: {comps} 次比较")

    print(f"\n  ASL(成功) = {ht.asl_success():.2f}")
    print(f"  ASL(失败) = {ht.asl_fail():.2f}")
    print(f"  装填因子 α = {ht.count}/{ht.size} = {ht.count / ht.size:.2f}")
    print()


if __name__ == "__main__":
    chaining_demo()
    linear_probing_demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 散列函数:
     除留余数法: H(key) = key % p  (p 取素数)
     直接定址法: H(key) = a*key + b (不会冲突)

  2. 冲突处理:
     拉链法: 同义词放一个链表
     线性探测: H(key)+1, +2, +3, ... (会聚集)
     平方探测: H(key)+1², -1², +2², ... (减少聚集)

  3. ASL:
     α = n/m (装填因子)
     拉链法: ASL成功 ≈ 1 + α/2
     线性探测: ASL成功 ≈ (1 + 1/(1-α))/2

  4. 注意:
     α 越大, 冲突越多, ASL 越大
     线性探测会产生「聚集」(堆积) 现象
     拉链法不会产生聚集, 性能更稳定
    """)
