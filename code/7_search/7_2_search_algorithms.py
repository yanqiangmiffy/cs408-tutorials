"""
查找算法: 顺序查找、折半查找、分块查找

1. 顺序查找: O(n), 适用于任何线性表
2. 折半查找: O(log n), 仅适用于有序顺序表
3. 分块查找: 块间有序折半 + 块内顺序查找

考研要点:
  - 折半查找的判定树
  - 折半查找的 ASL (成功/失败)
  - 分块查找的 ASL 分析
"""


def sequential_search(arr, key):
    """顺序查找 O(n)"""
    for i in range(len(arr)):
        if arr[i] == key:
            return i
    return -1


def sequential_search_sentinel(arr, key):
    """带哨兵的顺序查找

    将 key 放到 arr[0] 作为哨兵, 从后往前找
    优点: 不需要每次判断下标是否越界
    """
    arr_copy = [key] + arr  # arr_copy[0] = 哨兵
    i = len(arr_copy) - 1
    while arr_copy[i] != key:
        i -= 1
    return i - 1 if i > 0 else -1  # 返回在原数组中的下标


def binary_search(arr, key):
    """折半查找 O(log n)

    前提: arr 必须有序 (升序)

    步骤:
    1. low=0, high=n-1
    2. mid = (low + high) // 2
    3. arr[mid] == key → 找到
    4. arr[mid] > key  → high = mid - 1
    5. arr[mid] < key  → low = mid + 1
    6. low > high 时查找失败
    """
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == key:
            return mid
        elif arr[mid] > key:
            high = mid - 1
        else:
            low = mid + 1
    return -1


def binary_search_verbose(arr, key):
    """带详细输出的折半查找"""
    low, high = 0, len(arr) - 1
    step = 0

    print(f"  数组: {arr}")
    print(f"  查找: {key}")
    print(f"  {'步骤':>4s} {'low':>4s} {'high':>5s} {'mid':>4s} {'arr[mid]':>8s} {'比较':>6s}")
    print(f"  {'─' * 35}")

    while low <= high:
        step += 1
        mid = (low + high) // 2
        if arr[mid] == key:
            print(f"  {step:>4d} {low:>4d} {high:>5d} {mid:>4d} {arr[mid]:>8d} {'命中':>6s}")
            return mid
        elif arr[mid] > key:
            print(f"  {step:>4d} {low:>4d} {high:>5d} {mid:>4d} {arr[mid]:>8d} {'左半':>6s}")
            high = mid - 1
        else:
            print(f"  {step:>4d} {low:>4d} {high:>5d} {mid:>4d} {arr[mid]:>8d} {'右半':>6s}")
            low = mid + 1

    print(f"  查找失败! low={low} > high={high}")
    return -1


def block_search(blocks, block_index, key):
    """分块查找

    blocks: 分块后的数据 [[block1], [block2], ...]
    block_index: 索引表 [每块最大值, ...]

    步骤:
    1. 在索引表中折半查找, 确定 key 所在块
    2. 在块内顺序查找
    """
    # 1. 索引表折半查找
    low, high = 0, len(block_index) - 1
    block_id = -1
    while low <= high:
        mid = (low + high) // 2
        if key <= block_index[mid]:
            block_id = mid
            high = mid - 1
        else:
            low = mid + 1

    if block_id == -1:
        return -1

    # 2. 块内顺序查找
    for i, val in enumerate(blocks[block_id]):
        if val == key:
            # 计算全局下标
            global_idx = sum(len(blocks[j]) for j in range(block_id)) + i
            return global_idx

    return -1


def binary_search_demo():
    """折半查找演示"""
    print("=" * 60)
    print("折半查找")
    print("=" * 60)

    arr = [7, 10, 13, 16, 19, 29, 32, 33, 37, 41, 43]

    for key in [33, 20]:
        print(f"\n  --- 查找 {key} ---")
        result = binary_search_verbose(arr, key)
        if result >= 0:
            print(f"  ✓ 找到, 下标={result}")
        else:
            print(f"  ✗ 未找到")

    # ASL 分析
    print(f"""
  折半查找判定树 (n=11):
              19
            /    \\
          10       33
         / \\     /  \\
        7   13  29   41
         \\   \\   \\  / \\
         10  16  32 37 43

  ASL(成功) = (1×1 + 2×2 + 3×4 + 4×4) / 11 = 33/11 = 3.0
  ASL(失败) = (3×4 + 4×8) / 12 = 44/12 ≈ 3.67
    """)


def block_search_demo():
    """分块查找演示"""
    print("=" * 60)
    print("分块查找")
    print("=" * 60)

    blocks = [
        [22, 12, 13, 8, 9],     # 最大值 22
        [33, 42, 44, 38, 24],   # 最大值 44
        [48, 60, 58, 74, 57],   # 最大值 74
    ]
    block_index = [22, 44, 74]

    print(f"\n  索引表: {block_index}")
    for i, blk in enumerate(blocks):
        print(f"  块{i}: {blk} (最大={block_index[i]})")

    for key in [38, 50]:
        result = block_search(blocks, block_index, key)
        mark = "✓" if result >= 0 else "✗"
        print(f"\n  {mark} 查找 {key}: {'下标=' + str(result) if result >= 0 else '未找到'}")

    print(f"""
  分块查找 ASL:
  设 s 块, 每块 t 个元素 (n = s × t)
    块间折半 + 块内顺序: ASL ≈ log₂(s+1) + (t+1)/2
    块间顺序 + 块内顺序: ASL = (s+1)/2 + (t+1)/2

  当 s = √n 时, ASL 最小 ≈ √n + 1
    """)


if __name__ == "__main__":
    # 顺序查找
    print("=" * 60)
    print("顺序查找")
    print("=" * 60)
    arr = [5, 3, 8, 1, 9, 2]
    for key in [8, 7]:
        idx = sequential_search(arr, key)
        mark = "✓" if idx >= 0 else "✗"
        print(f"  {mark} 在 {arr} 中查找 {key}: {'下标=' + str(idx) if idx >= 0 else '未找到'}")

    print(f"\n  ASL(成功) = (1+2+...+n)/n = (n+1)/2")
    print(f"  ASL(失败) = n+1 (带哨兵) 或 n")

    print()
    binary_search_demo()
    block_search_demo()

    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 顺序查找:
     ASL成功 = (n+1)/2, ASL失败 = n+1
     适用: 任意线性表, 无序也可

  2. 折半查找:
     ASL成功 ≈ log₂(n+1) - 1
     仅适用于有序顺序表 (不能是链表!)
     判定树是平衡BST

  3. 分块查找:
     块间有序 + 块内无序
     ASL ≈ log₂(s+1) + (t+1)/2
    """)
