"""
特殊矩阵的压缩存储

核心思想: 利用矩阵的特殊性质，只存储有意义的元素，节省空间

类型:
  1. 对称矩阵: aij = aji, 只存下三角 + 对角线
  2. 三角矩阵: 上/下三角区元素全相同
  3. 三对角矩阵 (带状矩阵): 只有主对角线和相邻两条有非零元素
  4. 稀疏矩阵: 非零元素远少于零元素

考研要点:
  - 各种矩阵的下标映射公式 (重要!)
  - 行优先 vs 列优先存储
  - 稀疏矩阵的三元组表示
"""


# ==========================================
# 1. 对称矩阵的压缩存储
# ==========================================

class SymmetricMatrix:
    """对称矩阵压缩存储 (存下三角)

    下三角元素 aij (i >= j) 在一维数组中的位置:
    k = i*(i-1)/2 + j - 1  (1-indexed 行列号)

    上三角 aij (i < j) 与 aji 对称, 用 aji 的位置
    """

    def __init__(self, n):
        self.n = n
        # 下三角 + 对角线共 n*(n+1)/2 个元素
        self.data = [0] * (n * (n + 1) // 2)

    def _index(self, i, j):
        """将矩阵下标 (i,j) 映射到一维数组下标 (1-indexed)"""
        if i < j:
            i, j = j, i  # 对称: 访问上三角等价于访问下三角
        return i * (i - 1) // 2 + j - 1

    def set(self, i, j, value):
        self.data[self._index(i, j)] = value

    def get(self, i, j):
        return self.data[self._index(i, j)]

    def display_matrix(self):
        for i in range(1, self.n + 1):
            row = [self.get(i, j) for j in range(1, self.n + 1)]
            print(f"  {row}")


# ==========================================
# 2. 三角矩阵
# ==========================================

class LowerTriangularMatrix:
    """下三角矩阵: 上三角区全为常数 c

    存储: 下三角按行存储 + 最后一个位置存常数 c
    k = i*(i-1)/2 + j - 1  (i >= j)
    k = n*(n+1)/2           (i < j, 存常数)
    """

    def __init__(self, n, c=0):
        self.n = n
        self.c = c
        self.data = [0] * (n * (n + 1) // 2 + 1)
        self.data[-1] = c  # 最后存常数

    def set(self, i, j, value):
        if i >= j:
            self.data[i * (i - 1) // 2 + j - 1] = value

    def get(self, i, j):
        if i >= j:
            return self.data[i * (i - 1) // 2 + j - 1]
        return self.c


# ==========================================
# 3. 三对角矩阵
# ==========================================

class TridiagonalMatrix:
    """三对角矩阵 (带状矩阵)

    非零元素只在: 主对角线 + 上下各一条
    即 |i - j| <= 1 时 aij 可能非零

    元素 aij 在一维数组中的位置:
    k = 2*i + j - 3  (1-indexed)

    反推: 已知 k, 则 i = (k+1)//3 + 1, j = k - 2*i + 3
    """

    def __init__(self, n):
        self.n = n
        self.data = [0] * (3 * n - 2)  # 共 3n-2 个非零元素

    def _index(self, i, j):
        """(i,j) → 一维下标 (1-indexed 行列号)"""
        return 2 * i + j - 3

    def set(self, i, j, value):
        if abs(i - j) <= 1:
            self.data[self._index(i, j)] = value

    def get(self, i, j):
        if abs(i - j) <= 1:
            return self.data[self._index(i, j)]
        return 0

    def display_matrix(self):
        for i in range(1, self.n + 1):
            row = [self.get(i, j) for j in range(1, self.n + 1)]
            print(f"  {row}")


# ==========================================
# 4. 稀疏矩阵 (三元组表示)
# ==========================================

class SparseMatrix:
    """稀疏矩阵的三元组表示

    每个非零元素存储为 (row, col, value)
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.triples = []  # [(row, col, value), ...]

    def set(self, row, col, value):
        # 查找是否已存在
        for i, (r, c, v) in enumerate(self.triples):
            if r == row and c == col:
                if value == 0:
                    self.triples.pop(i)
                else:
                    self.triples[i] = (row, col, value)
                return
        if value != 0:
            self.triples.append((row, col, value))
            self.triples.sort()  # 按行列排序

    def get(self, row, col):
        for r, c, v in self.triples:
            if r == row and c == col:
                return v
        return 0

    def transpose(self):
        """转置: 行列互换, 然后重排"""
        result = SparseMatrix(self.cols, self.rows)
        for r, c, v in self.triples:
            result.triples.append((c, r, v))
        result.triples.sort()
        return result

    def display_triples(self):
        print(f"  三元组表 ({len(self.triples)} 个非零元素):")
        print(f"  {'行':>4s} {'列':>4s} {'值':>6s}")
        for r, c, v in self.triples:
            print(f"  {r:>4d} {c:>4d} {v:>6g}")

    def display_matrix(self):
        for i in range(self.rows):
            row = [self.get(i, j) for j in range(self.cols)]
            print(f"  {row}")


def symmetric_demo():
    """对称矩阵演示"""
    print("=" * 60)
    print("对称矩阵的压缩存储")
    print("=" * 60)

    sm = SymmetricMatrix(4)
    # 设置下三角
    values = [
        (1, 1, 1), (2, 1, 2), (2, 2, 3),
        (3, 1, 4), (3, 2, 5), (3, 3, 6),
        (4, 1, 7), (4, 2, 8), (4, 3, 9), (4, 4, 10),
    ]
    for i, j, v in values:
        sm.set(i, j, v)

    print(f"\n  压缩数组: {sm.data}")
    print(f"  元素数量: n*(n+1)/2 = {sm.n * (sm.n + 1) // 2}")
    print(f"\n  还原矩阵:")
    sm.display_matrix()
    print(f"\n  映射公式 (i >= j): k = i*(i-1)/2 + j - 1")
    print(f"  例: a(3,2) → k = 3*2/2 + 2 - 1 = {3 * 2 // 2 + 2 - 1}, data[{3 * 2 // 2 + 2 - 1}] = {sm.get(3, 2)}")
    print()


def tridiagonal_demo():
    """三对角矩阵演示"""
    print("=" * 60)
    print("三对角矩阵的压缩存储")
    print("=" * 60)

    n = 5
    tm = TridiagonalMatrix(n)
    # 设置三条对角线
    for i in range(1, n + 1):
        tm.set(i, i, i * 10)        # 主对角
        if i > 1:
            tm.set(i, i - 1, -(i - 1))  # 下对角
        if i < n:
            tm.set(i, i + 1, i)      # 上对角

    print(f"\n  三对角矩阵 ({n}×{n}):")
    tm.display_matrix()
    print(f"\n  压缩数组: {tm.data}")
    print(f"  元素数量: 3n-2 = {3 * n - 2}")
    print(f"\n  映射公式: k = 2*i + j - 3")
    print(f"  例: a(3,2) → k = 2*3 + 2 - 3 = {2 * 3 + 2 - 3}, data[{2 * 3 + 2 - 3}] = {tm.get(3, 2)}")
    print()


def sparse_demo():
    """稀疏矩阵演示"""
    print("=" * 60)
    print("稀疏矩阵的三元组存储")
    print("=" * 60)

    sp = SparseMatrix(4, 5)
    non_zeros = [(0, 1, 3), (0, 4, 5), (1, 2, 1), (2, 0, 2), (3, 3, 7)]
    for r, c, v in non_zeros:
        sp.set(r, c, v)

    print(f"\n  原矩阵 ({sp.rows}×{sp.cols}):")
    sp.display_matrix()
    sp.display_triples()

    print(f"\n  转置后:")
    tp = sp.transpose()
    tp.display_matrix()
    tp.display_triples()
    print()


if __name__ == "__main__":
    symmetric_demo()
    tridiagonal_demo()
    sparse_demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 对称矩阵 (下三角存储):
     k = i*(i-1)/2 + j - 1  (i >= j, 1-indexed)
     共 n*(n+1)/2 个元素

  2. 三角矩阵:
     下三角: 同对称矩阵公式, 上三角存一个常数
     共 n*(n+1)/2 + 1 个元素

  3. 三对角矩阵:
     k = 2*i + j - 3  (1-indexed)
     已知 k 反推: i = (k+1)//3 + 1
     共 3n - 2 个元素

  4. 稀疏矩阵:
     三元组表: (行, 列, 值)
     十字链表: 行链表 + 列链表
     转置: 行列互换后按行排序
    """)
