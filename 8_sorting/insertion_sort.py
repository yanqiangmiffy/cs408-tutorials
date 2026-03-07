"""
直接插入排序 (Insertion Sort)

时间复杂度:
  - 平均: O(n²)
  - 最坏: O(n²)  (逆序)
  - 最好: O(n)   (已有序)
空间复杂度: O(1)
稳定性: 稳定

核心思想:
  类似抓扑克牌。左侧维护已排序区，每次取右侧第一个元素，
  向左找到合适位置插入，其余元素右移一位。

关键步骤:
  1. 从 i=1 开始，取 key = arr[i]
  2. j 从 i-1 向左扫，arr[j] > key 则 arr[j+1]=arr[j]，j--
  3. 退出循环后，arr[j+1] = key
  4. 每插入一次，有序区扩大一位
"""


def insertion_sort(arr: list) -> list:
    """原地插入排序，返回排序后的数组"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def insertion_sort_verbose(arr: list) -> list:
    """带详细输出的插入排序"""
    arr = arr.copy()
    n = len(arr)
    print(f"初始数组: {arr}")
    print(f"数组长度 n = {n}")
    print("=" * 50)

    for i in range(1, n):
        key = arr[i]
        j = i - 1
        print(f"\ni={i}, key={key}, 有序区: {arr[:i]}")

        moves = 0
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            print(f"  arr[{j}]={arr[j]} 右移到 arr[{j + 1}]")
            j -= 1
            moves += 1

        arr[j + 1] = key
        print(f"  key={key} 插入到 arr[{j + 1}]")
        print(f"  当前数组: {arr}  (移动了 {moves} 次)")

    print("\n" + "=" * 50)
    print(f"排序结果: {arr}")
    return arr


def hand_trace():
    """模拟手写排序过程"""
    print("=" * 60)
    print("直接插入排序 · 手写排序过程")
    print("=" * 60)
    traces = [
        ("初始", [5, 3, 8, 1, 9, 2], []),
        ("i=1 插入3", [3, 5, 8, 1, 9, 2], [0, 1], "3 插到 5 前"),
        ("i=2 插入8", [3, 5, 8, 1, 9, 2], [0, 1, 2], "8 不动"),
        ("i=3 插入1", [1, 3, 5, 8, 9, 2], [0, 1, 2, 3], "1 插到最前"),
        ("i=4 插入9", [1, 3, 5, 8, 9, 2], [0, 1, 2, 3, 4], "9 不动"),
        ("i=5 插入2", [1, 2, 3, 5, 8, 9], [0, 1, 2, 3, 4, 5], "2 插到第2位"),
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
    test_cases = [
        [5, 3, 8, 1, 9, 2],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 1, 4, 1, 5, 9, 2, 6],
        [],
        [1],
    ]

    print("=" * 60)
    print("直接插入排序 (Insertion Sort)")
    print("=" * 60)

    hand_trace()

    print("\n详细排序过程:")
    insertion_sort_verbose([5, 3, 8, 1, 9, 2])

    print("\n\n批量测试:")
    for tc in test_cases:
        original = tc.copy()
        result = insertion_sort(tc)
        status = "✓" if result == sorted(original) else "✗"
        print(f"  {status} {original} → {result}")
