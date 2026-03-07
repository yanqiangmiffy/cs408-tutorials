"""
算法的时间复杂度

时间复杂度: 算法执行时间随问题规模 n 的增长趋势
大O表示法: T(n) = O(f(n)) 表示最坏情况上界

常见时间复杂度 (从小到大):
  O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2^n) < O(n!)

考研要点:
  - 掌握大O表示法的定义和求解方法
  - 注意最好、最坏、平均时间复杂度的区别
  - 常见代码模式对应的复杂度
  - 加法规则: T = T1 + T2 → O(max(f1, f2))
  - 乘法规则: T = T1 × T2 → O(f1 × f2)
"""

import time
import math


def constant_time(n):
    """O(1) - 常数时间: 与 n 无关"""
    x = n + 1        # 1 次
    y = x * 2        # 1 次
    return y          # 总共有限次操作


def logarithmic_time(n):
    """O(log n) - 对数时间: 每次缩小一半"""
    count = 0
    i = 1
    while i < n:
        i *= 2   # i: 1, 2, 4, 8, ... → 循环 log₂n 次
        count += 1
    return count


def linear_time(n):
    """O(n) - 线性时间: 遍历一次"""
    total = 0
    for i in range(n):    # 循环 n 次
        total += i
    return total


def nlogn_time(arr):
    """O(n log n) - 线性对数时间: 典型如归并排序"""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = nlogn_time(arr[:mid])     # 递归 log n 层
    right = nlogn_time(arr[mid:])
    # 每层合并 O(n)
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quadratic_time(n):
    """O(n²) - 平方时间: 双重循环"""
    count = 0
    for i in range(n):          # 外层 n 次
        for j in range(n):      # 内层 n 次
            count += 1          # 总共 n² 次
    return count


def cubic_time(n):
    """O(n³) - 立方时间: 三重循环"""
    count = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                count += 1
    return count


# ==========================================
# 常见考研代码的复杂度分析
# ==========================================

def analyze_examples():
    """常见代码模式的时间复杂度分析"""
    print("=" * 60)
    print("常见代码模式的时间复杂度分析")
    print("=" * 60)

    # 例1: 顺序执行 → 加法规则
    print("""
  例1: 加法规则 T(n) = O(max(f1, f2))
  ┌──────────────────────────────┐
  │ for i in range(n):     # O(n) │
  │     ...                       │
  │ for i in range(n):           │
  │     for j in range(n): # O(n²)│
  │         ...                   │
  │ → T(n) = O(n) + O(n²) = O(n²)│
  └──────────────────────────────┘
    """)

    # 例2: 嵌套执行 → 乘法规则
    print("""
  例2: 乘法规则 T(n) = O(f1 × f2)
  ┌──────────────────────────────┐
  │ for i in range(n):     # O(n) │
  │     for j in range(i): # O(n) │
  │         ...                   │
  │ → 0+1+2+...+(n-1) = n(n-1)/2 │
  │ → T(n) = O(n²)               │
  └──────────────────────────────┘
    """)

    # 例3: 对数时间
    print("""
  例3: 对数时间
  ┌──────────────────────────────┐
  │ i = n                        │
  │ while i > 1:                 │
  │     i = i // 2         # 每次减半│
  │ → 循环 log₂n 次              │
  │ → T(n) = O(log n)            │
  └──────────────────────────────┘
    """)

    # 例4: 递归
    print("""
  例4: 递归的时间复杂度
  ┌──────────────────────────────┐
  │ def f(n):                     │
  │     if n <= 1: return 1       │
  │     return f(n-1) + f(n-2)    │
  │                               │
  │ → 斐波那契递归: T(n) = O(2^n) │
  │                               │
  │ def f(n):                     │
  │     if n <= 1: return 1       │
  │     return f(n-1) + 1         │
  │                               │
  │ → 线性递归: T(n) = O(n)       │
  └──────────────────────────────┘
    """)


def complexity_comparison():
    """直观比较不同复杂度的增长速度"""
    print("=" * 60)
    print("复杂度增长速度对比")
    print("=" * 60)

    print(f"\n  {'n':>8s} {'O(1)':>6s} {'O(logn)':>8s} {'O(n)':>8s} "
          f"{'O(nlogn)':>10s} {'O(n²)':>10s} {'O(2^n)':>12s}")
    print("  " + "-" * 62)

    for n in [10, 100, 1000, 10000, 100000]:
        o1 = 1
        ologn = int(math.log2(n)) if n > 0 else 0
        on = n
        onlogn = n * ologn
        on2 = n * n
        o2n = "溢出" if n > 30 else str(2 ** n)

        print(f"  {n:>8d} {o1:>6d} {ologn:>8d} {on:>8d} "
              f"{onlogn:>10d} {on2:>10d} {o2n:>12s}")

    print()


def timing_demo():
    """实际测量不同复杂度的运行时间"""
    print("=" * 60)
    print("实际运行时间测量")
    print("=" * 60)

    test_sizes = [100, 1000, 5000, 10000]

    print(f"\n  {'n':>8s} {'O(1)':>12s} {'O(log n)':>12s} "
          f"{'O(n)':>12s} {'O(n²)':>12s}")
    print("  " + "-" * 52)

    for n in test_sizes:
        # O(1)
        start = time.perf_counter()
        constant_time(n)
        t1 = time.perf_counter() - start

        # O(log n)
        start = time.perf_counter()
        logarithmic_time(n)
        t2 = time.perf_counter() - start

        # O(n)
        start = time.perf_counter()
        linear_time(n)
        t3 = time.perf_counter() - start

        # O(n²)
        start = time.perf_counter()
        if n <= 10000:
            quadratic_time(n)
        t4 = time.perf_counter() - start

        print(f"  {n:>8d} {t1:>10.6f}s {t2:>10.6f}s "
              f"{t3:>10.6f}s {t4:>10.6f}s")

    print()


if __name__ == "__main__":
    analyze_examples()
    complexity_comparison()
    timing_demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 求时间复杂度步骤:
     ① 找基本操作 (执行最频繁的语句)
     ② 计算基本操作的执行次数 T(n)
     ③ 取 T(n) 的最高阶项，忽略系数 → O(f(n))

  2. 常见复杂度排序:
     O(1) < O(log n) < O(√n) < O(n) < O(n log n)
          < O(n²) < O(n³) < O(2^n) < O(n!)

  3. 注意事项:
     - log 底数不影响量级（换底公式只差常数倍）
     - 最好/最坏/平均三种情况要区分
     - 递归算法用递推方程求解
    """)
