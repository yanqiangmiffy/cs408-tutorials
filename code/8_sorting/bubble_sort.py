"""
冒泡排序 (Bubble Sort)

时间复杂度:
  - 平均: O(n²)
  - 最坏: O(n²)
  - 最好: O(n)  (已有序时，设置 swapped 标记提前退出)
空间复杂度: O(1)
稳定性: 稳定

核心思想:
  相邻元素两两比较，较大的像气泡一样向右"冒"，
  每轮结束后最大值沉到末尾。若某轮未发生交换则提前结束。

关键步骤:
  1. 外层循环 i 控制轮次（共 n-1 轮）
  2. 内层 j 从 0 扫到 n-i-2，比较 arr[j] 与 arr[j+1]
  3. 若 arr[j] > arr[j+1] 则交换
  4. 设 swapped 标记，若整轮无交换则提前 break
"""


def bubble_sort(arr: list) -> list:
    """原地冒泡排序，返回排序后的数组"""
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def bubble_sort_verbose(arr: list) -> list:
    """带详细输出的冒泡排序，展示每一轮的过程"""
    arr = arr.copy()
    n = len(arr)
    print(f"初始数组: {arr}")
    print(f"数组长度 n = {n}")
    print("=" * 50)

    for i in range(n):
        swapped = False
        print(f"\n第 {i + 1} 轮 (i={i}):")
        for j in range(0, n - i - 1):
            print(f"  比较 arr[{j}]={arr[j]} 与 arr[{j + 1}]={arr[j + 1]}", end="")
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                print(f" → 交换! 当前: {arr}")
            else:
                print(f" → 不交换")
        print(f"  本轮结束: {arr}")

        if not swapped:
            print(f"\n本轮无交换，数组已有序，提前结束!")
            break

    print("\n" + "=" * 50)
    print(f"排序结果: {arr}")
    return arr


# ======== 手写排序过程 ========
def hand_trace():
    """模拟手写排序过程"""
    print("=" * 60)
    print("冒泡排序 · 手写排序过程")
    print("=" * 60)
    traces = [
        ("初始", [5, 3, 8, 1, 9, 2], []),
        ("第1轮 i=0", [3, 5, 1, 8, 2, 9], [5], "9 冒到末尾"),
        ("第2轮 i=1", [3, 1, 5, 2, 8, 9], [4, 5], "8 到位"),
        ("第3轮 i=2", [1, 3, 2, 5, 8, 9], [3, 4, 5], "5 到位"),
        ("第4轮 i=3", [1, 2, 3, 5, 8, 9], [2, 3, 4, 5], "3 到位"),
        ("完成", [1, 2, 3, 5, 8, 9], [0, 1, 2, 3, 4, 5]),
    ]
    for trace in traces:
        label, arr = trace[0], trace[1]
        note = trace[3] if len(trace) > 3 else ""
        highlight = trace[2]
        arr_str = " ".join(
            f"[{v}]" if i in highlight else f" {v} " for i, v in enumerate(arr)
        )
        print(f"  {label:12s} → {arr_str}  {note}")
    print()


if __name__ == "__main__":
    # 基本测试
    test_cases = [
        [5, 3, 8, 1, 9, 2],
        [1, 2, 3, 4, 5],       # 最好情况
        [5, 4, 3, 2, 1],       # 最坏情况
        [3, 1, 4, 1, 5, 9, 2, 6],
        [],
        [1],
    ]

    print("=" * 60)
    print("冒泡排序 (Bubble Sort)")
    print("=" * 60)

    # 手写过程演示
    hand_trace()

    # 详细排序过程
    print("\n详细排序过程:")
    bubble_sort_verbose([5, 3, 8, 1, 9, 2])

    # 批量测试
    print("\n\n批量测试:")
    for tc in test_cases:
        original = tc.copy()
        result = bubble_sort(tc)
        status = "✓" if result == sorted(original) else "✗"
        print(f"  {status} {original} → {result}")
