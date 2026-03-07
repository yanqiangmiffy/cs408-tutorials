"""
快速排序 (Quick Sort)

时间复杂度:
  - 平均: O(n log n)
  - 最坏: O(n²)  (有序数组 + 选末尾为 pivot)
空间复杂度: O(log n)  (递归栈)
稳定性: 不稳定

核心思想:
  分治策略。选末尾元素为 pivot，partition 后 pivot 左边全 ≤ pivot，
  右边全 > pivot，pivot 归位。递归处理两侧。

关键步骤:
  1. partition：i=low-1，j 遍历 low~high-1
  2. arr[j] ≤ pivot 时 i++，交换 arr[i] 和 arr[j]
  3. 循环结束，交换 arr[i+1] 和 arr[high]，返回 i+1
  4. 递归对 [low, pi-1] 和 [pi+1, high] 排序
"""


def partition(arr: list, low: int, high: int) -> int:
    """Lomuto 分区方案"""
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort(arr: list, low: int = 0, high: int = None) -> list:
    """原地快速排序，返回排序后的数组"""
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
    """模拟手写排序过程"""
    print("=" * 60)
    print("快速排序 · 手写排序过程")
    print("=" * 60)
    traces = [
        ("初始", [5, 3, 8, 1, 9, 2], "pivot=2(末尾)"),
        ("partition", [1, 2, 8, 5, 9, 3], "2 归位 idx=1"),
        ("左递归", [1, 2, 8, 5, 9, 3], "[1] 归位"),
        ("右递归", [1, 2, 3, 5, 8, 9], "[8,5,9,3] 继续分"),
        ("完成", [1, 2, 3, 5, 8, 9], ""),
    ]
    for label, arr, note in traces:
        arr_str = " ".join(f" {v} " for v in arr)
        print(f"  {label:10s} → {arr_str}  {note}")
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

    print("\n\n批量测试:")
    for tc in test_cases:
        original = tc.copy()
        result = quick_sort(tc)
        status = "✓" if result == sorted(original) else "✗"
        print(f"  {status} {original} → {result}")
