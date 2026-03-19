"""
快速排序 (Quick Sort)

时间复杂度:
  - 平均: O(n log n)
  - 最坏: O(n²)  (有序数组 + 选末尾为 pivot)
空间复杂度: O(log n)  (递归栈)
稳定性: 不稳定

核心思想:
  分治策略。选 pivot 元素，partition 后 pivot 左边全 ≤ pivot，
  右边全 > pivot，pivot 归位。递归处理两侧。

分区策略:
  1. 王道挖坑法：双指针从两边向中间交替填坑（王道考研标准写法）
  2. Lomuto 分区：单指针 j 正向扫描，pivot 取自最后一个元素
  3. Hoare 分区：双指针 i/j 对向夹逼，pivot 取自第一个元素

Pivot 选择策略:
  - 末尾元素：pivot = arr[high]（简单易写，常考）
  - 首元素：pivot = arr[low]（王道挖坑法常用）
  - 中间元素：pivot = arr[(low+high)//2]
  - 随机元素：pivot = arr[random]（避免最坏情况）
  - 三数取中：取首、中、末的中位数（实用优化）
"""


# ============================================================================
# ① 王道挖坑法（Wang Dao Hole Method）
# ============================================================================

def partition_hole(arr: list, low: int, high: int) -> int:
    """
    王道挖坑法分区

    核心思想：用 pivot 挖一个"坑"，从两边向中间交替填坑，
    最后把 pivot 放入最终坑位。

    适用于：王道考研教材标准写法，常考

    步骤：
      1. pivot = arr[low]，挖坑，取出 pivot
      2. 从右向左找比 pivot 小的元素填坑
      3. 从左向右找比 pivot 大的元素填坑
      4. 重复直到 low >= high
      5. arr[low] = = pivot，pivot 归位
    """
    pivot = arr[low]  # 挖坑，取出 pivot
    while low < high:
        # 从右向左找比 pivot 小的元素填坑
        while low < high and arr[high] >= pivot:
            high -= 1
        arr[low] = arr[high]  # 填坑，新坑位在 high

        # 从左向右找比 pivot 大的元素填坑
        while low < high and arr[low] <= pivot:
            low += 1
        arr[high] = arr[low]  # 填坑，新坑位在 low

    arr[low] = pivot  # pivot 归位
    return low  # 返回 pivot 最终位置


def quick_sort_hole(arr: list, low: int = 0, high: int = None) -> list:
    """王道挖坑法快速排序"""
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot_idx = partition_hole(arr, low, high)
        quick_sort_hole(arr, low, pivot_idx - 1)
        quick_sort_hole(arr, pivot_idx + 1, high)
    return arr


# ============================================================================
# ② Lomuto 分区（单指针正向扫描）
# ============================================================================

def partition_lomuto(arr: list, low: int, high: int) -> int:
    """
    Lomuto 分区：单指针 j 正向扫描

    核心思想：用单指针 i 维护"≤ pivot"区域的边界，
    指针 j 正向扫描整个区间。

    适用于：简单易写，适合手写

    步骤：
      1. pivot = arr[high]，pivot 取自最后一个元素
      2. i = low - 1，i 维护 ≤ pivot 区域的边界
      3. j 从 low 扫到 high-1，arr[j] ≤ pivot 时 i++ 并交换
      4. 循环结束，交换 arr[i+1] 和 arr[high]，pivot 归位
    """
    pivot = arr[high]  # pivot 取自最后一个元素
    i = low - 1  # i 维护 ≤ pivot 区域的边界

    for j in range(low, high):  # j 正向扫描
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # 交换

    # pivot 归位
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort_lomuto(arr: list, low: int = 0, high: int = None) -> list:
    """Lomuto 分区快速排序"""
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot_idx = partition_lomuto(arr, low, high)
        quick_sort_lomuto(arr, low, pivot_idx - 1)
        quick_sort_lomuto(arr, pivot_idx + 1, high)
    return arr


# ============================================================================
# ③ Hoare 分区（双指针对向夹逼）
# ============================================================================

def partition_hoare(arr: list, low: int, high: int) -> int:
    """
    Hoare 分区：双指针 i/j 对向夹逼

    核心思想：双指针 i 从左、j 从右向中间夹逼，
    相遇时返回边界。

    适用于：原始 Hoare 版本，指针对向夹逼

    步骤：
      1. pivot = arr[low]，pivot 取自第一个元素
      2. i 从左向右找 ≥ pivot 的元素
      3. j 从右向左找 ≤ pivot 的元素
      4. 若 i <= j，交换 arr[i] 和 arr[j]，继续
      5. 返回 j 作为分割点

    注意：递归时边界为 [low, j] 和 [j+1, high]
    """
    pivot = arr[low]  # pivot 取自第一个元素
    i, j = low, high

    while i <= j:
        # i 向右找 ≥ pivot 的元素
        while i <= j and arr[i] < pivot:
            i += 1
        # j 向左找 ≤ pivot 的元素
        while i <= j and arr[j] > pivot:
            j -= 1
        if i <= j:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1

    return j  # 返回分割点


def quick_sort_hoare(arr: list, low: int = 0, high: int = None) -> list:
    """Hoare 分区快速排序"""
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot_idx = partition_hoare(arr, low, high)
        quick_sort_hoare(arr, low, pivot_idx)
        quick_sort_hoare(arr, pivot_idx + 1, high)
    return arr


# ============================================================================
# 默认实现（Lomuto 分区）
# ============================================================================

def partition(arr: list, low: int, high: int) -> int:
    """Lomuto 分区方案（默认）"""
    return partition_lomuto(arr, low, high)


def quick_sort(arr: list, low: int = 0, high: int = None) -> list:
    """原地快速排序，返回排序后的数组（默认使用 Lomuto 分区）"""
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)
    return arr


def quick_sort_verbose(arr: list, low: int = 0, high: int = None, depth: int = 0) -> list:
    """带详细输出的快速排序"""
    if high is None:
        arr = arr.copy()
        high = len(arr) - 1
        print(f"初始数组: {arr}")
        print("=" * 50)

    indent = "  " * depth
    if low < high:
        pivot = arr[high]
        print(f"\n{indent}quick_sort({arr[low:high + 1]}, low={low}, high={high})")
        print(f"{indent}  pivot = arr[{high}] = {pivot}")

        # 执行 partition
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        pi = i + 1

        print(f"{indent}  partition 后: {arr}, pivot 归位于 idx={pi}")
        print(f"{indent}  左半: {arr[low:pi]}  右半: {arr[pi + 1:high + 1]}")

        quick_sort_verbose(arr, low, pi - 1, depth + 1)
        quick_sort_verbose(arr, pi + 1, high, depth + 1)
    elif low == high:
        print(f"\n{indent}单元素 arr[{low}]={arr[low]}，不需要排序")

    if depth == 0:
        print("\n" + "=" * 50)
        print(f"排序结果: {arr}")
    return arr


def hand_trace():
    """模拟手写排序过程（王道挖坑法）"""
    print("=" * 60)
    print("快速排序 · 王道挖坑法手写排序过程")
    print("=" * 60)
    traces = [
        ("初始", [5, 3, 8, 1, 9, 2], "pivot=5(首元素)，挖坑 idx=0"),
        ("第1步2填坑", [2, 3, 8, 1, 9, 0], "坑位到 idx=5"),
        ("第2步8填坑", [2, 3, 0, 1, 9, 8], "坑位到 idx=2"),
        ("第3步1填坑", [2, 3, 1, 0, 9, 8], "坑位到 idx=3"),
        ("pivot归位", [2, 3, 1, 5, 9, 8], "5 归位 idx=3"),
        ("左递归", [1, 2, 3, 5, 9, 8], "[2,3,1] 排序"),
        ("右递归", [1, 2, 3, 5, 8, 9], "[9,8] 排序"),
        ("完成", [1, 2, 3, 5, 8, 9], ""),
    ]
    for label, arr, note in traces:
        arr_str = " ".join(f" {v} " for v in arr)
        print(f"  {label:12s} → {arr_str}  {note}")
    print()


if __name__ == "__main__":
    test_cases = [
        [5, 3, 8, 1, 9, 2],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 1, 4, 1, 5, 9, 2, 6],
        [],
        [1],
    ]

    print("=" * 60)
    print("快速排序 (Quick Sort)")
    print("=" * 60)

    hand_trace()

    print("\n详细排序过程:")
    quick_sort_verbose([5, 3, 8, 1, 9, 2])

    print("\n" + "=" * 60)
    print("三种分区策略对比")
    print("=" * 60)

    for tc in [[5, 3, 8, 1, 9, 2]]:
        print(f"\n测试数组: {tc}")
        print("-" * 60)

        # 王道挖坑法
        arr = tc.copy()
        result_hole = quick_sort_hole(arr)
        print(f"王道挖坑法:      {result_hole}")

        # Lomuto 分区
        arr = tc.copy()
        result_lomuto = quick_sort_lomuto(arr)
        print(f"Lomuto 分区:     {result_lomuto}")

        # Hoare 分区
        arr = tc.copy()
        result_hoare = quick_sort_hoare(arr)
        print(f"Hoare 分区:      {result_hoare}")

    print("\n" + "=" * 60)
    print("批量测试")
    print("=" * 60)

    for tc in test_cases:
        original = tc.copy()
        result = quick_sort(tc)
        status = "✓" if result == sorted(original) else "✗"
        print(f"  {status} {original} → {result}")
