"""
简单选择排序 (Selection Sort)

时间复杂度:
  - 平均: O(n²)
  - 最坏: O(n²)
  - 最好: O(n²)  (比较次数固定 n(n-1)/2)
空间复杂度: O(1)
稳定性: 不稳定

核心思想:
  每轮在未排序区找最小值，与未排序区首元素交换。
  交换次数最少（≤n-1次），但比较次数固定 n(n-1)/2，
  不因有序而提前结束。

关键步骤:
  1. 外层 i 从 0 到 n-2，表示当前待填位置
  2. 内层 j 从 i+1 扫到末尾，记录最小值下标 min_idx
  3. 交换 arr[i] 与 arr[min_idx]
  4. 已排序区扩大，不稳定（交换可能越过相同元素）
"""


def selection_sort(arr: list) -> list:
    """原地选择排序，返回排序后的数组"""
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def selection_sort_verbose(arr: list) -> list:
    """带详细输出的选择排序"""
    arr = arr.copy()
    n = len(arr)
    print(f"初始数组: {arr}")
    print(f"数组长度 n = {n}")
    print("=" * 50)

    for i in range(n):
        min_idx = i
        print(f"\ni={i}, 未排序区: {arr[i:]}")

        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        print(f"  最小值 arr[{min_idx}]={arr[min_idx]}")
        if min_idx != i:
            print(f"  交换 arr[{i}]={arr[i]} ↔ arr[{min_idx}]={arr[min_idx]}")
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        else:
            print(f"  arr[{i}]={arr[i]} 已是最小，不交换")
        print(f"  当前数组: {arr}")

    print("\n" + "=" * 50)
    print(f"排序结果: {arr}")
    return arr


def hand_trace():
    """模拟手写排序过程"""
    print("=" * 60)
    print("简单选择排序 · 手写排序过程")
    print("=" * 60)
    traces = [
        ("初始", [5, 3, 8, 1, 9, 2], []),
        ("i=0 找最小=1", [1, 3, 8, 5, 9, 2], [0], "1(idx3)↔5(idx0)"),
        ("i=1 找最小=2", [1, 2, 8, 5, 9, 3], [0, 1], "2(idx5)↔3(idx1)"),
        ("i=2 找最小=3", [1, 2, 3, 5, 9, 8], [0, 1, 2], "3(idx5)↔8(idx2)"),
        ("i=3 找最小=5", [1, 2, 3, 5, 9, 8], [0, 1, 2, 3], "5 不动"),
        ("完成", [1, 2, 3, 5, 8, 9], [0, 1, 2, 3, 4, 5]),
    ]
    for trace in traces:
        label, arr = trace[0], trace[1]
        note = trace[3] if len(trace) > 3 else ""
        highlight = trace[2]
        arr_str = " ".join(
            f"[{v}]" if i in highlight else f" {v} " for i, v in enumerate(arr)
        )
        print(f"  {label:14s} → {arr_str}  {note}")
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
    print("简单选择排序 (Selection Sort)")
    print("=" * 60)

    hand_trace()

    print("\n详细排序过程:")
    selection_sort_verbose([5, 3, 8, 1, 9, 2])

    print("\n\n批量测试:")
    for tc in test_cases:
        original = tc.copy()
        result = selection_sort(tc)
        status = "✓" if result == sorted(original) else "✗"
        print(f"  {status} {original} → {result}")
