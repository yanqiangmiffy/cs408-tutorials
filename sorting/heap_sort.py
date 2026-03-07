"""
堆排序 (Heap Sort)

时间复杂度:
  - 平均: O(n log n)
  - 最坏: O(n log n)
空间复杂度: O(1)
稳定性: 不稳定

核心思想:
  两阶段：① 建大根堆（从最后非叶节点向上 heapify）；
  ② 反复将堆顶（最大值）与末尾交换，堆大小减1，再对新堆顶 heapify。
  原地排序，不稳定。

关键步骤:
  1. 建堆：i 从 n//2-1 到 0，对每个 i 执行 heapify
  2. heapify：找左右孩子中最大者，若大于父节点则交换，递归下沉
  3. 排序：交换 arr[0] 和 arr[i]（i 从 n-1 到 1），对 arr[0] heapify
  4. 每次交换后有序区扩大一位
"""


def heapify(arr: list, n: int, i: int) -> None:
    """对以 i 为根的子树做大根堆调整，n 是堆大小"""
    largest = i
    l = 2 * i + 1  # 左孩子
    r = 2 * i + 2  # 右孩子

    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)  # 递归下沉


def heap_sort(arr: list) -> list:
    """原地堆排序，返回排序后的数组"""
    n = len(arr)

    # 建堆（从最后一个非叶节点开始）
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # 逐个取出堆顶
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # 堆顶交换到末尾
        heapify(arr, i, 0)               # 重新调整堆

    return arr


def heap_sort_verbose(arr: list) -> list:
    """带详细输出的堆排序"""
    arr = arr.copy()
    n = len(arr)
    print(f"初始数组: {arr}")
    print(f"数组长度 n = {n}")
    print("=" * 50)

    def heapify_v(size, i, phase=""):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < size and arr[l] > arr[largest]:
            largest = l
        if r < size and arr[r] > arr[largest]:
            largest = r
        if largest != i:
            print(f"  {phase}交换 arr[{i}]={arr[i]} ↔ arr[{largest}]={arr[largest]}")
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify_v(size, largest, phase)

    # 建堆
    print(f"\n阶段一：建大根堆")
    for i in range(n // 2 - 1, -1, -1):
        print(f"  heapify(i={i}), 当前节点值={arr[i]}")
        heapify_v(n, i, "  ")
    print(f"  建堆结果: {arr}  (堆顶={arr[0]})")

    # 排序
    print(f"\n阶段二：交换堆顶 + heapify")
    for i in range(n - 1, 0, -1):
        print(f"\n  交换 arr[0]={arr[0]} ↔ arr[{i}]={arr[i]}")
        arr[0], arr[i] = arr[i], arr[0]
        print(f"  {arr[i]} 归位, 堆大小缩到 {i}")
        heapify_v(i, 0, "  ")
        print(f"  当前: {arr}")

    print("\n" + "=" * 50)
    print(f"排序结果: {arr}")
    return arr


def print_heap_tree(arr: list, size: int = None):
    """可视化打印堆的树形结构"""
    if size is None:
        size = len(arr)
    if size == 0:
        print("  (空堆)")
        return

    import math
    height = int(math.log2(size)) + 1
    max_width = 2 ** height - 1

    idx = 0
    for level in range(height):
        count = min(2 ** level, size - idx)
        if count <= 0:
            break
        spacing = max_width // (2 ** level)
        line = ""
        for j in range(count):
            if idx + j < size:
                pad = spacing if j == 0 else spacing * 2
                line += f"{arr[idx + j]:^{pad}}"
        print(f"  {line}")
        idx += count


def hand_trace():
    """模拟手写排序过程"""
    print("=" * 60)
    print("堆排序 · 手写排序过程")
    print("=" * 60)
    traces = [
        ("初始", [5, 3, 8, 1, 9, 2], "先建大根堆"),
        ("建堆完成", [9, 5, 8, 1, 3, 2], "堆顶=最大值9"),
        ("交换堆顶↔末", [2, 5, 8, 1, 3, 9], "9 归位，堆大小-1"),
        ("heapify后", [8, 5, 2, 1, 3, 9], "8 成新堆顶"),
        ("再交换", [3, 5, 2, 1, 8, 9], "8 归位"),
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
    print("堆排序 (Heap Sort)")
    print("=" * 60)

    hand_trace()

    # 堆的树形结构
    print("堆的树形结构（建堆后）:")
    demo = [5, 3, 8, 1, 9, 2]
    n = len(demo)
    for i in range(n // 2 - 1, -1, -1):
        heapify(demo, n, i)
    print_heap_tree(demo)

    print("\n详细排序过程:")
    heap_sort_verbose([5, 3, 8, 1, 9, 2])

    print("\n\n批量测试:")
    for tc in test_cases:
        original = tc.copy()
        result = heap_sort(tc)
        status = "✓" if result == sorted(original) else "✗"
        print(f"  {status} {original} → {result}")
