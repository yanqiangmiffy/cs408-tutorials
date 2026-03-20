"""
希尔排序 (Shell Sort)

时间复杂度:
  - 平均: O(n log n) ~ O(n²)  (取决于步长序列)
  - 最坏: O(n²)  (使用 n/2 步长序列时)
空间复杂度: O(1)
稳定性: 不稳定

核心思想:
  插入排序的改进。先用大步长分组插排，使元素快速靠近目标；
  步长逐渐缩小至1，最后一次完整插排时数组已近乎有序，代价极小。

关键步骤:
  1. 初始 gap = n//2，每轮结束 gap //= 2
  2. 对每个 gap，从 i=gap 开始做插入排序（跨度为 gap）
  3. 重复直到 gap=1 完成最终插排
  4. 步长序列影响性能，常用 n//2, n//4... 或 Knuth 序列
"""


def shell_sort(arr: list) -> list:
    """原地希尔排序，返回排序后的数组"""
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr


def shell_sort_verbose(arr: list) -> list:
    """带详细输出的希尔排序"""
    arr = arr.copy()
    n = len(arr)
    print(f"初始数组: {arr}")
    print(f"数组长度 n = {n}")
    print("=" * 50)

    gap = n // 2
    round_num = 0
    while gap > 0:
        round_num += 1
        print(f"\n第 {round_num} 轮, gap = {gap}:")

        # 显示分组
        groups = {}
        for i in range(gap):
            group = [arr[j] for j in range(i, n, gap)]
            groups[i] = group
        print(f"  分组: {list(groups.values())}")

        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp

        print(f"  排序后: {arr}")
        gap //= 2

    print("\n" + "=" * 50)
    print(f"排序结果: {arr}")
    return arr


def hand_trace():
    """模拟手写排序过程"""
    print("=" * 60)
    print("希尔排序 · 手写排序过程")
    print("=" * 60)
    traces = [
        ("初始 [n=6]", [5, 3, 8, 1, 9, 2], "gap从3开始"),
        ("gap=3 分组", [1, 3, 8, 5, 9, 2], "[5,1],[3,9],[8,2] 各自插排"),
        ("gap=3 结果", [1, 3, 2, 5, 9, 8], "整体接近有序"),
        ("gap=1 插排", [1, 2, 3, 5, 8, 9], "代价很小"),
    ]
    for label, arr, note in traces:
        arr_str = " ".join(f" {v} " for v in arr)
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
    print("希尔排序 (Shell Sort)")
    print("=" * 60)

    hand_trace()

    print("\n详细排序过程:")
    shell_sort_verbose([5, 3, 8, 1, 9, 2])

    print("\n\n批量测试:")
    for tc in test_cases:
        original = tc.copy()
        result = shell_sort(tc)
        status = "✓" if result == sorted(original) else "✗"
        print(f"  {status} {original} → {result}")
