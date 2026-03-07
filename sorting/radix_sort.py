"""
基数排序 (Radix Sort)

时间复杂度:
  - 平均: O(d·(n+k))
  - 最坏: O(d·(n+k))
空间复杂度: O(n+k)
稳定性: 稳定

核心思想:
  非比较排序。LSD（低位优先）：从个位到最高位，每轮对该位做稳定的
  计数排序（10个桶）。d 轮后得到有序结果。依赖稳定子排序保证正确性。

关键步骤:
  1. exp=1 表示当前处理的位（个位十位…）
  2. 按 (num // exp) % 10 做计数排序（10个桶）
  3. 反向写回保证稳定性
  4. exp *= 10，直到最高位处理完毕
"""


def counting_sort_by_digit(arr: list, exp: int) -> None:
    """按指定位 (exp) 做计数排序（原地修改）"""
    n = len(arr)
    output = [0] * n
    count = [0] * 10  # 0~9 共10个桶

    # 统计当前位的数字出现次数
    for num in arr:
        digit = (num // exp) % 10
        count[digit] += 1

    # 累加前缀和
    for i in range(1, 10):
        count[i] += count[i - 1]

    # 反向填充保证稳定性
    for num in reversed(arr):
        digit = (num // exp) % 10
        output[count[digit] - 1] = num
        count[digit] -= 1

    # 写回原数组
    for i in range(n):
        arr[i] = output[i]


def radix_sort(arr: list) -> list:
    """基数排序（LSD），原地排序并返回"""
    if not arr:
        return arr
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10
    return arr


def radix_sort_verbose(arr: list) -> list:
    """带详细输出的基数排序"""
    arr = arr.copy()
    if not arr:
        print("空数组，无需排序")
        return arr

    print(f"初始数组: {arr}")
    max_val = max(arr)
    d = len(str(max_val))
    print(f"最大值: {max_val}, 位数 d={d}")
    print("=" * 50)

    exp = 1
    digit_names = ["个", "十", "百", "千", "万"]
    pass_num = 0
    while max_val // exp > 0:
        digit_name = digit_names[pass_num] if pass_num < len(digit_names) else f"10^{pass_num}"
        print(f"\n第 {pass_num + 1} 轮: 按{digit_name}位排序")

        # 显示各元素的当前位
        digits = [(num, (num // exp) % 10) for num in arr]
        print(f"  各元素{digit_name}位: {[(num, f'{digit_name}位={d}') for num, d in digits]}")

        # 分桶
        buckets = [[] for _ in range(10)]
        for num in arr:
            buckets[(num // exp) % 10].append(num)
        non_empty = {i: b for i, b in enumerate(buckets) if b}
        print(f"  桶: {non_empty}")

        counting_sort_by_digit(arr, exp)
        print(f"  结果: {arr}")

        exp *= 10
        pass_num += 1

    print("\n" + "=" * 50)
    print(f"排序结果: {arr}")
    return arr


def hand_trace():
    """模拟手写排序过程"""
    print("=" * 60)
    print("基数排序 · 手写排序过程")
    print("=" * 60)
    traces = [
        ("初始", [170, 45, 75, 90, 2, 24], "d=3位"),
        ("按个位排", [170, 90, 2, 24, 45, 75], "0,0,2,4,5,5"),
        ("按十位排", [2, 24, 45, 75, 170, 90], "0,2,4,7,7,9"),
        ("按百位排", [2, 24, 45, 75, 90, 170], "0,0,0,0,0,1"),
    ]
    for label, arr, note in traces:
        arr_str = " ".join(f"{v:3d}" for v in arr)
        print(f"  {label:10s} → [{arr_str}]  {note}")
    print()


if __name__ == "__main__":
    test_cases = [
        [170, 45, 75, 90, 2, 24],
        [5, 3, 8, 1, 9, 2],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [329, 457, 657, 839, 436, 720, 355],
        [],
        [1],
    ]

    print("=" * 60)
    print("基数排序 (Radix Sort)")
    print("=" * 60)

    hand_trace()

    print("\n详细排序过程:")
    radix_sort_verbose([170, 45, 75, 90, 2, 24])

    print("\n\n批量测试:")
    for tc in test_cases:
        original = tc.copy()
        result = radix_sort(tc)
        status = "✓" if result == sorted(original) else "✗"
        print(f"  {status} {original} → {result}")
