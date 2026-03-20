"""
串的基本操作和模式匹配

1. 串的基本操作: 赋值、比较、求长、拼接、求子串、定位
2. 朴素模式匹配: O(m*n), 暴力匹配
3. KMP 算法: O(m+n), 利用 next 数组避免回溯

考研要点:
  - 手算 next 数组和 nextval 数组 (重要!)
  - KMP 算法思想: 主串指针不回溯，模式串按 next 数组跳转
  - 朴素算法 vs KMP 的时间复杂度对比
"""


# ==========================================
# 1. 朴素模式匹配 (BF 算法)
# ==========================================

def brute_force(text, pattern):
    """朴素模式匹配 (暴力匹配)

    时间复杂度: O(m*n)
    思路: 主串每个位置都尝试匹配模式串
    """
    n, m = len(text), len(pattern)
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            return i  # 匹配成功, 返回起始位置
    return -1


def brute_force_verbose(text, pattern):
    """带详细输出的朴素匹配"""
    n, m = len(text), len(pattern)
    print(f"  主串:   {text}")
    print(f"  模式串: {pattern}")
    print(f"  {'─' * 40}")

    comparisons = 0
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            comparisons += 1
            j += 1
        if j < m:
            comparisons += 1

        # 显示匹配过程
        spaces = " " * i
        matched = pattern[:j]
        if j == m:
            print(f"  {' ' * 10}{spaces}{pattern} ← 匹配成功! 位置={i}")
            print(f"  总比较次数: {comparisons}")
            return i
        else:
            fail_char = pattern[j] if j < m else ''
            print(f"  {' ' * 10}{spaces}{matched}{'×' if fail_char else ''}")

    print(f"  匹配失败, 总比较次数: {comparisons}")
    return -1


# ==========================================
# 2. KMP 算法
# ==========================================

def get_next(pattern):
    """求 next 数组

    next[j] = 模式串 pattern[0..j-1] 的最长公共前后缀长度
    即: 模式串在位置 j 匹配失败时, 应跳转到 next[j] 继续匹配

    手算方法:
    next[0] = -1 (或0, 取决于实现)
    next[1] = 0
    对于 j >= 2: 看 pattern[0..j-1] 的最长公共前后缀
    """
    m = len(pattern)
    next_arr = [0] * m
    next_arr[0] = -1
    if m == 1:
        return next_arr

    next_arr[1] = 0
    j = 2
    k = 0  # k 指向前缀末尾

    while j < m:
        if k == -1 or pattern[j - 1] == pattern[k]:
            k += 1
            next_arr[j] = k
            j += 1
        else:
            k = next_arr[k]

    return next_arr


def get_nextval(pattern, next_arr):
    """求 nextval 数组 (next 的优化版)

    优化思想: 如果 pattern[next[j]] == pattern[j],
    则跳到 next[j] 后还是会失败, 应该继续跳

    nextval[j] = next[j]   如果 pattern[next[j]] != pattern[j]
    nextval[j] = nextval[next[j]]  如果 pattern[next[j]] == pattern[j]
    """
    m = len(pattern)
    nextval = [0] * m
    nextval[0] = -1
    for j in range(1, m):
        if next_arr[j] != -1 and pattern[next_arr[j]] == pattern[j]:
            nextval[j] = nextval[next_arr[j]]
        else:
            nextval[j] = next_arr[j]
    return nextval


def kmp_search(text, pattern):
    """KMP 模式匹配算法

    时间复杂度: O(m + n)
    核心: 主串指针 i 不回溯, 模式串指针 j 按 next 数组跳转
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    next_arr = get_next(pattern)

    i = 0  # 主串指针
    j = 0  # 模式串指针

    while i < n and j < m:
        if j == -1 or text[i] == pattern[j]:
            i += 1
            j += 1
        else:
            j = next_arr[j]  # 模式串跳转, i 不回溯!

    if j == m:
        return i - m  # 匹配成功
    return -1


def kmp_verbose(text, pattern):
    """带详细输出的 KMP"""
    n, m = len(text), len(pattern)
    next_arr = get_next(pattern)
    nextval = get_nextval(pattern, next_arr)

    print(f"  主串:   {text}")
    print(f"  模式串: {pattern}")
    print(f"\n  --- next 数组 ---")
    print(f"  下标 j:  {list(range(m))}")
    print(f"  字符:    {list(pattern)}")
    print(f"  next:    {next_arr}")
    print(f"  nextval: {nextval}")
    print(f"\n  --- 匹配过程 ---")

    i = j = 0
    step = 0
    while i < n and j < m:
        step += 1
        if j == -1 or text[i] == pattern[j]:
            if j >= 0:
                match = "匹配" if text[i] == pattern[j] else ""
                print(f"  步骤{step}: i={i}('{text[i]}') j={j}('{pattern[j]}') {match}")
            else:
                print(f"  步骤{step}: j=-1, 重新开始")
            i += 1
            j += 1
        else:
            old_j = j
            j = next_arr[j]
            print(f"  步骤{step}: i={i}('{text[i]}') j={old_j}('{pattern[old_j]}') "
                  f"失败→ j跳到{j}")

    if j == m:
        print(f"\n  匹配成功! 位置 = {i - m}")
        return i - m
    print(f"\n  匹配失败")
    return -1


def next_array_demo():
    """next 数组手算演示"""
    print("=" * 60)
    print("next 数组手算过程")
    print("=" * 60)

    patterns = ["abaabcac", "ababaaab", "abcabd"]

    for p in patterns:
        next_arr = get_next(p)
        nextval = get_nextval(p, next_arr)
        print(f"\n  模式串: {p}")
        print(f"  {'j':>4s}  {'char':>4s}  {'next':>4s}  {'nextval':>7s}  说明")
        print(f"  {'─' * 50}")
        for j in range(len(p)):
            prefix = p[:j]
            if j == 0:
                desc = "约定 next[0]=-1"
            elif j == 1:
                desc = "next[1]=0"
            else:
                # 找最长公共前后缀
                max_len = 0
                for l in range(1, j):
                    if p[:l] == p[j-l:j]:
                        max_len = l
                desc = f"前缀后缀公共长度={max_len}"
            print(f"  {j:>4d}  {p[j]:>4s}  {next_arr[j]:>4d}  {nextval[j]:>7d}  {desc}")
    print()


def comparison_demo():
    """朴素 vs KMP 对比"""
    print("=" * 60)
    print("朴素匹配 vs KMP 对比")
    print("=" * 60)

    text = "aaaaaaaab"
    pattern = "aaab"

    print(f"\n  === 朴素匹配 ===")
    brute_force_verbose(text, pattern)

    print(f"\n  === KMP 匹配 ===")
    kmp_verbose(text, pattern)
    print()


if __name__ == "__main__":
    next_array_demo()
    comparison_demo()

    # 批量测试
    print("=" * 60)
    print("批量测试")
    print("=" * 60)
    test_cases = [
        ("hello world", "world", 6),
        ("aabaabaaf", "aabaaf", 3),
        ("ababababc", "ababc", 4),
        ("abcdef", "xyz", -1),
    ]
    for text, pattern, expected in test_cases:
        bf = brute_force(text, pattern)
        kmp = kmp_search(text, pattern)
        mark = "✓" if bf == expected and kmp == expected else "✗"
        print(f"  {mark} text='{text}', pattern='{pattern}' → BF={bf}, KMP={kmp}")

    print()
    print("=" * 60)
    print("考研要点速记")
    print("=" * 60)
    print("""
  1. 朴素匹配: O(mn), 匹配失败 i 回溯到 i-j+2

  2. KMP: O(m+n), i 不回溯, j 按 next 跳转

  3. next 数组含义:
     next[j] = pattern[0..j-1] 最长公共前后缀长度
     next[0] = -1, next[1] = 0

  4. nextval 优化:
     若 pattern[next[j]] == pattern[j], 跳了也白跳
     nextval[j] = nextval[next[j]]

  5. 手算 next 的方法:
     看 pattern[0..j-1] 中, 最长的【既是前缀又是后缀】的子串长度
    """)
