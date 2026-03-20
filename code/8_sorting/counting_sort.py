"""
计数排序 (Counting Sort)

时间复杂度:
  - 平均: O(n+k)
  - 最坏: O(n+k)
空间复杂度: O(k)
稳定性: 稳定

核心思想:
  非比较排序。统计每个值出现次数，前缀和得出各值的最终位置，
  反向遍历原数组写入输出（反向保证稳定）。
  k 为值域范围，k 过大时不适用。

关键步骤:
  1. count[v-min]++ 统计每个值频次
  2. 前缀和：count[i] += count[i-1]，得排名
  3. 反向遍历原数组：output[count[v]-1]=v，count[v]--
  4. output 写回 arr
"""


def counting_sort(arr: list) -> list:
    """计数排序，返回新的排序数组"""
    if not arr:
        return arr
    max_val = max(arr)
    min_val = min(arr)
    k = max_val - min_val + 1

    # 计数数组
    count = [0] * k
    for num in arr:
        count[num - min_val] += 1

    # 累加（使稳定）
    for i in range(1, k):
        count[i] += count[i - 1]

    # 反向填充输出数组
    output = [0] * len(arr)
    for num in reversed(arr):
        output[count[num - min_val] - 1] = num
        count[num - min_val] -= 1

    return output


def counting_sort_verbose(arr: list) -> list:
    """带详细输出的计数排序"""
    arr = arr.copy()
    if not arr:
        print("空数组，无需排序")
        return arr

    n = len(arr)
    max_val = max(arr)
    min_val = min(arr)
    k = max_val - min_val + 1

    print(f"初始数组: {arr}")
    print(f"n={n}, 值域: [{min_val}, {max_val}], k={k}")
    print("=" * 50)

    # 计数
    count = [0] * k
    for num in arr:
        count[num - min_val] += 1
    print(f"\n1. 计数结果 (值→次数):")
    for i, c in enumerate(count):
        if c > 0:
            print(f"   值 {i + min_val}: {c} 次")

    # 前缀和
    print(f"\n2. 前缀和:")
    print(f"   累加前: {count}")
    for i in range(1, k):
        count[i] += count[i - 1]
    print(f"   累加后: {count}")

    # 反向填充
    print(f"\n3. 反向遍历原数组，写入输出:")
    output = [0] * n
    for num in reversed(arr):
        pos = count[num - min_val] - 1
        output[pos] = num
        count[num - min_val] -= 1
        print(f"   num={num}, 放入 output[{pos}], count[{num - min_val}] → {count[num - min_val]}")

    print(f"\n" + "=" * 50)
    print(f"排序结果: {output}")
    return output


def hand_trace():
    """模拟手写排序过程"""
    print("=" * 60)
    print("计数排序 · 手写排序过程")
    print("=" * 60)
    traces = [
        ("初始", [3, 1, 4, 1, 5, 2], "值域 1~5，k=5"),
        ("计数", [3, 1, 4, 1, 5, 2], "count=[2,1,1,1,1]（1出现2次）"),
        ("前缀和", [3, 1, 4, 1, 5, 2], "count=[2,3,4,5,6]"),
        ("回填", [1, 1, 2, 3, 4, 5], "按位置写入"),
    ]
    for label, arr, note in traces:
        arr_str = " ".join(f" {v} " for v in arr)
        print(f"  {label:8s} → {arr_str}  {note}")
    print()


if __name__ == "__main__":
    test_cases = [
        [3, 1, 4, 1, 5, 2],
        [5, 3, 8, 1, 9, 2],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 1, 4, 1, 5, 9, 2, 6],
        [],
        [1],
    ]

    print("=" * 60)
    print("计数排序 (Counting Sort)")
    print("=" * 60)

    hand_trace()

    print("\n详细排序过程:")
    counting_sort_verbose([3, 1, 4, 1, 5, 2])

    print("\n\n批量测试:")
    for tc in test_cases:
        original = tc.copy()
        result = counting_sort(tc)
        status = "✓" if result == sorted(original) else "✗"
        print(f"  {status} {original} → {result}")
