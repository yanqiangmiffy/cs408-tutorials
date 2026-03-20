"""
算法的空间复杂度

空间复杂度: 算法执行过程中所需的额外存储空间随问题规模 n 的增长趋势
S(n) = O(g(n))

注意: 空间复杂度只计算「额外」辅助空间，不包括输入数据本身所占空间

常见空间复杂度:
  O(1)     - 原地算法 (如冒泡排序、插入排序)
  O(log n) - 递归深度 log n (如快速排序的栈空间)
  O(n)     - 需要额外 n 大小的辅助空间 (如归并排序)
  O(n²)    - 二维矩阵

考研要点:
  - 递归算法的空间复杂度 = O(递归深度)
  - 原地算法: 只使用常数个额外变量
"""

import sys


def space_o1():
    """O(1) 空间复杂度: 常数个额外变量"""
    print("=" * 60)
    print("O(1) 空间复杂度 - 原地算法")
    print("=" * 60)

    arr = [5, 3, 8, 1, 9, 2]
    print(f"\n  冒泡排序 (原地):")
    print(f"  输入: {arr}")

    # 冒泡排序只用了 swapped, i, j, 临时变量 → O(1)
    n = len(arr)
    for i in range(n):
        swapped = False            # 额外变量1
        for j in range(n - i - 1): # 额外变量2
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # 原地交换
                swapped = True     # 额外变量3
        if not swapped:
            break

    print(f"  输出: {arr}")
    print(f"  额外空间: 只用了 i, j, swapped 三个变量 → S(n) = O(1)")
    print()


def space_on():
    """O(n) 空间复杂度: 需要额外 n 大小辅助空间"""
    print("=" * 60)
    print("O(n) 空间复杂度 - 归并排序")
    print("=" * 60)

    def merge_sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])    # 创建新数组
        right = merge_sort(arr[mid:])   # 创建新数组
        result = []                     # 额外 O(n) 空间
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i]); i += 1
            else:
                result.append(right[j]); j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    arr = [5, 3, 8, 1, 9, 2]
    print(f"\n  归并排序:")
    print(f"  输入: {arr}")
    result = merge_sort(arr)
    print(f"  输出: {result}")
    print(f"  额外空间: 合并时需要 O(n) 大小辅助数组 + O(log n) 栈空间")
    print(f"  → S(n) = O(n)")
    print()


def space_ologn():
    """O(log n) 空间复杂度: 递归深度"""
    print("=" * 60)
    print("O(log n) 空间复杂度 - 递归")
    print("=" * 60)

    call_depth = [0]
    max_depth = [0]

    def binary_search_recursive(arr, target, low, high):
        call_depth[0] += 1
        max_depth[0] = max(max_depth[0], call_depth[0])

        if low > high:
            call_depth[0] -= 1
            return -1
        mid = (low + high) // 2
        if arr[mid] == target:
            call_depth[0] -= 1
            return mid
        elif arr[mid] < target:
            result = binary_search_recursive(arr, target, mid + 1, high)
        else:
            result = binary_search_recursive(arr, target, low, mid - 1)
        call_depth[0] -= 1
        return result

    arr = list(range(0, 100, 5))  # [0, 5, 10, ..., 95]
    target = 45
    print(f"\n  二分查找 (递归版):")
    print(f"  数组长度: {len(arr)}, 查找目标: {target}")

    idx = binary_search_recursive(arr, target, 0, len(arr) - 1)
    print(f"  找到位置: {idx}")
    print(f"  最大递归深度: {max_depth[0]}")
    print(f"  → 每层递归只用常数空间，栈深度 = O(log n)")
    print(f"  → S(n) = O(log n)")
    print()


def space_on2():
    """O(n²) 空间复杂度: 二维矩阵"""
    print("=" * 60)
    print("O(n²) 空间复杂度 - 二维矩阵")
    print("=" * 60)

    n = 4
    # 创建 n×n 邻接矩阵
    adj_matrix = [[0] * n for _ in range(n)]
    edges = [(0, 1), (0, 2), (1, 3), (2, 3)]
    for u, v in edges:
        adj_matrix[u][v] = 1
        adj_matrix[v][u] = 1

    print(f"\n  图的邻接矩阵 ({n}个顶点):")
    for i, row in enumerate(adj_matrix):
        print(f"  {i}: {row}")
    print(f"  需要 {n}×{n} = {n*n} 个存储单元 → S(n) = O(n²)")
    print()


def recursion_space_demo():
    """递归算法的空间复杂度分析"""
    print("=" * 60)
    print("递归算法的空间复杂度分析")
    print("=" * 60)

    print("""
  递归空间 = O(递归调用的最大深度)

  ┌────────────────────────────────────────────────┐
  │ 算法              递归深度       空间复杂度    │
  │────────────────────────────────────────────────│
  │ 二分查找          O(log n)       O(log n)      │
  │ 快速排序(最好)    O(log n)       O(log n)      │
  │ 快速排序(最坏)    O(n)           O(n)          │
  │ 归并排序          O(log n)+O(n)  O(n)          │
  │ 斐波那契(朴素)    O(n)           O(n)          │
  │ 全排列            O(n)           O(n)          │
  └────────────────────────────────────────────────┘

  注: 递归每深入一层，系统栈会保存:
      - 局部变量
      - 参数
      - 返回地址
    """)

    # 演示: 递归深度对比
    def factorial_recursive(n, depth=1):
        """阶乘: 递归深度 = n → O(n)"""
        if n <= 1:
            print(f"    {'  ' * depth}到达底部, 深度={depth}")
            return 1
        return n * factorial_recursive(n - 1, depth + 1)

    print("  阶乘递归 f(5) 的调用栈深度:")
    result = factorial_recursive(5)
    print(f"  结果: 5! = {result}")
    print(f"  递归深度 = n = 5 → S(n) = O(n)")
    print()


if __name__ == "__main__":
    space_o1()
    space_on()
    space_ologn()
    space_on2()
    recursion_space_demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 空间复杂度常见值:
     O(1): 冒泡, 插入, 选择, 希尔, 堆排序
     O(log n): 快速排序 (递归栈), 二分查找 (递归版)
     O(n): 归并排序, 计数排序, 基数排序
     O(n²): 邻接矩阵

  2. 递归算法空间 = O(递归深度)
     - 每层额外空间固定 → 总空间 = 层数 × 每层空间

  3. 原地算法: S(n) = O(1)
     只使用常数个额外辅助变量

  4. 空间换时间:
     散列表: 用 O(n) 空间换 O(1) 查找时间
     动态规划: 用 O(n) 空间避免重复计算
    """)
