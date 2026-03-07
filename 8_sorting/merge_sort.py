"""
归并排序 (Merge Sort)

时间复杂度:
  - 平均: O(n log n)
  - 最坏: O(n log n)
  - 最好: O(n log n)
空间复杂度: O(n)
稳定性: 稳定

核心思想:
  分治策略。不断二分到单个元素（自然有序），再两两合并有序段。
  合并时双指针取小者填入。唯一能保证最坏 O(n log n) 的比较排序，
  代价是需要 O(n) 额外空间。

关键步骤:
  1. 递归拆分：mid = (lo+hi)//2，分别排左右两半
  2. 合并：left[i] 与 right[j] 比较，取小者放入 output
  3. 剩余部分直接追加
  4. 写回原数组对应区间
"""


def merge(left: list, right: list) -> list:
    """合并两个有序列表"""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(arr: list) -> list:
    """归并排序（非原地），返回新的排序数组"""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge_sort_verbose(arr: list, depth: int = 0) -> list:
    """带详细输出的归并排序"""
    indent = "  " * depth
    print(f"{indent}merge_sort({arr})")

    if len(arr) <= 1:
        print(f"{indent}  → 单元素，直接返回 {arr}")
        return arr

    mid = len(arr) // 2
    print(f"{indent}  拆分: 左={arr[:mid]}, 右={arr[mid:]}")

    left = merge_sort_verbose(arr[:mid], depth + 1)
    right = merge_sort_verbose(arr[mid:], depth + 1)

    # 合并过程
    result = []
    i = j = 0
    print(f"{indent}  合并 {left} + {right}:")
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            print(f"{indent}    取左 left[{i}]={left[i]}")
            result.append(left[i])
            i += 1
        else:
            print(f"{indent}    取右 right[{j}]={right[j]}")
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])

    print(f"{indent}  → 合并结果: {result}")
    return result


def hand_trace():
    """模拟手写排序过程"""
    print("=" * 60)
    print("归并排序 · 手写排序过程")
    print("=" * 60)
    traces = [
        ("初始", [5, 3, 8, 1, 9, 2], ""),
        ("拆分到底", [5, 3, 8, 1, 9, 2], "[5][3][8][1][9][2]"),
        ("两两合并", [3, 5, 1, 8, 2, 9], "[3,5][1,8][2,9]"),
        ("四合并二", [1, 3, 5, 8, 2, 9], "[1,3,5,8][2,9]"),
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
    print("归并排序 (Merge Sort)")
    print("=" * 60)

    hand_trace()

    print("\n详细排序过程:")
    merge_sort_verbose([5, 3, 8, 1, 9, 2])

    print("\n\n批量测试:")
    for tc in test_cases:
        original = tc.copy()
        result = merge_sort(tc)
        status = "✓" if result == sorted(original) else "✗"
        print(f"  {status} {original} → {result}")
